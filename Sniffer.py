from Core import Core
from Util import mac_addr,createSocket,eth_length
# from tabulate import tabulate


# Create an instance of the Core class
core_instance = Core()

#Create socket
soc = createSocket()


while True:
    
    packet, mac_dest, mac_src, eth_protocol = core_instance.getHeaderInfo(soc)

    print('Destination MAC : ' + mac_addr(mac_dest) + ' Source MAC : ' + mac_addr(mac_src) + ' Protocol : ' + str(eth_protocol))
    
    # Prepare the data for the table
    # table_data = [
    #     ["Destination MAC", "Source MAC", "Ethernet Protocol", "packet"],
    #     [mac_addr(mac_dest), mac_addr(mac_src) , str(eth_protocol), str(packet)]
    # ]

    # Print the table
    # print(tabulate(table_data, headers="firstrow"))
    
    core_instance.initiate()