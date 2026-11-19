# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import importlib
from types import SimpleNamespace
from unittest.mock import Mock

import httpx
import pytest
from pydantic import ValidationError
from soar_sdk.exceptions import ActionFailure
from soar_sdk.params import MakeRequestParams

from src.actions.geolocate_domain import DomainParams, geolocate_domain
from src.actions.geolocate_ip import IpParams, geolocate_ip
from src.actions.make_request import make_request
from src.asset import Asset
from src.client import lookup, send_request
from src.models import GeoOutput, TimeZoneOutput


def asset() -> Asset:
    return Asset(access_key=" secret ", use_ssl=True)


def test_lookup_sends_key_and_timeout(monkeypatch):
    request = httpx.Request("GET", "https://api.ipstack.com/8.8.8.8")
    response = httpx.Response(200, json={"ip": "8.8.8.8", "city": "Mountain View"}, request=request)
    get = Mock(return_value=response)
    monkeypatch.setattr(httpx, "get", get)

    assert lookup(asset(), "8.8.8.8")["city"] == "Mountain View"
    assert get.call_args.kwargs["params"] == {"access_key": "secret"}
    assert get.call_args.kwargs["timeout"] == 30
    assert get.call_args.kwargs["follow_redirects"] is True
    assert get.call_args.kwargs["verify"] is True


def test_http_200_api_error_is_failure(monkeypatch):
    monkeypatch.setattr(httpx, "get", lambda *args, **kwargs: httpx.Response(200, json={"success": False, "error": "bad key"}))
    with pytest.raises(ActionFailure, match="bad key"):
        lookup(asset(), "8.8.8.8")


def test_ip_false_values_become_null(monkeypatch):
    monkeypatch.setattr(
        importlib.import_module("src.actions.geolocate_ip"), "lookup", lambda *args: {"city": "", "country_code": "US", "latitude": 0}
    )
    soar = SimpleNamespace(set_summary=Mock(), set_message=Mock())
    output = geolocate_ip(IpParams(ip="8.8.8.8"), soar, asset())
    assert output.model_dump() == {"city": None, "country_code": "US", "latitude": None}
    soar.set_message.assert_called_once_with("City: None, Country code: US")


def test_invalid_ip_is_rejected_before_lookup():
    with pytest.raises(ValidationError, match="valid IPv4 or IPv6"):
        IpParams(ip="not-an-ip")


@pytest.mark.parametrize("domain", ["", "   ", "example.com,example.org"])
def test_invalid_domain_values_are_rejected(domain):
    with pytest.raises(ValidationError, match="Domain"):
        DomainParams(domain=domain)


def test_domain_url_and_missing_domain(monkeypatch):
    called = []

    def fake_lookup(_asset, endpoint):
        called.append(endpoint)
        return {"type": None}

    monkeypatch.setattr(importlib.import_module("src.actions.geolocate_domain"), "lookup", fake_lookup)
    soar = SimpleNamespace(set_summary=Mock(), set_message=Mock())
    assert geolocate_domain(DomainParams(domain="https://example.com/path"), soar, asset()) == []
    assert called == ["example.com"]
    soar.set_message.assert_called_once_with("Provided domain was not found. Please provide a valid domain.")


def test_domain_missing_type_fails(monkeypatch):
    monkeypatch.setattr(importlib.import_module("src.actions.geolocate_domain"), "lookup", lambda *args: {})
    soar = SimpleNamespace(set_summary=Mock(), set_message=Mock())

    with pytest.raises(ActionFailure, match="missing type"):
        geolocate_domain(DomainParams(domain="example.com"), soar, asset())


def test_domain_not_found_clears_summary(monkeypatch):
    from src.app import create_app

    responses = iter(
        [
            {"type": "ipv4", "city": "London", "country_code": "GB"},
            {"type": None},
        ]
    )
    monkeypatch.setattr(importlib.import_module("src.actions.geolocate_domain"), "lookup", lambda *args: next(responses))
    app = create_app()
    action = app.actions_manager.get_action("geolocate_domain")
    configured_asset = asset()

    assert action(DomainParams(domain="example.com"), asset=configured_asset)
    assert action(DomainParams(domain="does-not-resolve.invalid"), asset=configured_asset)

    first, second = app.actions_manager.get_results()
    assert first.get_summary() == {"city": "London", "country_code": "GB"}
    assert second.get_message() == "Provided domain was not found. Please provide a valid domain."
    assert second.get_data() == []
    assert second.get_summary() == {}


