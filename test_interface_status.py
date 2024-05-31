import pytest
from interface_status import get_interface_status
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_connection_handler():
    with patch('interface_status.ConnectHandler') as mock:
        yield mock

def test_get_interface_status_success(mock_connection_handler):
    mock_conn = MagicMock()
    mock_conn.send_command.return_value = "Interface status output"
    mock_connection_handler.return_value = mock_conn

    output = get_interface_status('sandbox-iosxr-1.cisco.com', 'admin', 'C1sco12345')

    assert output == "Interface status output"
    mock_connection_handler.assert_called_once_with(
        device_type='cisco_ios',
        ip='sandbox-iosxr-1.cisco.com',
        username='admin',
        password='C1sco12345'
    )
    mock_conn.send_command.assert_called_once_with("show ip interface brief")
    mock_conn.disconnect.assert_called_once()

def test_get_interface_status_failure(mock_connection_handler):
    mock_connection_handler.side_effect = Exception("Connection error")

    output = get_interface_status('sandbox-iosxr-1.cisco.com', 'admin', 'C1sco12345')

    assert output == "Connection error"
