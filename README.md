py-auto-resource-generator
==========================
Puppet and chef data-model generator from Yang model.


Overview
=========
Python library for conversion of standardized Yang data model to IT automation tool data model for Puppet and Chef.
The library is in initial phase of development and currently support conversion from Yang model to Puppet resource type, 
support for Chef will be added in future.

Getting started
================
Make sure to install pyang and lxml.
Install lxml
```
pip install lxml
```

Install pyang  
```
pip install pyang
```
Add puppet.py in plugin directory of pyang installation.

For instruction on using pyang refer
[pyang](http://www.yang-central.org/twiki/pub/Main/YangTools/pyang.1.html)

Below is the command to generate interface Puppet resource type from interface Yang model
```
$pyang -f puppet --puppet-output /usr/tmp ietf-interfaces.yang
```
Puppet resource types file will be created in 'puppet-types' folder in destination path mentioned in command after '--puppet-output', if destination path is not give the 'puppet-types' folder will be created in current working directory.


LICENSE
========
Apache 2.0

CONTRIBUTORS
=============
* Ganesh Nalawade (@ganesh634)
