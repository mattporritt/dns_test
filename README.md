# Python Test DNS Server

This project provides a simple DNS server written in Python. The server can be used for testing and development purposes. It forwards DNS requests to Google's DNS servers, receives the responses, and sends them back to the client.

## Setup and Usage ##

This server relies on some extra Python libraries, these can be installed via:

```commandline
pip install -r requirements.txt
```

Modify the `config.yaml` file to define the specific domains and their DNS behaviors. See behaviors section below.

Run the server script from the command line as follows:

```commandline
sudo python3 dns_server.py
```

Remember that you need to run this script with sufficient privileges due to the use of port 53, a privileged port. On Unix-like systems (including Linux and macOS), use `sudo` to run the script as root. On Windows, open Command Prompt as an Administrator.

To test the DNS server, you can use nslookup:

```commandline
nslookup example.com 127.0.0.1
```

## Functionality ##

The server logs DNS request and response messages. For each DNS request, it logs the domain(s) being requested. For each DNS response, it logs the A records (IPv4 addresses) returned.

It is a tool for testing DNS behaviors. This server allows you to define specific domains and dictate how they should respond to DNS requests. 

The behaviors currently supported are `static`, `once`, and `flip`. 

## Behaviors

**Static**

For `static` behavior, the DNS server always returns the static IP defined in the `config.yaml` file. 

Example:

```yaml
- domain: 'example.com'
  ip: '1.2.3.4'
  behavior: 'static'  # Always returns 1.2.3.4 for example.com
```

**Once**

For `once` behavior, the DNS server first returns Google's DNS response, then always responds with the static IP for all subsequent requests.

Example:

```yaml
- domain: 'moodle.com'
  ip: '5.6.7.8'
  behavior: 'once'  # Returns Google's DNS response first time, then 5.6.7.8 afterwards

```

**Flip**

For `flip` behavior, the DNS server alternates between Google's DNS response and the static IP for each request.

Example:

```yaml
- domain: 'google.com'
  ip: '9.10.11.12'
  behavior: 'flip'  # Alternates between Google's DNS response and 9.10.11.12 for each request
```

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

