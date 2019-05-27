import serial_communication
import pytest


#add prepare - initialize a serial port with valid values  and cleanup methods
#list of supported baudrate - static or dinamic?
#list of available ports - via dmesg

@pytest.fixture
def open_valid_connection():
        serial = serial_communication.SerialCommunication(0,115200)
        serial.open()
	return serial 


#negative tests
def test_already_open(open_valid_connection):
	#Check that an exception is raised if the port is already opened
	with pytest.raises(Exception):
		open_valid_connection.open()

def test_inexistent_command_01(open_valid_connection):
	#Check that the help menu is returned if the command is wrong
	serial = open_valid_connection
	assert (serial.send_receive("cli_help") in serial.send_receive("no_command"))

def test_inexistent_command_02(open_valid_connection):
	#Check that an unknown command explanation is returned
	assert ("Unknown command" in open_valid_connection.send_receive("no_command"))

def test_inexistent_port():
	#Check that an Error is raised if the port doesn't exists - emulated virtual device is not in connected state
	#TBD find out an inexistent port - ls /dev/tty*
	port = 9999
	with pytest.raises(Exception):
		 serial_communication.SerialCommunication(port,115200)

def test_invalid_port():
	#Check that an Error is raised if the port is invalid - string instead of integer
	with pytest.raises(Exception):
		serial_communication.SerialCommunication("this_should_be_integer",115200)

def test_inexistent_baudrate():
	pass

def test_invalid_baudrate():
	#Check that an Error is raised if the baudrate is not integer
	with pytest.raises(Exception):
		serial_communication.SerialCommunication(5,"this_should_be_integer")

#functional tests

def test_help_command(open_valid_connection):
	assert "PASS" in open_valid_connection.send_receive("cli_help")

def test_cli_read_time(open_valid_connection):
        assert "PASS" in open_valid_connection.send_receive("cli_read_time")

def test_cli_read_date(open_valid_connection):
	assert "PASS" in open_valid_connection.send_receive("cli_read_date")

def test_cli_read_date_time_01(open_valid_connection):
	#check that command executes with success
	assert "PASS" in open_valid_connection.send_receive("cli_read_date_time")
#tbd check that command returns the expected value

def test_cli_read_date_format(open_valid_connection):
	assert "PASS" in open_valid_connection.send_receive("cli_read_date_format")	
