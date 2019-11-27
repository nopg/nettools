import sys
import asyncio
import yaml
import getpass
import logging
import tkinter as tk
from datetime import datetime

import netdev

PYTHONASYNCIODEBUG = 1

#netdev_logger = netdev.logger
#netdev_logger.setLevel(logging.INFO)
#netdev_logger.addHandler(logging.StreamHandler())

def ly(filename):
    try:
        with open(filename) as _:
            return yaml.load(_)
    except:
        print("Invalid device file!")
        sys.exit(0)

def main(fin,configpath,username,password,COMMANDS,outputBox=None,root=None):

    start_time = datetime.now()
    devices = ly(fin)
    timeouts = []
    authfailed = []
    connectrefused = []
    unknownerror = []
    successes = []

    def present_output(msg):
        if not outputBox or not root:
            print(msg, end='', flush=True)
        else:
            outputBox.insert(tk.END, msg)
            outputBox.see(tk.END)
            root.update()
            print(msg, end='', flush=True)

    async def connect_and_run(device, configpath, COMMANDS):

        present_output("\nConnecting to {}.....\n".format(device['host']))
        try: 
            ios = netdev.create(**device)
            await ios.connect()
        except netdev.exceptions.TimeoutError as e:
            timeouts.append(device['host'])
            present_output("\nERROR =  {}".format(e))
            return
        except netdev.exceptions.DisconnectError as e:
            authfailed.append(device['host'])
            present_output("\nERROR = {}".format(e))
            return
        except netdev.exceptions.CommitError as e:
            unknownerror.append(device['host'])
            present_output("\nERROR = {}".format(e))
            return
        except Exception as e:
            unknownerror.append(device['host'])
            present_output("\nERROR = {}".format(e))
            return

        filename = ios.base_prompt
        
        filename = filename + '..' + \
        str(datetime.now().year) + '-' + \
        str(datetime.now().month) + '-' + \
        str(datetime.now().day) + '--' + \
        str(datetime.now().hour) + '-' + \
        str(datetime.now().minute) + '-' + \
        str(datetime.now().second) + '.' + \
        str(datetime.now().microsecond) + '.log'
                
        successes.append( (device['host'] , filename + ".log") )
        present_output("Success connecting to {}\nOutput:".format(device['host']))
                
        if configpath == '':
            for command in COMMANDS:
                present_output("\nRunning Command: {}\n\n".format(command))
                output = await ios.send_command(command)
                present_output(output)
        else:
            try:
                with open(configpath + "/" + filename, 'w') as fout:
                    for command in COMMANDS:
                        present_output("\nRunning Command: {}\n\n".format(command))
                        fout.write('\n\nRunning Command:\n' + command + '\n\n')
                        output = await ios.send_command(command)
                        present_output(output)
                        fout.write(output)
                fout.close()
            except FileNotFoundError:
                present_output("\nInvalid destination folder!\nContinuing....\n")
                return

    # BUILD DEVICE LIST TO SEND INTO run_loop() #
    device_list = []

    for type in devices:
        if devices[type]:
            for ip in devices[type]:
                secret = ''
                if type == 'IOS':
                    device_type = 'cisco_ios'
                elif type == 'NX-OS':
                    device_type = 'cisco_nxos'             
                elif type == 'ASA':
                    device_type = 'cisco_asa'  
                elif type == 'ASA-ENABLE':
                    device_type = 'cisco_asa'
                    password = ip[1]
                    secret = ip[2]
                    ip = ip[0]
                if ip:
                    device_list.append( {'username': username, 'password': password, 'secret': secret, 'device_type': device_type, 'host': ip} )

    # RUN LOOP #
    loop = asyncio.get_event_loop()
    tasks = [connect_and_run(device, configpath, COMMANDS) for device in device_list]
    loop.run_until_complete(asyncio.wait(tasks))

    present_output("\n\n\n\nStats from last run:")
    
    present_output("\n\n\nDevices timed out: ")
    [present_output("\n" + each) for each in timeouts]

    present_output("\n\nAuthentication failures:")
    [present_output("\n" + each) for each in authfailed]
        
    present_output("\n\nConnection Refused:")
    [present_output("\n" + each) for each in connectrefused]
        
    present_output("\n\nUnknown Error:")
    [present_output("\n" + each) for each in unknownerror]
        
    present_output("\n\nSuccessful: ")
    [present_output("\n{:15s} {:15s}".format(addr,fname)) for addr,fname in successes]
        
    present_output("\n\nTime elapsed: {}\n\n".format(datetime.now() - start_time))

    present_output("\n\nComplete! Thank you for using nettools (needs a better name!).\n\n")

    return

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("\nplease provide the following arguments:")
        print("\tpython3 file_run_commands.py <device-file.yml> <output folder path> <username>\n\n")
        sys.exit(0)

    device_file = sys.argv[1]
    configpath = sys.argv[2]
    username = sys.argv[3]

    password = getpass.getpass("Type the password: ")

    commands = []
    command = input("Enter the commands, one line at a time. Blank line to finish: ")
    while command:
        commands.append(command)
        command = input("Next command: ")

    main(device_file, configpath, username, password, commands)

