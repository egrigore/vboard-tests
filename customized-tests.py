#python specific
from datetime import datetime

#project specific
import serial_communication

#requires pre-installation 
import pytest


#add prepare - initialize a serial port with valid values  and cleanup methods
#list of supported baudrate - static or dinamic?
#list of available ports - via dmesg

@pytest.fixture
def open_valid_connection():
        serial = serial_communication.SerialCommunication(0,115200)
        serial.open()
	return serial 


#negative functional tests
def test_already_open(open_valid_connection):
	#Check that an exception is raised if the port is already opened
	with pytest.raises(Exception):
		open_valid_connection.open()

def test_already_closed(open_valid_connection):
	#Check that an exception is raised if the port is already closed
	open_valid_connection.close()
        with pytest.raises(Exception):
		open_valid_connection.close()

def test_command_before_open():
	#check that an exception is raised if a command is triggered before port was opened
	serial = serial_communication.SerialCommunication(0,115200)
	with pytest.raises(Exception):
		serial.send_receive("cli_read_time")

def test_command_after_close(open_valid_connection):
	#check that an exception is raised if a command is triggered after port was closed
	open_valid_connection.close()
        with pytest.raises(Exception):
		open_valid_connection.send_receive("cli_help")

def test_inexistent_command_01(open_valid_connection):
	#Check that the help menu is returned if the command is wrong
	serial = open_valid_connection
	assert (serial.send_receive("cli_help") in serial.send_receive("no_command"))

def test_inexistent_command_02(open_valid_connection):
	#Check that an unknown command explanation is returned
	assert ("Unknown command" in open_valid_connection.send_receive("no_command"))

def test_inexistent_port():
	#Check that an Error is raised if the port doesn't exists - emulated virtual device is not in connected state
	#TBD find out an inexistent port - ls /dev/tty* - assuming for now that 9999 doesn't exist
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


# basic functional tests

def test_help_command_01(open_valid_connection):
	#Check that help command finishes with success
	assert "PASS" in open_valid_connection.send_receive("cli_help")

def test_help_command_02(open_valid_connection):
	#Check that help mentions all the available commands
	available_commands = ["cli_read_time","cli_read_date","cli_read_date_time","cli_read_date_format","cli_write_date_format","cli_help"] 
	assert all(command in open_valid_connection.send_receive("cli_help") for command in available_commands)

def test_cli_read_time_01(open_valid_connection):
	#Check that read time command finishes with success
        assert "PASS" in open_valid_connection.send_receive("cli_read_time")

def test_cli_read_time_02(open_valid_connection):
	#Check that read time command returns the expected output- assuming last 3 digits as being the margin of error
	expected_time = str(datetime.now().time())[:-3]
	received_time = open_valid_connection.send_receive("cli_read_time")
	assert expected_time in received_time

def test_cli_read_date_01(open_valid_connection):
	assert "PASS" in open_valid_connection.send_receive("cli_read_date")

def test_cli_read_date_02(open_valid_connection):
	# since the object is newly instantiated date_format is usa as default
	expected_date = str(datetime.now().date())
	assert expected_date in open_valid_connection.send_receive("cli_read_date")

def test_cli_read_date_03(open_valid_connection):
	#check that for the int date format read_date returns the expected result: DD:MM:YYYY
	pass

def test_cli_read_date_time_01(open_valid_connection):
	#check that command executes with success
	assert "PASS" in open_valid_connection.send_receive("cli_read_date_time")
#tbd check that command returns the expected value

def test_cli_read_date_format(open_valid_connection):
	assert "PASS" in open_valid_connection.send_receive("cli_read_date_format")	

# other scenarios

def test_date_format_persistency(open_valid_connection):
	#check that the value of date_format is persistent after the connection is closed
	open_valid_connection.send_receive("cli_write_date_format int")
	open_valid_connection.close()
	assert "int" == open_valid_connection.date_format


