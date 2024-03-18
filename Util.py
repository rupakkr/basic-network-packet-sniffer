import socket
import sys
from struct import *
import binascii

eth_length = 14 #Ethernet heade length 14bits

def createSocket():
        try:
            s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        except socket.error:
            print('Socket could not be created', socket.error)
            sys.exit()
        return s


#Method to convert the binary address to tuple of hex codes
def mac_addr(binary_addr):
    hex_addr = binascii.hexlify(binary_addr).decode('utf-8')
    formatted_hex_addr = ':'.join([hex_addr[i:i+2] for i in range(0, len(hex_addr), 2)])
    return formatted_hex_addr