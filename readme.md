# README IS A WORK IN PROGRESS WILL BE UPDATED SOON (5/17/19)

# NetTools
GUI front-end to a few modules I've created. 

 *Python 3 support only, substitute 'python/pip' with 'python3/pip3' if necessary
 *Most modules rely on the use of a device-list file *(yaml format, see sample-devices.yml for info)* for the list of devices to connect to.

## Required 3rd party Python modules
### (use pip install \<modulename>)
 - tkinter (built into most Python distros)
 - netdev
 - jtextfsm
 - requests
 - netmiko

## Usage
 - run *python nettools.py*
 - choose the module you will be using
 - input the required information
 - output will be displayed via console and popup window, as well as any output files specific to the module

## Module Descriptions
 - ### APIC-EM
 Connect to an APIC-EM Controller to pull a list of devices (using a device tag for searching, or all devices)
 User provides list of commands to be pushed to all devices. This can be used to gather 'show' output, or for configuration changes
 - ### Device File (.yml)
 
