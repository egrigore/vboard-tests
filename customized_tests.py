#python specific
from datetime import datetime

#project specific
import serial_communication

#requires pre-installation 
import pytest


#add prepare - initialize a serial port with valid values  and cleanup methods
#list of supported baudrate - static or dinamic?
#list of available ports - via dmesg


# basic functional tests

def test_help_command_01(open_valid_connection):
	#Check that help command finishes with success
	assert "PASS" in open_valid_connection.send_receive("cli_help")

def test_help_command_02(open_valid_connection, available_commands):
	#Check that help mentions all the available commands
	#available_commands = ["cli_read_time","cli_read_date","cli_read_date_time","cli_read_date_format","cli_write_date_format","cli_help"] 
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
	expected_date = str(datetime.now().date()) #the expected format is YYYY-MM-DD
	assert expected_date in open_valid_connection.send_receive("cli_read_date")

def test_cli_read_date_03(open_valid_connection):
	#check that for the int date format read_date returns the expected result: DD month YYYY
	pass

def test_cli_read_date_time_01(open_valid_connection):
	#check that command executes with success
	assert "PASS" in open_valid_connection.send_receive("cli_read_date_time")

def test_cli_read_date_time_02(open_valid_connection):
	#tbd check that command returns the expected value
	pass

def test_cli_read_date_format(open_valid_connection):
	assert "PASS" in open_valid_connection.send_receive("cli_read_date_format")	

# other scenarios

def test_date_format_persistency(open_valid_connection):
	#check that the value of date_format is persistent after the connection is closed
	open_valid_connection.send_receive("cli_write_date_format int")
	open_valid_connection.close()
	assert "int" == open_valid_connection.date_format


