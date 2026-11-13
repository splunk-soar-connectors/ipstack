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
from soar_sdk.action_results import ActionOutput, OutputField, PermissiveActionOutput


class LanguageOutput(ActionOutput):
    code: str | None = OutputField(example_values=["hi"])
    name: str | None = OutputField(example_values=["English"])
    native: str | None = OutputField(example_values=["ह\x0fन्दी"])


class LocationOutput(ActionOutput):
    calling_code: str | None = OutputField(example_values=["91"])
    capital: str | None = OutputField(example_values=["Washington D.C."])
    country_flag: str | None = OutputField(cef_types=["url"], example_values=["http://assets.ipstack.com/flags/in.svg"])
    country_flag_emoji: str | None = OutputField(example_values=["🆪🇳"])
    country_flag_emoji_unicode: str | None = OutputField(example_values=["U+1F1EE U+1F1F3"])
    geoname_id: float | None = OutputField(example_values=[1270033])
    is_eu: bool | None = OutputField(example_values=[True, False])
    languages: list[LanguageOutput] | None = None


class GeoOutput(PermissiveActionOutput):
    city: str | None = OutputField(column_name="City", example_values=["Mountain View"])
    continent_code: str | None = OutputField(example_values=["AS"])
    continent_name: str | None = OutputField(example_values=["Asia"])
    country_code: str | None = OutputField(example_values=["US"])
    country_name: str | None = OutputField(column_name="Country", example_values=["United States"])
    ip: str | None = OutputField(cef_types=["ip", "ipv6"], example_values=["216.58.100.174", "2405:205:c00b:98f7:9103:6255:bf6:19d5"])
    latitude: float | None = OutputField(example_values=[37.4002, 23.0013])
    longitude: float | None = OutputField(example_values=[-122.0004, 72.6007])
    metro_code: float | None = OutputField(example_values=[800])
    region_code: str | None = OutputField(example_values=["CA"])
    region_name: str | None = OutputField(column_name="Region", example_values=["California"])
    time_zone: str | None = OutputField(example_values=["America/Los_Angeles"])
    type: str | None = OutputField(example_values=["ipv6"])
    zip: str | None = OutputField(example_values=["980000"])
    zip_code: str | None = OutputField(example_values=["94003"])
    location: LocationOutput | None = None


class GeoSummary(ActionOutput):
    city: str | None = None
    country_code: str | None = None
