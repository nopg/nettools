import sys
import yaml
import tkinter as tk
from datetime import datetime

from netmiko import ConnectHandler
from netmiko.ssh_exception import *

def ly(filename):
    try:
        with open(filename) as _:
            return yaml.load(_)
    except:
        print("Invalid device file!")
        sys.exit(0)

def run_commands(fin,configpath,username,password,COMMANDS,outputBox,root):
    start_time = datetime.now()
    devices = ly(fin)
    timeouts = []
    authfailed = []
    connectrefused = []
    unknownerror = []
    successes = []
    outputBox.insert(tk.END,"\n\n\nThank you! Gathering Output..\n\n\n")
    root.update()
    print("\n\n\nThank you! Gathering Output..\n\n\n")

    for type in devices:
        for device in devices[type]:
            if type == 'IOS':
                device_type = 'cisco_ios'
                ip = device
            elif type == 'NX-OS':
                device_type = 'cisco_nxos'
                ip = device                
            elif type == 'ASA':
                device_type = 'cisco_asa'
                ip = device                
            elif type == 'TELNET':
                device_type = 'cisco_ios_telnet'
                ip = device[0]
                telnetpassword = device[1]
                enablepass = device[2]

            if(type == 'TELNET'):
                connect_dict = {'device_type': device_type, 'ip': ip, 'username': username, 'password': telnetpassword, 'secret': enablepass}
            else:
                connect_dict = {'device_type': device_type, 'ip': ip, 'username': username, 'password': password}

            outputBox.insert(tk.END, f"\n\nConnecting to {ip}.....")
            root.update()
            print(f"Connecting to {ip}.....", end='', flush=True)
            try: 
                net_connect = ConnectHandler(**connect_dict)
                if(type == 'TELNET'):
                    net_connect.enable()
                    
            except NetMikoTimeoutException:
                timeouts.append(ip)
                outputBox.insert(tk.END, "\nSSH session timed trying to connect to the device: {}\n".format(ip))
                root.update()
                print("\nSSH session timed trying to connect to the device: {}\n".format(ip))
                continue
            except NetMikoAuthenticationException:
                authfailed.append(ip)
                outputBox.insert(tk.END, "\nSSH authentication failed for device: {}\n".format(ip))
                root.update()
                print("\nSSH authentication failed for device: {}\n".format(ip))                
                continue
            except ConnectionRefusedError:
                connectrefused.append(ip)
                outputBox.insert(tk.END, "\nConnection refused for device: {}\n".format(ip))
                root.update()
                print("\nConnection refused for device: {}\n".format(ip))
                continue
            except KeyboardInterrupt:
                outputBox.insert(tk.END, "\nUser interupted connection, closing program.\n")
                root.update()
                print("\nUser interupted connection, closing program.\n")
                sys.exit(0)
            except Exception:
                unknownerror.append(ip)
                outputBox.insert(tk.END, "\nUnknown error connecting to device: {}\n".format(ip))
                root.update()
                print("\nUnknown error connecting to device: {}\n".format(ip))
                continue

            output = net_connect.send_command("show run | inc hostname")
            if not output:
                filename = net_connect.send_command("show hostname").strip()
            else:
                filename = output[9:]

            filename = filename + '..' + \
            str(datetime.now().year) + '-' + \
            str(datetime.now().month) + '-' + \
            str(datetime.now().day) + '--' + \
            str(datetime.now().hour) + '-' + \
            str(datetime.now().minute) + '-' + \
            str(datetime.now().second) + '.log'
            
            successes.append( (ip , filename + ".log") )
            outputBox.insert(tk.END, "Success!\nOutput:\n")
            root.update()
            print("Success!\nOutput", flush=True)
            
            if configpath == '':
                if device_type == "cisco_nxos":
                    output = net_connect.send_config_set(COMMANDS)
                    outputBox.insert(tk.END, "\n" + output + "\n\n")
                    root.update()
                    print(output)
                else:
                    for command in COMMANDS:
                        outputBox.insert(tk.END, "\nRunning Command: {}\n\n".format(command))
                        root.update()
                        print("Running Command: {}\n".format(command), flush=True)
                        
                        output = net_connect.send_command(command)
                        
                        outputBox.insert(tk.END, output)
                        root.update()
                        print(output)
            else:
                try:
                    with open(configpath + "/" + filename, 'w') as fout:
                        if device_type == "cisco_nxos":
                            output = net_connect.send_config_set(COMMANDS)
                            print(output)
                            outputBox.insert(tk.END, output)
                            root.update()
                            fout.write(output)
                        else:
                            for command in COMMANDS:
                                outputBox.insert(tk.END, "\nRunning Command: {}\n\n".format(command))
                                root.update()                            
                                print("Running Command: {}\n".format(command), flush=True)
                                fout.write('\n\nRunning Command:\n' + command + '\n\n')

                                output = net_connect.send_command(command)

                                outputBox.insert(tk.END, output)
                                root.update()
                                print(output)
                                fout.write(output)
                except:
                    outputBox.insert(tk.END, "Invalid destination folder!\nContinuing....")
                    root.update()
                    print("Invalid destination folder!\nContinuing....")
                    
                    output = net_connect.send_config_set(COMMANDS)
                    
                    outputBox.insert(tk.END, output)
                    root.update()
                    print(output)
                    
    outputBox.insert(tk.END, "\n\n\nComplete! Check command prompt for stats.")
    root.update()
    
    print("\n\n\n\n\n\n")
    print("Devices timed out: ")
    for each in timeouts:
        print(each)
    print()
    print("Authentication failures:")
    for each in authfailed:
        print(each)
    print()
    print("Connection Refused:")
    for each in connectrefused:
        print(each)
    print()
    print("Unknown Error:")
    for each in unknownerror:
        print(each)
    print()
    print("Successful: ")
    for addr,fname in successes:
        print("{:15s} {:15s}".format(addr,fname))
    print()
    print("Time elapsed: {}".format(datetime.now() - start_time))

    return