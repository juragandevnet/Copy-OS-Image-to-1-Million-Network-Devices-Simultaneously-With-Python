### IT'S CREATED BY JURAGAN DEVNET ###

import getpass
from netmiko import ConnectHandler 
from threading import Thread
from time import strftime,gmtime
from tqdm import tqdm

def CopyImage(device_type, username, password, ip_address):
    SshCopy = {
        'device_type' : device_type,
        'ip' : ip_address,
        'username': username,
        'password': password 
    }
    time = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    try:
        net_connect = ConnectHandler(**SshCopy)
        output_hostname = net_connect.send_command('show run | i hostname')
        output_flash = net_connect.send_command('dir bootflash: | i TestImage.bin')
        if "TestImage.bin" not in output_flash:
            output = net_connect.send_command_timing('copy tftp://10.66.49.215:/TestImage.bin bootflash:/TestImage.bin')
            for progress_bar in tqdm(range(len(output)), desc = output_hostname):
                output = net_connect.send_command('\n', expect_string=r'.', read_timeout=3600)
            print("Image has been uploaded for " + output_hostname + ' in '+ time)
            net_connect.disconnect()
        else:
            print(output_hostname)
            print(output_flash)
            print("Image TestImage.bin Does Exist")
    except Exception:
        print("Check your Network Connection, make sure you can SSH to", ip_address)

### CREDENTIALS ###
username = input("username: ")
password = getpass.getpass()

### READ FILE ###
f = open('devices.txt','r')  

### RUNNING thread ###
threads=[]
threads = [Thread(target=CopyImage, args=('cisco_ios', username, password, ip_address)) for ip_address in f.readlines()]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

