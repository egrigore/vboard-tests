#project specific
import serial_communication

#requires pre-installation 
import pytest


def test_multiple_connection_on_same_port():
	#test that at least 64k connections are allowed on the same port at the same baudrate
	for i in range(64000):
		i =  serial_communication.SerialCommunication(5,115200)
		i.open()
	assert "PASS" in i.send_receive("cli_help")

def test_multiple_ports():
	#Test that the maximum number of ports is unlimited 
	#Check that no files/folders is created for each new port - assume linux - use df -i to find the number of available nodes and set that one as maxim
	#TBD
	pass

def test_multiple_commands_on_the_same_connection():
	#TBD
	pass

def test_parallel_commands_on_the_same_connection():
	#TBD trigger in the same time a read_date and a close operation over the same conenction
	pass
