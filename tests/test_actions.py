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

from src.actions.geolocate_domain import DomainParams, geolocate_domain
from src.actions.geolocate_ip import IpParams, geolocate_ip
from src.asset import Asset
from src.client import lookup


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
