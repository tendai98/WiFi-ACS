# WiFi Access Control Control using Deauth frames

## Overview

This project serves as an experimental Layer 2 firewall designed to enhance the security of a WiFi network by blocking unauthorized or unwanted devices using Deauthentication (Deauth) frames. It operates on a standalone computer, such as a Raspberry Pi, and leverages Scapy and Python to monitor devices on a target network based on their MAC addresses. Unauthorized devices are identified and blocked by sending Deauth frames to unwanted devices.

## Features

- **Device Monitoring**: Continuously scans the target WiFi network for active devices and their MAC addresses.

- **Custom Database Integration**: Maintains a database of authorized MAC addresses to identify devices that are allowed to connect to the network.

- **Automatic Blocking**: Detects unauthorized devices and sends Deauth frames to disconnect them from the network.

- **Customizable Policies**: Allows administrators to define access policies and authorized MAC addresses for the network.

## Hardware and Software Requirements

### Hardware:
- A standalone computer (e.g., Raspberry Pi) running a Linux-based operating system.
- A WiFi adapter that supports monitor mode for capturing network traffic.

### Software:
- Python 3.x installed on the computer.
- Scapy, a powerful packet manipulation library for Python.
- Access to the target WiFi network.

## Getting Started

To set up and use the Layer 2 Firewall with Deauth Frames, follow these steps:

1. Clone this repository or download the project files to your standalone computer (e.g., Raspberry Pi).

   ```bash
   git clone https://github.com/tendai98/WiFi-ACS.git
   ```

2. Install the required Python libraries, including Scapy, on your computer.

   ```bash
   pip install scapy
   ```

3. Configure the firewall by editing the database of authorized MAC addresses and any access policies you wish to enforce.

4. Run the Python script on your computer to start monitoring the target WiFi network.

   ```bash
   python nodd
   ```

5. The firewall will continuously monitor the network, identify unauthorized devices, and send Deauth frames to block them.

6. You can access logs and reports for analysis and review in real-time.

## Usage

1. **Database Configuration**: Maintain a list of authorized MAC addresses in the database, specifying which devices are allowed to connect to the network.

2. **Access Policies**: Define and customize access policies, such as how to handle unauthorized devices.

3. **Unauthorized Device Detection**: When an unauthorized device is detected, the firewall will send Deauth frames to disconnect it.

## Disclaimer

This project is intended for educational and security research purposes. Ensure you have the necessary permissions and comply with local laws and regulations when using this tool. Unauthorized access to or disruption of networks may be illegal and unethical.

