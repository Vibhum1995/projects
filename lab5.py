# Name: Vibhum Chandorkar (vich1161@colorado.edu)
# Objective: LAb5 Objective (a,b,c,d,e)
# Version: 3.7

from netmiko import ConnectHandler
import re
import time


cisco = {
    'device_type': 'cisco_ios',
    'ip': '192.168.100.1',
    'username': 'tony',
    'password': 'stark',
}
connect_r1 = ConnectHandler(**cisco)

# Objective a
# Getting the IP assigned to Mininet VM
output = connect_r1.send_command("show ip dhcp binding | include 0800.2763.c492")
vm_ip = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", output)
print('The IP assigned to VM is {}'.format(vm_ip[0]))
connect_r1.disconnect()

print('\n')

# Objective b
# Initializaing minimal topology on mininet
linux = {
    'device_type': 'linux',
    'ip': vm_ip[0],
    'username': 'mininet',
    'password': 'mininet',
}

connect_linux = ConnectHandler(**linux)
#connect_linux2 = ConnectHandler(**linux)
mininet_cmd = connect_linux.send_command_timing('sudo mn')
mininet_cmd2 = connect_linux.send_command_timing('mininet')
print(mininet_cmd2)
print("\n")

# Objective c
# Setting the bridge and controller configuration and finding the assigned IP
mininet_cmd3 = connect_linux.send_command_timing("sh ovs-vsctl set-controller s1 tcp:10.20.30.2:6633")
mininet_cmd6 = connect_linux.send_command_timing('sh ovs-vsctl set bridge s1 protocols=OpenFlow13')
mininet_cmd7 = connect_linux.send_command_timing("sh ovs-vsctl get-controller s1")
#print(mininet_cmd7)

controller_ip = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", mininet_cmd7)
print(controller_ip)
print('The controller IP is {}'.format(controller_ip[0]))

# Objective d
# Setting OSPF protocl on router from sshing one to another for OpenFlow Connectivity
R1 = ['router ospf 1', 'network 192.168.100.0 0.0.0.255 area 0', 'network 192.168.200.0 0.0.0.255 area 0']
R2 = ['config t', 'router ospf 1', 'network 192.168.200.0 0.0.0.255 area 0', 'network 172.16.100.0 0.0.0.255 area 0']
R3 = ['config t', 'router ospf 1', 'network 10.20.30.0 0.0.0.255 area 0', 'network 172.16.100.0 0.0.0.255 area 0']
router_IP = ['192.168.200.2', '172.16.100.1']
Routers = [['config t', 'router ospf 1', 'network 192.168.200.0 0.0.0.255 area 0', 'network 172.16.100.0 0.0.0.255 area 0'], ['config t', 'router ospf 1', 'network 10.20.30.0 0.0.0.255 area 0', 'network 172.16.100.0 0.0.0.255 area 0']]
count = 2
connect_router = ConnectHandler(**cisco)
initial_cmd = connect_router.send_config_set(R1)

run_config = connect_router.send_command("show run | section ospf")
print("Following are the router R1 ospf config")
print(run_config)
print('\n')
time.sleep(10)

for ip in range(len(router_IP)):
    current_router = 'R'+ str(count)
    ssh_cmd = "ssh -l tony " + router_IP[ip]
    command1 = connect_router.send_command_timing(ssh_cmd)
    command2 = connect_router.send_command_timing("stark")
    print('Following is the ospf config of router {}'.format(current_router))
    for i in Routers[ip]:
        command3 = connect_router.send_command_timing(i)

    command5 = connect_router.send_command_timing("exit")
    command6 = connect_router.send_command_timing("exit")
    command4 = connect_router.send_command_timing("show run | section ospf")
    print(command4)
    count = count + 1
    print('\n')

# Objective e
# Checking Openflow connectivity between controller and the OVS in mininet
connect_linux3 = ConnectHandler(**linux)
#ping_cmd = "ping -c 5 "+ controller_ip[0]
mininet_cmd8 = connect_linux.send_command_timing("pingall")
print(mininet_cmd8)





