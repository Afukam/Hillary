import argparse
import re
import subprocess
import schedule
import time



def get_arguement():
   parser = argparse.ArgumentParser()
   parser.add_argument("-i", "--interface",dest="interface",help="Interface to change MAC address")
   parser.add_argument("-m", "--mac",dest="new_mac",help="New Mac Address")
   options = parser.parse_args()

  
   if not options.interface:
      parser.error("[-]Interface input error, please use -h or --help for more options")
   elif not options.new_mac:
      parser.error("[-]New Mac not identified, please use -h or --help for more options")
    
   return options


def mac_change(interface, new_mac):
   print(f"[+]Changing the MAC address for {interface} to {new_mac} , feel free to grab a coffee or tea, while the change is in progress")
   try:
      subprocess.call(["ifconfig", interface, "down"])
      subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
      subprocess.call(["ifconfig", interface, "up"])
   except subprocess.CalledProcessError as e:
      print("[-] Oops, An error occurred while changing the MAC address. Try again, but make sure you have root access before proceeding.")


def current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode())
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print(f"[-] Couldn't get a MAC Address from {interface}")
    except subprocess.CalledProcessError as e:
        print(f"[-] An error occurred while getting the current MAC address of {interface}.")

options = get_argument()
current_mac_address = current_mac(options.interface)
if current_mac_address:
   print(f"[+] Current MAC Address = {current_mac_address}")


change_mac(options.interface, options.new_mac)
current_mac_address = current_mac(options.interface)
if current_mac_address and current_mac_address == options.new_mac:
   print(f"[+] MAC Address was changed successfully to {current_mac_address}")
else:
   print("[-] MAC address was not changed. Try again")


schedule.every(5).minutes.do(mac_change)

while True:
   schedule.run_pending()
   time.sleep(5)
else:
   print("[-] Process terminated. Try again")

   
   
      
     

      
     

    


  

  
  
