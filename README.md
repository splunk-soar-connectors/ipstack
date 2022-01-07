[comment]: # "Auto-generated SOAR connector documentation"
# ipstack

Publisher: Splunk  
Connector Version: 2\.0\.2  
Product Vendor: ipstack  
Product Name: ipstack  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

Integrates with ipstack to implement investigative actions

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a ipstack asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access\_key** |  required  | password | API Access Key
**use\_ssl** |  optional  | boolean | Use SSL encryption \(not available with free version\)

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[geolocate ip](#action-geolocate-ip) - Queries Service for IP location info  
[geolocate domain](#action-geolocate-domain) - Geolocate a domain  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'geolocate ip'
Queries Service for IP location info

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** |  required  | IP to lookup | string |  `ip`  `ipv6` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.ip | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.city | string | 
action\_result\.data\.\*\.continent\_code | string | 
action\_result\.data\.\*\.continent\_name | string | 
action\_result\.data\.\*\.country\_code | string | 
action\_result\.data\.\*\.country\_name | string | 
action\_result\.data\.\*\.ip | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.latitude | numeric | 
action\_result\.data\.\*\.location\.calling\_code | string | 
action\_result\.data\.\*\.location\.capital | string | 
action\_result\.data\.\*\.location\.country\_flag | string |  `url` 
action\_result\.data\.\*\.location\.country\_flag\_emoji | string | 
action\_result\.data\.\*\.location\.country\_flag\_emoji\_unicode | string | 
action\_result\.data\.\*\.location\.geoname\_id | numeric | 
action\_result\.data\.\*\.location\.is\_eu | boolean | 
action\_result\.data\.\*\.location\.languages\.\*\.code | string | 
action\_result\.data\.\*\.location\.languages\.\*\.name | string | 
action\_result\.data\.\*\.location\.languages\.\*\.native | string | 
action\_result\.data\.\*\.longitude | numeric | 
action\_result\.data\.\*\.metro\_code | numeric | 
action\_result\.data\.\*\.region\_code | string | 
action\_result\.data\.\*\.region\_name | string | 
action\_result\.data\.\*\.time\_zone | string | 
action\_result\.data\.\*\.type | string | 
action\_result\.data\.\*\.zip | string | 
action\_result\.data\.\*\.zip\_code | string | 
action\_result\.summary\.city | string | 
action\_result\.summary\.country\_code | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'geolocate domain'
Geolocate a domain

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain to geolocate | string |  `domain`  `url` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.domain | string |  `domain`  `url` 
action\_result\.data\.\*\.city | string | 
action\_result\.data\.\*\.continent\_code | string | 
action\_result\.data\.\*\.continent\_name | string | 
action\_result\.data\.\*\.country\_code | string | 
action\_result\.data\.\*\.country\_name | string | 
action\_result\.data\.\*\.ip | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.latitude | numeric | 
action\_result\.data\.\*\.location\.calling\_code | string | 
action\_result\.data\.\*\.location\.capital | string | 
action\_result\.data\.\*\.location\.country\_flag | string |  `url` 
action\_result\.data\.\*\.location\.country\_flag\_emoji | string | 
action\_result\.data\.\*\.location\.country\_flag\_emoji\_unicode | string | 
action\_result\.data\.\*\.location\.geoname\_id | numeric | 
action\_result\.data\.\*\.location\.is\_eu | boolean | 
action\_result\.data\.\*\.location\.languages\.\*\.code | string | 
action\_result\.data\.\*\.location\.languages\.\*\.name | string | 
action\_result\.data\.\*\.location\.languages\.\*\.native | string | 
action\_result\.data\.\*\.longitude | numeric | 
action\_result\.data\.\*\.metro\_code | numeric | 
action\_result\.data\.\*\.region\_code | string | 
action\_result\.data\.\*\.region\_name | string | 
action\_result\.data\.\*\.time\_zone | string | 
action\_result\.data\.\*\.type | string | 
action\_result\.data\.\*\.zip | string | 
action\_result\.data\.\*\.zip\_code | string | 
action\_result\.summary\.city | string | 
action\_result\.summary\.country\_code | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 