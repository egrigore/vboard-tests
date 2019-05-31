#python specific
from datetime import datetime

#project specific
import serial_communication

#requires pre-installation 
import pytest


def test_write_date_format_no_param(open_valid_connection):
	#operation should fail if no parameter is given to write_date_format command
        assert "FAIL" in open_valid_connection.send_receive("cli_write_date_format")

def test_write_date_format_wrong_param(open_valid_connection):
        #operation should fail if wrong parameter is given to write_date_format command
        assert "FAIL" in open_valid_connection.send_receive("cli_write_date_format 5")

def test_write_date_format_twice_param(open_valid_connection):
        #operation should fail if wrong parameter is given to write_date_format command
        assert "FAIL" in open_valid_connection.send_receive("cli_write_date_format intint")

def test_read_time_invalid_date_format(open_valid_connection):
	#check that read time command is not affected by date_format
	open_valid_connection.date_format = ""
	assert str(datetime.now().time())[:-3] in open_valid_connection.send_receive("cli_read_time").split("\n")[0]

def test_read_date_invalid_date_format(open_valid_connection):
	#check that read date command triggers an error when date_format is invalid - or should it return the values for the default date_format?
	open_valid_connection.date_format = ""
	with pytest.raises(Exception):
		open_valid_connection.send_receive("cli_read_date")


def test_write_date_format_over_invalid(open_valid_connection):
	#check that write_date_format can ovewrite an invalid value
	open_valid_connection.date_format = "This is an invalid value for d@t3f0rm2t"
	open_valid_connection.send_receive("cli_write_date_format int")
	assert "int" == open_valid_connection.date_format
