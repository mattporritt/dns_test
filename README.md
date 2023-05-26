# Python Test DNS Server

This project provides a simple DNS server written in Python. The server can be used for testing and development purposes. It forwards DNS requests to Google's DNS servers, receives the responses, and sends them back to the client. It also allows you to define specific domains and dictate how they should respond to DNS requests.

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

### Behaviors  ###

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

### Debugging ###
By default the server will only output logging for domains that are defined in `config.yaml`. To enable debug logging for all domains, set the `debug` when starting the server.

```commandline
sudo python3 dns_server.py -d
```

## Using the DNS Server ##
To use the DNS server, you need to configure your computer to use it. Configuration depends on your operating system and context.

### DNS For Docker ###
If you are using Docker, you can pass it the DNS server's IP address as a command line argument. For example:

```commandline
docker run --dns 192.168.120.100 
```
Where the IP is the address of the DNS server. (Likely the IP of your host machine).

If you are using a Docker Compose file, you can specify the DNS server's IP address in the `dns` field. For example:

```yaml
    dns:
      - 192.168.120.100 # IP address of the DNS server. (Likely the IP of your host machine).
```

Using either of these methods will cause Docker to use the DNS server for all DNS requests for the container.

### Changing Mac Host DNS ###
If you are running Mac OS, you can set the DNS for the system on the command line by running the following command:

```commandline
sudo networksetup -setdnsservers Wi-Fi 127.0.0.1
# or
sudo networksetup -setdnsservers Ethernet 127.0.0.1
```
You can find the name of your network service by opening a Terminal window and typing:

```commandline
networksetup -listallnetworkservices
```

### Changing Ubuntu Host DNS ###
On Ubuntu, you can change your DNS settings via the command line by editing the /etc/resolv.conf file or by using the nmcli command if you're using NetworkManager. Here's how to do it:

**Method 1: Editing /etc/resolv.conf**

1. Open a Terminal window.
2. Open the /etc/resolv.conf file in a text editor with root privileges. For example, you can use nano:

```commandline
sudo nano /etc/resolv.conf
```

3. In the file, you'll see lines that look like this:

```commandline
nameserver 8.8.8.8
nameserver 8.8.4.4
```

These are your current DNS servers. You can replace these with the DNS servers you want to use.

4. Save the file and exit the text editor. If you're using nano, you can do this by pressing Ctrl+X, then Y to confirm that you want to save the changes, and then Enter to confirm the file name.
5. Test the new DNS settings. You can do this by pinging a domain name like google.com and checking that you get a response.

**Method 2: Using nmcli with NetworkManager**

1. Open a Terminal window.
2. Find the name of your network connection:

```commandline
nmcli con show
```

3. Set the DNS for that connection:

```commandline
sudo nmcli con mod <connection> ipv4.dns "8.8.8.8 8.8.4.4"
```

Replace <connection> with the name of your network connection, and replace 8.8.8.8 8.8.4.4 with the DNS servers you want to use.

4. To make the changes take effect, you need to restart the network connection:

```commandline
sudo nmcli con down <connection> && sudo nmcli con up <connection>
```

Replace <connection> with the name of your network connection.


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

