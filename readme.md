# README IS A WORK IN PROGRESS WILL BE UPDATED SOON (5/20/19)

# NetTools
GUI front-end to a few modules I've created. 

 * Python 3 support only, substitute 'python/pip' with 'python3/pip3' if necessary
 * Most modules rely on the use of a device-list file *(yaml format, see sample-devices.yml for info) * for the list of devices to connect to.

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
 - ### APIC-EM (Deprecated, APIC-EM is dead)
 Connect to an APIC-EM Controller to pull a list of devices (using a device tag for searching, or all devices)
 User provides list of commands to be pushed to all devices. This can be used to gather 'show' output, or for configuration changes
 - ### Device File (.yml)
 Connect to all devices in the Device File, and run a list of commands against all devices. If configuration is needed, include 'config t' before the rest of the command set. Output via CLI/Popup Window, and optionally created an output file for each device in the list.
 - ### Manual Entry
Same as above, except manually enter all device IP's rather than using .yml file. This can be useful if you are too lazy to create the device file. Once run, a device file will automatically be created for you as a hidden temporary file within the local directory. The file can then be renamed and used on subsequent runs.
 - ### AP-Ports
 Search a list of devices (using .yml file) for a specific CDP string on every port. For every port found to have a neighbor matching this CDP string (Model/Device Type), output a 'show run interface xxx' for each discovered port. This was built to help discover AP's with incorrect switch port configurations.
 - ### Used Ports Inventory
Again using a .yml file, search through every device listed and output a .csv listing a port count and type for all devices. Very useful for determining port counts needed on new switches based on existing speed and SFP types found. Also shows any err-disabled ports found.
