import subprocess
import re
import argparse
import random
import schedule
import time

def current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode())
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print(f"[-] Couldn't get a MAC Address from {interface}")
    except subprocess.CalledProcessError:
        print(f"[-] An error occurred while getting the current MAC address of {interface}.")

def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC Address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC Address")
    parser.add_argument("-r", "--random", action="store_true", dest="random_mac", help="Set a random MAC Address")
    options = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help or -h for more information")
    elif not options.new_mac and not options.random_mac:
        parser.error("[-] Please specify either a new MAC address or use the random MAC option")

    return options

def change_mac(interface, new_mac):
    print(f"[+] Changing the MAC address for {interface} to {new_mac}")
    try:
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])
    except subprocess.CalledProcessError:
        print("[-] An error occurred while changing the MAC address.")

def generate_random_mac():
    return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])

options = get_argument()
if options.random_mac:
    options.new_mac = generate_random_mac()

current_mac_address = current_mac(options.interface)
if current_mac_address:
    print(f"[+] Current MAC Address = {current_mac_address}")

change_mac(options.interface, options.new_mac)
current_mac_address = current_mac(options.interface)
if current_mac_address and current_mac_address == options.new_mac:
    print(f"[+] MAC Address was changed successfully to {current_mac_address}")
else:
    print("[-] MAC address was not changed. Try again")

# Schedule the MAC address change every 5 minutes
schedule.every(5).minutes.do(change_mac, options.interface, options.new_mac)

while True:
    schedule.run_pending()
    time.sleep(5)


while True:
    schedule.run_pending()
    time.sleep(5)
