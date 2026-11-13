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
from soar_sdk.app import App

from ..models import GeoOutput, GeoSummary
from .geolocate_domain import DomainParams, geolocate_domain
from .geolocate_ip import IpParams, geolocate_ip


def register_actions(app: App) -> App:
    app.register_action(
        action=geolocate_ip,
        description="Queries Service for IP location info",
        action_type="investigate",
        read_only=True,
        params_class=IpParams,
        output_class=GeoOutput,
        summary_type=GeoSummary,
        render_as="table",
    )
    app.register_action(
        action=geolocate_domain,
        description="Geolocate a domain",
        action_type="investigate",
        read_only=True,
        params_class=DomainParams,
        output_class=GeoOutput,
        summary_type=GeoSummary,
        render_as="table",
    )
    return app
