import socket
from struct import *
from Util import eth_length



class Core:
    
    def __init__(self):
        pass

    def getHeaderInfo(self, s):
        raw_data = s.recvfrom(65565)
        self.packet = raw_data[0]
        ##eth_length = 14 #Ethernet heade length 14bits
        eth_header = self.packet[:eth_length]
        eth = unpack('!6s6sH', eth_header)
        mac_dest = self.packet[0:6]
        mac_src = self.packet[6:12]
        self.eth_protocol = socket.ntohs(eth[2])
        
        return self.packet,mac_dest, mac_src, self.eth_protocol
    
    def initiate(self):
        if self.eth_protocol == 8:
            # Parse IP header
            ip_header = self.packet[eth_length:20 + eth_length]
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
            
            protocol_handlers = {
                6: self.tcpProtocol,
                1: self.icmpProtocol,
                17: self.udpProtocol
            }
            
            protocol_handlers = protocol_handlers.get(protocol)
            protocol_handlers(iph_length)
             
        

            # # TCP protocol
            # if protocol == 6:
            #     self.tcpProtocol(iph_length)

            # # ICMP Packets
            # elif protocol == 1:
            #     self.icmpProtocol(iph_length)

            # # UDP packets
            # elif protocol == 17:
            #     self.udpProtocol(iph_length)

            # # some other IP packet
            # else:
            #     print('Protocol other than TCP/UDP/ICMP')
    
  
    def tcpProtocol(self, iph_length):
        t = iph_length + eth_length
        tcp_header = self.packet[t:t + 20]
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
        data_size = len(self.packet) - h_size

        # get data from the packet
        data = self.packet[h_size:]

        print('Data : ', data)
        
    def icmpProtocol(self, iph_length):
        u = iph_length + eth_length
        icmph_length = 4
        icmp_header = self.packet[u:u + 4]
        icmph = unpack('!BBH', icmp_header)

        icmp_type = icmph[0]
        code = icmph[1]
        checksum = icmph[2]

        print('Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum))

        h_size = eth_length + iph_length + icmph_length
        data_size = len(self.packet) - h_size

                # get data from the packet
        data = self.packet[h_size:]

        print('Data : ',data)
            
    def udpProtocol(self, iph_length):
        u = iph_length + eth_length
        udph_length = 8
        udp_header = self.packet[u:u + 8]
        udph = unpack('!HHHH', udp_header)

        source_port = udph[0]
        dest_port = udph[1]
        length = udph[2]
        checksum = udph[3]

        print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(
                    length) + ' Checksum : ' + str(checksum))

        h_size = eth_length + iph_length + udph_length
        data_size = len(self.packet) - h_size

        # get data from the packet
        data = self.packet[h_size:]

        print('Data : ', data)

    