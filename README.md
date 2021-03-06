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

Top Level Help
-
    Command:
    ./api.py --help
    Response:
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

Module Level Help
-
    Command:
    ./api.py operating_system --help
    Response:
    usage: PROG operating_system [-h] [--create] [--delete] [--update] [--search]
                                 [--read] [--version VERSION] [--id ID]
                                 [--name NAME] [--resource_uri RESOURCE_URI]
                                 argument__
    
    positional arguments:
      argument__            OBJECT to act upon
    
    optional arguments:
      -h, --help            show this help message and exit
      --create              ACTION: create operating_system
      --delete              ACTION: delete operating_system
      --update              ACTION: update operating_system
      --search              ACTION: search for operating_system
      --read                ACTION: read operating_system
      --version VERSION     Unicode string data. Ex: "Hello World"
      --id ID               Integer data. Ex: 2673
      --name NAME           Unicode string data. Ex: "Hello World"
      --resource_uri RESOURCE_URI
                            Unicode string data. Ex: "Hello World"

Reading an Object
-
    Command:
    ./api.py operating_system 12 --read 
    Response:
    id: 12
    name: Fedora Core
    version: 7

Updating an Object
-
You can update an object by looking at the results returned, they start with --.
They will be the ones besides the ACTION items

    Command:
    ./api.py operating_system 12 --update --name='Ubuntu'
    Response:
    Success

Creating an Interface
-
    Command:
    ./api.py interface --create --system=system.host.name --mac=00:00:00:00:00:00\
    --fqdn=host.vlan.dc.mozilla.com --range=10.0.0.1,10.0.0.255
    Response:
    Success (Will eventually return the interface details) 
