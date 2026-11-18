# Copyright (c) 2018-2026 Splunk Inc.
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
import json
import re
from typing import Any
from urllib.parse import parse_qsl

from soar_sdk.action_results import MakeRequestOutput
from soar_sdk.exceptions import ActionFailure
from soar_sdk.params import MakeRequestParams

from ..asset import Asset
from ..client import send_request


DEFAULT_REQUEST_TIMEOUT_SECONDS = 30
BLOCKED_HEADERS = {"authorization", "host", "proxy-authorization"}
URL_SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")


def _endpoint(value: str) -> str:
    endpoint = value.strip()
    if not endpoint:
        raise ActionFailure("Endpoint cannot be empty")
    if URL_SCHEME_PATTERN.match(endpoint) or endpoint.startswith("//"):
        raise ActionFailure("Invalid endpoint: provide an ipstack API path, not a full URL")
    if "?" in endpoint or "#" in endpoint:
        raise ActionFailure("Invalid endpoint: provide query values through query_parameters")
    return endpoint.lstrip("/")


def _headers(value: str | None) -> dict[str, str] | None:
    if not value:
        return None
    try:
        headers = json.loads(value)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ActionFailure("Invalid JSON headers") from exc
    if not isinstance(headers, dict) or not all(isinstance(key, str) and isinstance(item, str) for key, item in headers.items()):
        raise ActionFailure("Invalid JSON headers: provide an object containing string values")
    if any(key.lower() in BLOCKED_HEADERS for key in headers):
        raise ActionFailure("Authorization, Host, and Proxy-Authorization headers cannot be overridden")
    return headers


def _query_parameters(value: str | None) -> dict[str, Any] | list[tuple[str, str]] | None:
    if not value:
        return None
    try:
        query_parameters = json.loads(value)
    except json.JSONDecodeError as exc:
        if value.lstrip().startswith("{"):
            raise ActionFailure("Invalid query parameters") from exc
        query_parameters = parse_qsl(value.lstrip().lstrip("?"), keep_blank_values=True)
    else:
        if not isinstance(query_parameters, dict):
            raise ActionFailure("Invalid query parameters: provide a JSON object or query string")

    keys = query_parameters if isinstance(query_parameters, dict) else (key for key, _ in query_parameters)
    if any(str(key).lower() == "access_key" for key in keys):
        raise ActionFailure("The asset access key cannot be overridden")
    return query_parameters


def _body(value: str | None) -> dict[str, Any] | list[Any] | None:
    if not value:
        return None
    try:
        body = json.loads(value)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ActionFailure("Invalid JSON body") from exc
    if not isinstance(body, dict | list):
        raise ActionFailure("Invalid JSON body: provide a JSON object or array")
    return body


def make_request(params: MakeRequestParams, asset: Asset) -> MakeRequestOutput:
    """Make an authenticated request to an ipstack API endpoint."""
    if params.timeout is not None and params.timeout <= 0:
        raise ActionFailure("Timeout must be greater than zero")

    response = send_request(
        asset,
        params.http_method,
        _endpoint(params.endpoint),
        headers=_headers(params.headers),
        query_parameters=_query_parameters(params.query_parameters),
        body=_body(params.body),
        timeout=params.timeout or DEFAULT_REQUEST_TIMEOUT_SECONDS,
        verify_ssl=params.verify_ssl,
    )
    return MakeRequestOutput(status_code=response.status_code, response_body=response.text)
