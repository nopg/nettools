import jtextfsm
import yaml
import getpass
import sys
from netmiko import ConnectHandler
from netmiko.ssh_exception import *

def ly(filename):
    with open(filename) as _:
        return yaml.load(_)

def format_fsm_output(re_table, fsm_results):
    """
    FORMAT FSM OUTPUT(LIST OF LIST) INTO PYTHON LIST OF DICTIONARY VALUES BASED ON TEXTFSM TEMPLATE

    :param re_table: re_table from generic fsm search
    :param fsm_results: fsm results from generic fsm search
    :return result: updated list of dictionary values
    """
    result = []
    for item in fsm_results:
        tempdevice = {}
        for position, header in enumerate(re_table.header):
            tempdevice[header] = item[position]
        result.append(tempdevice)

    return result

def run_commands(username, password, switchfile, searchstring):

    print("Running, please wait...")
#   OPEN INPUT/OUTPUT FILES #
    devices = ly(switchfile)
    with open("./ap_ports-output.log", 'w') as fout:

    #   GRAB CDP NEIGHBORS #
        for type in devices:
            if type == 'IOS':
                for ip in devices[type]:
                    connect_dict = {'device_type': 'cisco_ios', 'ip': ip, 'username': username, 'password': password}

                    fout.write("\nSwitch: {}\n".format(ip))
                    fout.write("------------------------\n")

                    try:
                        net_connect = ConnectHandler(**connect_dict)
                    except NetMikoTimeoutException:
                        print("Unable to connect to {}".format(ip))
                        fout.write("\nUnable to connect (timeout) !\n\n\n\n")
                        continue
                    except NetMikoAuthenticationException:
                        print("Authentication error connecting to {}".format(ip))
                        fout.write("\nUnable to connect (authentication failure) !\n\n\n\n")
                        continue
                    except Exception:
                        print("Unknown error connecting to {}".format(ip))
                        continue

                    output = net_connect.send_command("show cdp neighbor detail")

                    template = open("cisco_ios_show_cdp_neighbors_detail.template")
                    re_table = jtextfsm.TextFSM(template)
                    fsm_results = re_table.ParseText(output)

            #   FORMAT OUTPUT
                    cdpneighbors = format_fsm_output(re_table, fsm_results)

                    print("\n-------------------------------")
                    fout.write("\n-----------------------------")

                    print("\nSwitch IP: {}".format(ip))
                    fout.write("\nSwitch IP: {}".format(ip))

            #   SEARCH FOR DEVICES AND PRINT/SAVE OUTPUT #
                    found = 0
                    for device in cdpneighbors:
                        if searchstring in device['PLATFORM']:
                            found += 1

                            print("\nConnected device: {} found on port: {}\n".format(device['DESTINATION_HOST'],
                                                                                           device['LOCAL_PORT']))
                            print("show run interface {}".format(device['LOCAL_PORT']))

                            fout.write("\nConnected device: {} found on port: {}\n".format(device['DESTINATION_HOST'], device['LOCAL_PORT']))
                            output = net_connect.send_command("show run interface {}".format(device['LOCAL_PORT']))
                            fout.write(output)
                            print(output)

                    print("\nFound {} devices matching \'{}\'\n\n\n\n".format(found, searchstring))
                    fout.write("\nFound {} devices matching \'{}\'\n\n\n\n".format(found, searchstring))

        
    print("\nFinished, output located in \'ap_ports-output.log\' file\n")

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("\nplease provide the following arguments:")
        print("\tpython3 ap_ports.py <device-file.yml> <cdp model search string> <username>\n\n")
        sys.exit(0)

    device_file = sys.argv[1]
    searchstring = sys.argv[2]
    username = sys.argv[3]

    password = getpass.getpass("Type the password: ")
    run_commands(username, password, device_file, searchstring)