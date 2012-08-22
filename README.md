tasty-cli
=========

Command Line client for Tastypie REST Api

Installation
=

Requirements
-

git clone https://github.com/rtucker-mozilla/tastypie-client.git

cd tastypie-client

sudo python setup.py install

tasty-cli installation
-
git clone https://github.com/rtucker-mozilla/tasty-cli.git

Create a text file in your homedir .tasty-cli

The syntax is the file shall have 3 lines:

username

password

url_of_api

Usage
=

./api.py --help
usage: PROG [-h]
            
            {key_value,operating_system,system,server_model,allocation,system_status,location,system_rack,interface}
            ...

positional arguments:
  {key_value,operating_system,system,server_model,allocation,system_status,location,system_rack,interface}
    key_value           api access to key_value
    operating_system    api access to operating_system
    system              api access to system
    server_model        api access to server_model
    allocation          api access to allocation
    system_status       api access to system_status
    location            api access to location
    system_rack         api access to system_rack
    interface           Interface Manipulation

optional arguments:
  -h, --help            show this help message and exit
