from netmiko import ConnectHandler

def get_interface_status(ip, username, password, device_type='cisco_ios'):
    device = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
    }
    try:
        connection = ConnectHandler(**device)
        output = connection.send_command("show ip interface brief")
        connection.disconnect()
        return output
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    ip = 'sandbox-iosxr-1.cisco.com'
    username = 'admin'
    password = 'C1sco12345'
    print(get_interface_status(ip, username, password))
