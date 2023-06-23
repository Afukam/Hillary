import argparse
import re
import subprocess

def get_arguement():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--interface",dest="interface",help="Interface to change MAC address")
  parser.add_argument("-m", "--mac",dest="new_mac",help="New Mac Address")
  
  
