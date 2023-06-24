import argparse
import re
import subprocess

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
      print("[-] Oops, An error occurred while changing the MAC address. Try again, but make sure you have root access before proceeding")
     

      
     

    


  

  
  
