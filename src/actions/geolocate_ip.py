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

import pydantic
from soar_sdk.abstract import SOARClient
from soar_sdk.params import Param, Params

from ..asset import Asset
from ..client import lookup
from ..models import GeoOutput, GeoSummary


# Pydantic exposes this helper dynamically, so import it through the module to keep static analysis accurate.
field_validator = getattr(pydantic, "field_validator")


class IpParams(Params):
    ip: str = Param(description="IP to lookup", primary=True, cef_types=["ip", "ipv6"], column_name="IP")

    @field_validator("ip")
    @classmethod
    def validate_ip(cls, value: str) -> str:
        try:
            ipaddress.ip_address(value)
        except ValueError as exc:
            raise ValueError("IP must be a valid IPv4 or IPv6 address") from exc
        return value


def geolocate_ip(params: IpParams, soar: SOARClient, asset: Asset) -> GeoOutput:
    response = lookup(asset, params.ip)
    response = {key: value if value else None for key, value in response.items()}
    soar.set_summary(GeoSummary(city=response.get("city"), country_code=response.get("country_code")))
    soar.set_message(f"City: {response.get('city')}, Country code: {response.get('country_code')}")
    return GeoOutput(**response)
