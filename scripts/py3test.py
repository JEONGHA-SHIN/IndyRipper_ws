#!/usr/bin/env python3

from indydcp_client import IndyDCPClient

bind_ip = "192.168.0.14"    
server_ip = "10.82.10.62"  
robot_name = "NRMK-Indy7" 
indy = IndyDCPClient(bind_ip, server_ip, robot_name) 


indy.connect()
print(indy.is_connected())

if indy.is_connected():
	indy.go_zero()
else:
	indy.reset.robot()


