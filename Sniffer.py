import socket
import sys
from struct import *
import binascii


def mac_addr(binary_addr):
    hex_addr = binascii.hexlify(binary_addr).decode('utf-8')
    formatted_hex_addr = ':'.join([hex_addr[i:i+2] for i in range(0, len(hex_addr), 2)])
    return formatted_hex_addr


try:
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
except socket.error:
    print('Socket could not be created', socket.error)
    sys.exit()


while True:
    raw_data = s.recvfrom(65565)
    packet = raw_data[0]
    eth_length = 14 #Ethernet heade length 14bits
    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])

    print('Destination MAC : ' + mac_addr(packet[0:6]) + ' Source MAC : ' + mac_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol))
    
    if eth_protocol == 8:
        # Parse IP header
        ip_header = packet[eth_length:20 + eth_length]
        iph = unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = iph[0] 
        version = version_ihl >> 4
        ihl = version_ihl & 0xF

        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])

        print('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(
            ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(
            d_addr))

        # TCP protocol
        if protocol == 6:
            t = iph_length + eth_length
            tcp_header = packet[t:t + 20]
            tcph = unpack('!HHLLBBHHH', tcp_header)

            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4

            print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(
                sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length))

            h_size = eth_length + iph_length + tcph_length * 4
            data_size = len(packet) - h_size

            # get data from the packet
            data = packet[h_size:]

            print('Data : ', data)

        # ICMP Packets
        elif protocol == 1:
            u = iph_length + eth_length
            icmph_length = 4
            icmp_header = packet[u:u + 4]
            icmph = unpack('!BBH', icmp_header)

            icmp_type = icmph[0]
            code = icmph[1]
            checksum = icmph[2]

            print('Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum))

            h_size = eth_length + iph_length + icmph_length
            data_size = len(packet) - h_size

            # get data from the packet
            data = packet[h_size:]

            print('Data : ',data)

        # UDP packets
        elif protocol == 17:
            u = iph_length + eth_length
            udph_length = 8
            udp_header = packet[u:u + 8]
            udph = unpack('!HHHH', udp_header)

            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]

            print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(
                length) + ' Checksum : ' + str(checksum))

            h_size = eth_length + iph_length + udph_length
            data_size = len(packet) - h_size

            # get data from the packet
            data = packet[h_size:]

            print('Data : ', data)

        # some other IP packet
        else:
            print('Protocol other than TCP/UDP/ICMP')
