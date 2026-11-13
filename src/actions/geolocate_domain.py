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
from urllib.parse import urlsplit

from soar_sdk.abstract import SOARClient
from soar_sdk.params import Param, Params

from ..asset import Asset
from ..client import lookup
from ..models import GeoOutput, GeoSummary


class DomainParams(Params):
    domain: str = Param(description="Domain to geolocate", primary=True, cef_types=["domain", "url"], column_name="Domain")


def geolocate_domain(params: DomainParams, soar: SOARClient, asset: Asset) -> list[GeoOutput]:
    try:
        parsed = urlsplit(params.domain)
        domain = parsed.hostname if parsed.scheme and parsed.hostname else params.domain
    except ValueError:
        domain = params.domain
    response = lookup(asset, domain)
    if not response.get("type"):
        soar.set_message("Provided domain was not found. Please provide a valid domain.")
        return []
    soar.set_summary(GeoSummary(city=response.get("city"), country_code=response.get("country_code")))
    soar.set_message(f"City: {response.get('city')}, Country code: {response.get('country_code')}")
    return [GeoOutput(**response)]
