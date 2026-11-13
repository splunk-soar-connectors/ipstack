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
from soar_sdk.abstract import SOARClient
from soar_sdk.app import App
from soar_sdk.logging import getLogger

from .actions import register_actions
from .asset import Asset
from .client import lookup


def create_app() -> App:
    app = App(
        name="ipstack",
        app_type="information",
        logo="logo_ipstack.svg",
        logo_dark="logo_ipstack_dark.svg",
        product_vendor="ipstack",
        product_name="ipstack",
        publisher="Splunk",
        appid="87078d70-ca1e-4dfa-9dbe-cf3fa56b99ae",
        fips_compliant=True,
        asset_cls=Asset,
        python_version="3.13",
    )

    @app.test_connectivity()
    def test_connectivity(soar: SOARClient, asset: Asset) -> None:
        getLogger().progress("Querying a domain to check connectivity")
        lookup(asset, "ipstack.com")
        soar.set_message("Test Connectivity Passed")

    return register_actions(app)


app = create_app()


if __name__ == "__main__":
    app.cli()
