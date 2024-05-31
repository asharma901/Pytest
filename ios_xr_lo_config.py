from netmiko import ConnectHandler
import re


# Function to read device list from a file
def read_device_list(file_path):
    with open(file_path) as file:
        return file.read().splitlines()


# Function to read credentials from a file
def read_credentials(file_path):
    with open(file_path) as file:
        creds = file.read().splitlines()
        return creds[0], creds[1]


# Function to check and configure loopback interfaces
def check_and_configure_loopback(device_info):
    try:
        ssh = ConnectHandler(**device_info)
        print(f"^^^^^ Connecting to {device_info['ip']}")

        # Check existing loopback interfaces
        output = ssh.send_command("show running-config interface | include ^interface Loopback")
        existing_loopbacks = re.findall(r"Loopback(\d+)", output)
        existing_loopbacks = [int(loop) for loop in existing_loopbacks]
        print(f"Existing Loopbacks: {existing_loopbacks}")

        # Prepare configuration commands for missing loopbacks
        loopback_configs = []
        for i in range(50, 61):
            if i not in existing_loopbacks:
                ip_address = f"{i}.{i}.{i}.{i}"
                loopback_configs.append(f"interface Loopback{i}")
                loopback_configs.append(f"ipv4 address {ip_address}/32")
                loopback_configs.append("exit")

        # Send configuration commands if there are any missing loopbacks
        if loopback_configs:
            cli_out = ssh.send_config_set(loopback_configs)
            print(cli_out)
            ssh.send_command("commit")
            print(f"Configuration committed on {device_info['ip']}")
        else:
            print("All Loopbacks from 50 to 60 are already configured.")

        ssh.disconnect()
        print(f"^^^^^ Disconnected from {device_info['ip']}")
    except Exception as e:
        print(f"An error occurred on {device_info['ip']}: {str(e)}")


# Main function
def main():
    # File paths
    device_list_file = r"C:\Users\AbhishekSharma\Pictures\Miss_file_python\device_list.txt"
    credential_file = r"C:\Users\AbhishekSharma\Pictures\Miss_file_python\device_cred.txt"

    # Read device list and credentials
    device_list = read_device_list(device_list_file)
    username, password = read_credentials(credential_file)

    # Iterate over each device and perform the check and configuration
    for device_ip in device_list:
        device_info = {
            "device_type": "cisco_xr",
            "ip": device_ip,
            "username": username,
            "password": password,
            "port": 22
        }
        check_and_configure_loopback(device_info)


if __name__ == "__main__":
    main()
