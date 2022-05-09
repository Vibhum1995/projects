# Author: Vibhum Chandorkar (vich1161@colorado.edu)
# Name: lab 9
# Purpose: Obj2
# Date: 4/8/2019
# version: 3

import csv
from ncclient import manager
import re
from prettytable import PrettyTable


# Making required configuration
configs = """
     <config>
		<cli-config-data>
            <cmd>hostname %s</cmd>
			<cmd>interface loopback 99</cmd>
			<cmd>ip address %s </cmd>
			<cmd>no shutdown</cmd>
			<cmd>router ospf 1</cmd>
			<cmd>network %s area %s </cmd>
			<cmd>wr</cmd>
		</cli-config-data>
	</config>

"""


# MAking list
list=[]

# Openeing the config file and reading the file from line 2
with open('obj2-conf.txt') as f:
    contents = (f.readlines())[1:6]
    for content in contents:
	
	# Splitting the contents by space and assigning each individual variable resp value
        new_contents = content.split()
        #print(new_contents)
        router = new_contents[0]
        hostname = new_contents[1]
        loopback = new_contents[2]

	
        if (loopback.split('/'))[1] == '24':
            loopback = (loopback.split('/'))[0] + ' 255.255.255.0'
        ospf_area = new_contents[3]
        network = new_contents[4]
        if (network.split('/'))[1] == '24':
            network = (network.split('/'))[0] + ' 0.0.0.255'


	# Putting the values in the config format
        config_format = configs % (hostname, loopback, network, ospf_area)


	# Opening CSV file containg router ssh configuration 
        file = open('router.csv')
        reader = csv.DictReader(file)
        for row in reader:
            Router = row['Router']
            Username = row['Username']
            Password = row['Password']
            IP = row['IP']
		# Connecting using ncclient manager if the Router match router i.e (R1,R2 etc)
            if Router == router:
                try:
                    m = manager.connect(host=IP, port=22,
                                         username=Username,
                                         password=Password, hostkey_verify=False,
                                         allow_agent=False, look_for_keys=False, timeout=20)
			# Editng the configurations
                    final_data_config = m.edit_config(target='running', config=config_format)
                    print(final_data_config)
                except:
                    pass
                

configs1=[]
configs2=[]
configs3=[]
configs4=[]
configs5=[]

# Again reading from the csv file and taking router ssh configs
file = open('router.csv')
reader = csv.DictReader(file)

for row in reader:

	Router = row['Router']
	Username = row['Username']
	Password = row['Password']
	IP = row['IP']
	
	# Getting the config through ncclient manager
	m1 = manager.connect(host=IP, port=22, username=Username, password=Password, device_params={'name':'csr'}, hostkey_verify=False, timeout=20)
	
	# Storing the running config output in output_config 
	output_config = m1.get_config(source='running')
	output = str(output_config)
	

	# Using regex to parse the required values and puting the in the above created lists
	new_hostname = (re.findall(r'hostname (.*)?', output))
	a=new_hostname[0].strip('\r')
	configs1.append(a)
	
	new_network_list = re.findall(r'network(.*)?', output)
	new_network = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', new_network_list[0])
	ospf_network = new_network[0]+' '+new_network[1]
	configs2.append(ospf_network)	

	new_ip = (re.findall(r'ip address (.*)?', output))
	b=new_ip[0].strip('\r')
	configs3.append(b)	

	new_area = (re.findall(r'area (.*)?', output))
	c=new_area[0].strip('\r')
	configs4.append(c)

# Pritnting the output in pretty table
x= PrettyTable()
x.add_column("Hostname", configs1)
x.add_column("Ospf Network", configs2)
x.add_column("Loopback IP", configs3)
x.add_column("Ospf Area", configs4)	
print(x)




