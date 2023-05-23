# Python Test DNS Server

This project provides a simple DNS server written in Python. The server can be used for testing and development purposes. It forwards DNS requests to Google's DNS servers, receives the responses, and sends them back to the client.

## Dependency Installation ##

This server relies on some extra Python libraries, these can be installed via:

```commandline
pip install -r requirements.txt
```

## Usage ##

Run the server script from the command line as follows:

```commandline
sudo python3 dns_server.py
```

Remember that you need to run this script with sufficient privileges due to the use of port 53, a privileged port. On Unix-like systems (including Linux and macOS), use `sudo` to run the script as root. On Windows, open Command Prompt as an Administrator.

## Functionality ##

The server logs DNS request and response messages. For each DNS request, it logs the domain(s) being requested. For each DNS response, it logs the A records (IPv4 addresses) returned.

## AI Acknowledgement ##
Parts of this plugin were developed using ChatGPT and Github Copilot.

## License ##

2023 Matt Porritt <matt.porritt@moodle.com>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.

