from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
from netmiko.ssh_exception import NetMikoAuthenticationException
from datetime import datetime

with open('commands_file') as f:
    command_list = f.readlines()

with open('devices_file') as f:
    devices_list = f.readlines()

for devices in devices_list:
    ios_device = {
        'device_type': 'cisco_ios',
        'host': devices.strip(),
        'username': 'admin',
        'password': 'access123',
        'secret': 'access123'
    }

    try:
        print "**connecting to device: " + devices.strip()
        net_connect = ConnectHandler(**ios_device)
        net_connect.enable()


        for command in command_list:


            output = net_connect.send_command(command.strip())
            ## send config set
            print "\n\n ------ Start------\n\n"
            print "Command is:", command.strip()
            print output
            print "\n\n ------ END------\n\n"

            file = open('Host{} * {}-config.txt'.format(ios_device['host'], datetime.now().date()), 'a')
            file.write ("\n==============================================\n")
            file.write("Host {}".format(ios_device['host']))
            file.write("|| Date:{}".format(datetime.now().date()))
            file.write("\n==============================================\n")
            file.write("\n\n")
            file.write(output)
            file.close()

    except(NetMikoAuthenticationException):
        print "Authentication fail"+ devices.strip()
        continue

    except(NetMikoTimeoutException):
        print "Timeout" + devices.strip()
        continue

    except(EOFError):
        print "End of file:" + devices.strip()
        continue

    except(SSHException):
        print "SSH Issue" + devices.strip()
        continue

    except Exception as unknown_error:
        print "ASome other Error" + unknown_error
        continue
