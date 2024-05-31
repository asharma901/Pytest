import pytest
from unittest.mock import patch, MagicMock
from ios_xr_lo_config import read_device_list, read_credentials, check_and_configure_loopback

# Sample data for testing
sample_device_list = ["sandbox-iosxr-1.cisco.com"]
sample_credentials = ("admin", "C1sco12345")

# Mock data for the device response
mock_show_running_config_output = """
interface Loopback50
interface Loopback51
interface Loopback52
interface Loopback53
interface Loopback54
interface Loopback55
interface Loopback56
interface Loopback57
interface Loopback58
interface Loopback59
interface Loopback60
"""

@pytest.fixture
def mock_read_device_list():
    with patch('ios_xr_lo_config.read_device_list', return_value=sample_device_list):
        yield

@pytest.fixture
def mock_read_credentials():
    with patch('ios_xr_lo_config.read_credentials', return_value=sample_credentials):
        yield

@pytest.fixture
def mock_connect_handler():
    with patch('ios_xr_lo_config.ConnectHandler') as MockConnectHandler:
        instance = MockConnectHandler.return_value
        instance.send_command.side_effect = lambda command: mock_show_running_config_output if "show running-config interface" in command else ""
        instance.send_config_set.return_value = "Config set"
        instance.send_command.side_effect = ["show running-config interface | include ^interface Loopback", "commit"]
        yield MockConnectHandler

def test_read_device_list(mock_read_device_list):
    devices = read_device_list(r"C:\Users\AbhishekSharma\Pictures\Miss_file_python\device_list.txt")
    assert devices == sample_device_list

def test_read_credentials(mock_read_credentials):
    username, password = read_credentials(r"C:\Users\AbhishekSharma\Pictures\Miss_file_python\device_cred.txt")
    assert username == sample_credentials[0]
    assert password == sample_credentials[1]

def test_check_and_configure_loopback(mock_connect_handler, mock_read_device_list, mock_read_credentials):
    device_info = {
        "device_type": "cisco_xr",
        "ip": sample_device_list[0],
        "username": sample_credentials[0],
        "password": sample_credentials[1],
        "port": 22
    }
    check_and_configure_loopback(device_info)
    mock_connect_handler.assert_called_once_with(**device_info)
    instance = mock_connect_handler.return_value
    instance.send_command.assert_any_call("show running-config interface | include ^interface Loopback")
    instance.send_command.assert_any_call("commit")
    instance.disconnect.assert_called_once()

if __name__ == "__main__":
    pytest.main()
