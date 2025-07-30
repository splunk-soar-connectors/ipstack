# ipstack

Publisher: Splunk \
Connector Version: 2.0.8 \
Product Vendor: ipstack \
Product Name: ipstack \
Minimum Product Version: 5.1.0

Integrates with ipstack to implement investigative actions

### Configuration variables

This table lists the configuration variables required to operate ipstack. These variables are specified when configuring a ipstack asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access_key** | required | password | API Access Key |
**use_ssl** | optional | boolean | Use SSL encryption (not available with free version) |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration \
[geolocate ip](#action-geolocate-ip) - Queries Service for IP location info \
[geolocate domain](#action-geolocate-domain) - Geolocate a domain

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'geolocate ip'

Queries Service for IP location info

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** | required | IP to lookup | string | `ip` `ipv6` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.ip | string | `ip` `ipv6` | 192.168.0.10 24a6:205:c00b:98f7:9103:6255:bf6:19d5 |
action_result.data.\*.city | string | | Mountain View |
action_result.data.\*.continent_code | string | | AS |
action_result.data.\*.continent_name | string | | Asia |
action_result.data.\*.country_code | string | | US |
action_result.data.\*.country_name | string | | United States |
action_result.data.\*.ip | string | `ip` `ipv6` | 216.58.100.174 2405:205:c00b:98f7:9103:6255:bf6:19d5 |
action_result.data.\*.latitude | numeric | | 37.4002 23.0013 |
action_result.data.\*.location.calling_code | string | | 91 |
action_result.data.\*.location.capital | string | | Washington D.C. |
action_result.data.\*.location.country_flag | string | `url` | http://assets.ipstack.com/flags/in.svg |
action_result.data.\*.location.country_flag_emoji | string | | 🆪🇳 |
action_result.data.\*.location.country_flag_emoji_unicode | string | | U+1F1EE U+1F1F3 |
action_result.data.\*.location.geoname_id | numeric | | 1270033 |
action_result.data.\*.location.is_eu | boolean | | True False |
action_result.data.\*.location.languages.\*.code | string | | hi |
action_result.data.\*.location.languages.\*.name | string | | English |
action_result.data.\*.location.languages.\*.native | string | | हन्दी |
action_result.data.\*.longitude | numeric | | -122.0004 72.6007 |
action_result.data.\*.metro_code | numeric | | 800 |
action_result.data.\*.region_code | string | | CA |
action_result.data.\*.region_name | string | | California |
action_result.data.\*.time_zone | string | | America/Los_Angeles |
action_result.data.\*.type | string | | ipv6 |
action_result.data.\*.zip | string | | 980000 |
action_result.data.\*.zip_code | string | | 94003 |
action_result.summary.city | string | | Mountain View |
action_result.summary.country_code | string | | US |
action_result.message | string | | City: Mountain View, Country code: US |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'geolocate domain'

Geolocate a domain

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** | required | Domain to geolocate | string | `domain` `url` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.domain | string | `domain` `url` | https://test.com test.com |
action_result.data.\*.city | string | | Mountain View |
action_result.data.\*.continent_code | string | | NA |
action_result.data.\*.continent_name | string | | North America |
action_result.data.\*.country_code | string | | US |
action_result.data.\*.country_name | string | | United States |
action_result.data.\*.ip | string | `ip` `ipv6` | 192.168.0.4 2607:f8a0:4005:80b::230c |
action_result.data.\*.latitude | numeric | | 37.4002 37.001 |
action_result.data.\*.location.calling_code | string | | 1 |
action_result.data.\*.location.capital | string | | Washington D.C. |
action_result.data.\*.location.country_flag | string | `url` | http://path.to.api.com/flags/us.svg |
action_result.data.\*.location.country_flag_emoji | string | | 🆪🇸 |
action_result.data.\*.location.country_flag_emoji_unicode | string | | U+1F1FA U+1F1F8 |
action_result.data.\*.location.geoname_id | numeric | | 2964574 |
action_result.data.\*.location.is_eu | boolean | | True False |
action_result.data.\*.location.languages.\*.code | string | | en |
action_result.data.\*.location.languages.\*.name | string | | English |
action_result.data.\*.location.languages.\*.native | string | | English |
action_result.data.\*.longitude | numeric | | -122.0004 -97.002 |
action_result.data.\*.metro_code | numeric | | 800 |
action_result.data.\*.region_code | string | | CA |
action_result.data.\*.region_name | string | | California |
action_result.data.\*.time_zone | string | | America/Los_Angeles |
action_result.data.\*.type | string | | ipv6 |
action_result.data.\*.zip | string | | |
action_result.data.\*.zip_code | string | | 94003 |
action_result.summary.city | string | | Mountain View |
action_result.summary.country_code | string | | US |
action_result.message | string | | City: Mountain View, Country code: US City: None, Country code: US |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