def test_domain_success_preserves_api_fields(monkeypatch):
    monkeypatch.setattr(
        importlib.import_module("src.actions.geolocate_domain"),
        "lookup",
        lambda *args: {"type": "ipv4", "city": "London", "country_code": "GB", "security": {"is_proxy": False}},
    )
    soar = SimpleNamespace(set_summary=Mock(), set_message=Mock())
    results = geolocate_domain(DomainParams(domain="example.com"), soar, asset())
    assert len(results) == 1
    assert results[0].model_dump()["security"] == {"is_proxy": False}
    soar.set_message.assert_called_once_with("City: London, Country code: GB")


def test_time_zone_output_preserves_api_object():
    output = GeoOutput(
        time_zone={
            "id": "America/Los_Angeles",
            "current_time": "2026-08-19T06:22:04-07:00",
            "gmt_offset": -25200,
            "code": "PDT",
            "is_daylight_saving": True,
        }
    )

    assert isinstance(output.time_zone, TimeZoneOutput)
    assert output.time_zone.id == "America/Los_Angeles"
    assert output.time_zone.gmt_offset == -25200


@pytest.mark.parametrize("endpoint", ["/8.8.8.8", "/check", "/1.1.1.1,8.8.8.8"])
def test_make_request_accepts_ipstack_endpoints(monkeypatch, endpoint):
    response = httpx.Response(200, json={"ip": "8.8.8.8"})
    request = Mock(return_value=response)
    monkeypatch.setattr(importlib.import_module("src.actions.make_request"), "send_request", request)
    configured_asset = asset()

    output = make_request(MakeRequestParams(http_method="GET", endpoint=endpoint), configured_asset)

    assert output.status_code == 200
    assert output.response_body == response.text
    assert request.call_args.args == (configured_asset, "GET", endpoint.lstrip("/"))
    assert request.call_args.kwargs == {
        "headers": None,
        "query_parameters": None,
        "body": None,
        "timeout": 30,
        "verify_ssl": True,
    }


def test_make_request_forwards_generic_parameters(monkeypatch):
    response = httpx.Response(202, text="accepted")
    request = Mock(return_value=response)
    monkeypatch.setattr(importlib.import_module("src.actions.make_request"), "send_request", request)
    configured_asset = asset()

    output = make_request(
        MakeRequestParams(
            http_method="POST",
            endpoint="/future-endpoint",
            headers='{"Content-Type": "application/json", "X-Test": "value"}',
            query_parameters='{"fields": "ip,city"}',
            body='{"enabled": true}',
            timeout=12,
            verify_ssl=False,
        ),
        configured_asset,
    )

    assert output.status_code == 202
    assert output.response_body == "accepted"
    request.assert_called_once_with(
        configured_asset,
        "POST",
        "future-endpoint",
        headers={"Content-Type": "application/json", "X-Test": "value"},
        query_parameters={"fields": "ip,city"},
        body={"enabled": True},
        timeout=12,
        verify_ssl=False,
    )


def test_send_request_adds_asset_access_key(monkeypatch):
    response = httpx.Response(200, text="ok")
    request = Mock(return_value=response)
    monkeypatch.setattr(httpx, "request", request)

    assert send_request(asset(), "GET", "check", query_parameters=[("fields", "ip,city")]) is response
    assert request.call_args.args == ("GET", "https://api.ipstack.com/check")
    assert request.call_args.kwargs["params"] == [("fields", "ip,city"), ("access_key", "secret")]
    assert request.call_args.kwargs["follow_redirects"] is False


@pytest.mark.parametrize(
    ("params", "message"),
    [
        (MakeRequestParams(http_method="GET", endpoint="https://api.ipstack.com/check"), "not a full URL"),
        (MakeRequestParams(http_method="GET", endpoint="check?fields=ip"), "through query_parameters"),
        (MakeRequestParams(http_method="GET", endpoint="check", headers='{"Host": "example.com"}'), "cannot be overridden"),
        (MakeRequestParams(http_method="GET", endpoint="check", query_parameters="access_key=other"), "cannot be overridden"),
        (MakeRequestParams(http_method="GET", endpoint="check", query_parameters="[]"), "JSON object or query string"),
        (MakeRequestParams(http_method="GET", endpoint="check", body="not-json"), "Invalid JSON body"),
        (MakeRequestParams(http_method="GET", endpoint="check", timeout=0), "greater than zero"),
    ],
)
def test_make_request_rejects_invalid_requests(params, message):
    with pytest.raises(ActionFailure, match=message):
        make_request(params, asset())
