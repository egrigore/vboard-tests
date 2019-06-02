#project specific
import serial_communication

#requires pre-installation 
import pytest


#negative functional tests
def test_already_open(open_valid_connection):
        #Check that an exception is raised if the port is already opened
        with pytest.raises(Exception):
                open_valid_connection.open()


def test_already_closed(open_valid_connection_wo_close):
        #Check that an exception is raised if the port is already closed
        open_valid_connection_wo_close.close()
        with pytest.raises(Exception):
                open_valid_connection_wo_close.close()

def test_command_before_open():
        #check that an exception is raised if a command is triggered before port was opened
        serial = serial_communication.SerialCommunication(0,115200)
        with pytest.raises(Exception):
                serial.send_receive("cli_read_time")

def test_command_after_close(open_valid_connection_wo_close):
        #check that an exception is raised if a command is triggered after port was closed
        open_valid_connection_wo_close.close()
        with pytest.raises(Exception):
                open_valid_connection_wo_close.send_receive("cli_help")

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
#TBD - read date and read date time for invalid date_format

