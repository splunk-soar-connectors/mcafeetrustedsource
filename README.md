[comment]: # "Auto-generated SOAR connector documentation"
# McAfee TrustedSource

Publisher: Martin Ohl  
Connector Version: 1\.0\.0  
Product Vendor: McAfee  
Product Name: TrustedSource  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.0\.1068  

McAfee TrustedSource provides an online service that enables you to check website categorization and risk levels

### Supported Actions  
[test connectivity](#action-test-connectivity) - Test TrustedSource communication  
[lookup url](#action-lookup-url) - Check the url categorization and risk level  

## action: 'test connectivity'
Test TrustedSource communication

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'lookup url'
Check the url categorization and risk level

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**url** |  required  | URL to lookup | string |  `url`  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.url | string |  `url` 
action\_result\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.category | string | 
action\_result\.data\.\*\.score | numeric | 
action\_result\.data\.\*\.risk | string | 