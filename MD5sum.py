### IT'S CREATED BY JURAGAN DEVNET ###

import getpass
from netmiko import ConnectHandler 
from threading import Thread
from time import strftime,gmtime
from tqdm import tqdm

def upload(device_type, username, password, ip_address,Md5_Number):
    SshMd5 = {
        'device_type' : device_type,
        'ip' : ip_address,
        'username': username,
        'password': password 
    }
    time = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    try:
        net_connect = ConnectHandler(**SshMd5)
        output_hostname = net_connect.send_command('show run | i hostname')
        output_flash = net_connect.send_command('dir bootflash: | i TestImage.bin')
        output_md5 = net_connect.send_command_timing('verify /md5 bootflash:/TestImage.bin')
        for progress_bar in tqdm(range(len(output_md5)), desc=output_hostname, leave=False ):
            output_md5 += net_connect.send_command('\n', expect_string=r'.', read_timeout=3600)
        print(output_hostname + ' | Task Completed in ', time)
        if output_flash:
            print(' ' + output_flash)
            if Md5_Number in output_md5:
                print(" MD5 Checksum Completed your MD5 number is ", Md5_Number)
            else:
                print(" Error, the OS is corrupted")
        else:
            print(" OS Does Not Exist")
        net_connect.disconnect()
    except Exception:
        print("Check your Network Connection, make sure you can SSH to", ip_address)

### MD5 Number ###
Md5_Number = '4da060594ce9759704e48d9a0319011a'

## READ FILE ###
f = open('devices.txt','r')  

username = input("username: ")
password = getpass.getpass()
print("\n")

threads=[]
threads = [Thread(target=upload, args=('cisco_ios', username, password, ip_address, Md5_Number)) for ip_address in f.readlines()]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
