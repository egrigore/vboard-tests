import pytest
import serial_communication

@pytest.fixture
def open_valid_connection():
        serial = serial_communication.SerialCommunication(0,115200)
        serial.open()
        yield serial
	serial.close()

@pytest.fixture
def open_valid_connection_wo_close():
        serial = serial_communication.SerialCommunication(0,115200)
        serial.open()
        return serial


@pytest.fixture
def available_commands():
	commands = ["cli_read_time","cli_read_date","cli_read_date_time","cli_read_date_format","cli_write_date_format","cli_help"]
	return commands
