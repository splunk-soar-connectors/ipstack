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
import ipaddress

from soar_sdk.action_results import MakeRequestOutput
from soar_sdk.exceptions import ActionFailure
from soar_sdk.params import MakeRequestParams, Param

from ..asset import Asset
from ..client import get_response


MAX_BULK_IPS = 50


class IpstackMakeRequestParams(MakeRequestParams):
    http_method: str = Param(
        description="Only GET is supported for bulk IP lookups.",
        required=False,
        default="GET",
        value_list=["GET"],
    )
    endpoint: str = Param(
        description="Two to 50 comma-separated IPv4 or IPv6 addresses. Example: /1.1.1.1,8.8.8.8",
        required=True,
    )
    headers: str | None = Param(description="Not supported for bulk IP lookup. Leave empty.", required=False)
    query_parameters: str | None = Param(description="Not supported for bulk IP lookup. Leave empty.", required=False)
    body: str | None = Param(description="Not supported for bulk IP lookup. Leave empty.", required=False)
    timeout: int | None = Param(description="Timeout for the request in seconds.", required=False)
    verify_ssl: bool = Param(description="Whether to verify the SSL certificate.", required=False, default=True)


def _bulk_endpoint(endpoint: str) -> str:
    value = endpoint.strip()
    if value.startswith(("http://", "https://")):
        raise ActionFailure("Provide only a comma-separated list of IP addresses, without a base URL.")

    ips = [ip.strip() for ip in value.lstrip("/").split(",")]
    if not 2 <= len(ips) <= MAX_BULK_IPS or any(not ip for ip in ips):
        raise ActionFailure(f"Provide between 2 and {MAX_BULK_IPS} comma-separated IP addresses.")

    try:
        for ip in ips:
            ipaddress.ip_address(ip)
    except ValueError as exc:
        raise ActionFailure("Each bulk lookup value must be a valid IPv4 or IPv6 address.") from exc
    return ",".join(ips)


def make_request(params: IpstackMakeRequestParams, asset: Asset) -> MakeRequestOutput:
    """Run an ipstack bulk IP lookup and return its raw response."""
    if params.http_method != "GET":
        raise ActionFailure("Only GET is supported for bulk IP lookup.")
    if params.headers or params.query_parameters or params.body:
        raise ActionFailure("Headers, query parameters, and body are not supported for bulk IP lookup.")
    if params.timeout is not None and params.timeout <= 0:
        raise ActionFailure("Timeout must be greater than zero.")

    response = get_response(
        asset,
        _bulk_endpoint(params.endpoint),
        timeout=params.timeout or 30,
        verify_ssl=params.verify_ssl,
    )
    return MakeRequestOutput(status_code=response.status_code, response_body=response.text)
