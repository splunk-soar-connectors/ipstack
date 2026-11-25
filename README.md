# ipstack

Publisher: Splunk <br>
Connector Version: 3.0.1 <br>
Product Vendor: ipstack <br>
Product Name: ipstack <br>
Minimum Product Version: 7.0.0

Integrates with ipstack to implement investigative actions

### Configuration variables

This table lists the configuration variables required to operate ipstack. These variables are specified when configuring a ipstack asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access_key** | required | password | API Access Key |
**use_ssl** | optional | boolean | Use SSL encryption |

### Supported Actions

[test connectivity](#action-test-connectivity) - test connectivity <br>
[make request](#action-make-request) - Make an authenticated request to an ipstack API endpoint. <br>
[geolocate ip](#action-geolocate-ip) - Queries Service for IP location info <br>
[geolocate domain](#action-geolocate-domain) - Geolocate a domain

## action: 'test connectivity'

test connectivity

Type: **test** <br>
Read only: **True**

Basic test for app.

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'make request'

Make an authenticated request to an ipstack API endpoint.

Type: **generic** <br>
Read only: **False**

'make request' action for the app. Used to handle arbitrary HTTP requests with the app's asset

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**http_method** | required | The HTTP method to use for the request. | string | |
**endpoint** | required | The endpoint to send the request to. | string | |
**headers** | optional | The headers to send with the request (JSON object). An example is {'Content-Type': 'application/json'} | string | |
**query_parameters** | optional | Parameters to append to the URL (JSON object or query string). An example is ?key=value&key2=value2 | string | |
**body** | optional | The body to send with the request (JSON object). An example is {'key': 'value', 'key2': 'value2'} | string | |
**timeout** | optional | The timeout for the request in seconds. | numeric | |
**verify_ssl** | optional | Whether to verify the SSL certificate. Default is True. | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.http_method | string | | |
action_result.parameter.endpoint | string | | |
action_result.parameter.headers | string | | |
action_result.parameter.query_parameters | string | | |
action_result.parameter.body | string | | |
action_result.parameter.timeout | numeric | | |
action_result.parameter.verify_ssl | boolean | | |
action_result.data.\*.status_code | numeric | | 200 404 500 |
action_result.data.\*.response_body | string | | {"key": "value"} |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'geolocate ip'

Queries Service for IP location info

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** | required | IP to lookup | string | `ip` `ipv6` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.ip | string | `ip` `ipv6` | |
action_result.data.\*.city | string | | Mountain View |
action_result.data.\*.continent_code | string | | AS |
action_result.data.\*.continent_name | string | | Asia |
action_result.data.\*.country_code | string | | US |
action_result.data.\*.country_name | string | | United States |
action_result.data.\*.ip | string | `ip` `ipv6` | 216.58.100.174 2405:205:c00b:98f7:9103:6255:bf6:19d5 |
action_result.data.\*.latitude | numeric | | 37.4002 23.0013 |
action_result.data.\*.longitude | numeric | | -122.0004 72.6007 |
action_result.data.\*.metro_code | numeric | | 800 |
action_result.data.\*.region_code | string | | CA |
action_result.data.\*.region_name | string | | California |
action_result.data.\*.time_zone.id | string | | America/Los_Angeles |
action_result.data.\*.time_zone.current_time | string | | 2026-08-19T06:22:04-07:00 |
action_result.data.\*.time_zone.gmt_offset | numeric | | -25200 |
action_result.data.\*.time_zone.code | string | | PDT |
action_result.data.\*.time_zone.is_daylight_saving | boolean | | True False |
action_result.data.\*.type | string | | ipv6 |
action_result.data.\*.zip | string | | 980000 |
action_result.data.\*.zip_code | string | | 94003 |
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
action_result.summary.city | string | | |
action_result.summary.country_code | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'geolocate domain'

Geolocate a domain

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** | required | A single domain or URL to geolocate; comma-separated values are not supported | string | `domain` `url` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failure |
action_result.message | string | | |
action_result.parameter.domain | string | `domain` `url` | |
action_result.data.\*.city | string | | Mountain View |
action_result.data.\*.continent_code | string | | AS |
action_result.data.\*.continent_name | string | | Asia |
action_result.data.\*.country_code | string | | US |
action_result.data.\*.country_name | string | | United States |
action_result.data.\*.ip | string | `ip` `ipv6` | 216.58.100.174 2405:205:c00b:98f7:9103:6255:bf6:19d5 |
action_result.data.\*.latitude | numeric | | 37.4002 23.0013 |
action_result.data.\*.longitude | numeric | | -122.0004 72.6007 |
action_result.data.\*.metro_code | numeric | | 800 |
action_result.data.\*.region_code | string | | CA |
action_result.data.\*.region_name | string | | California |
action_result.data.\*.time_zone.id | string | | America/Los_Angeles |
action_result.data.\*.time_zone.current_time | string | | 2026-08-19T06:22:04-07:00 |
action_result.data.\*.time_zone.gmt_offset | numeric | | -25200 |
action_result.data.\*.time_zone.code | string | | PDT |
action_result.data.\*.time_zone.is_daylight_saving | boolean | | True False |
action_result.data.\*.type | string | | ipv6 |
action_result.data.\*.zip | string | | 980000 |
action_result.data.\*.zip_code | string | | 94003 |
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
action_result.summary.city | string | | |
action_result.summary.country_code | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2026 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
