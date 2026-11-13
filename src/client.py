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
import httpx
from soar_sdk.exceptions import ActionFailure

from .asset import Asset


def lookup(asset: Asset, endpoint: str) -> dict:
    scheme = "https" if asset.use_ssl else "http"
    try:
        response = httpx.get(
            f"{scheme}://api.ipstack.com/{endpoint}",
            params={"access_key": asset.access_key.strip()},
            timeout=30,
            follow_redirects=True,
        )
    except httpx.RequestError as exc:
        raise ActionFailure(f"Error connecting to ipstack. Details: {type(exc).__name__}") from exc

    content_type = response.headers.get("Content-Type", "").lower()
    if "json" in content_type:
        try:
            data = response.json()
        except ValueError as exc:
            raise ActionFailure(f"Unable to parse JSON response. Error: {exc}") from exc
        if not isinstance(data, dict):
            raise ActionFailure("Unable to parse JSON response. Expected an object")
        if 200 <= response.status_code < 399 and data.get("success", True):
            return data
        raise ActionFailure(f"Error from server. Status Code: {response.status_code} Data from server: {response.text}")

    if "html" in content_type:
        from bs4 import BeautifulSoup

        message = "\n".join(line.strip() for line in BeautifulSoup(response.text, "html.parser").get_text().splitlines() if line.strip())
        raise ActionFailure(f"Status Code: {response.status_code}. Data from server:\n{message}\n")
    if not response.text:
        if response.status_code == 200:
            return {}
        raise ActionFailure("Empty response and no information in the header")
    raise ActionFailure(f"Can't process response from server. Status Code: {response.status_code} Data from server: {response.text}")
