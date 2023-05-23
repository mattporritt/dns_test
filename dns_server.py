import socket
import socketserver
import logging
import dns.message
import signal
import threading
import yaml

# Set up logging
logging.basicConfig(level=logging.INFO)


class DNSHandler(socketserver.BaseRequestHandler):
    # Load specific domains from the config file
    with open('config.yaml') as file:
        config = yaml.full_load(file)
        specific_domains = {f"{entry['domain']}." if not entry['domain'].endswith('.') else entry['domain']:
                                {'ip': entry['ip'],
                                 'behavior': entry['behavior'],
                                 'used': False,
                                 'flip_next': True}
                            for entry in config['specific_domains']}

    @staticmethod
    def log_dns_message(message, message_type, static_response=False):
        # Parse the DNS message
        dns_msg = dns.message.from_wire(message)

        if message_type == 'request':
            # If this is a request, log the domain(s) being requested
            logging.info(f"Client request for domain(s): {', '.join(str(q.name) for q in dns_msg.question)}")
        elif message_type == 'response':
            # If this is a response, log the A records (IPv4 addresses) returned
            source = "static" if static_response else "Google DNS"
            logging.info(f"Response from {source}: {', '.join(answer.to_text() for answer in dns_msg.answer)}")

    @staticmethod
    def get_google_dns_response(request_data):
        """
        This method queries the Google DNS with the given request data.
        It sends the request to Google's DNS server and returns the response.

        :param request_data: The request data in wire format to send to Google's DNS
        :return: The response from Google's DNS server
        """
        dns_query = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dns_query.sendto(request_data, ("8.8.8.8", 53))

        # Receive and return response from Google's DNS server
        response, _ = dns_query.recvfrom(1024)
        return response

    def handle(self):
        data = self.request[0].strip()
        socket_in = self.request[1]

        dns_msg = dns.message.from_wire(data)

        # Check if the requested domain matches any of the specific domains
        for question in dns_msg.question:
            domain = str(question.name)
            if domain in self.specific_domains:
                domain_info = self.specific_domains[domain]
                if domain_info['behavior'] == 'static' or (domain_info['behavior'] == 'once' and domain_info['used']) or (
                        domain_info['behavior'] == 'flip' and not domain_info['flip_next']):
                    # Create a DNS response
                    response = dns.message.make_response(dns_msg)

                    # Add the answer to the response
                    rrset = dns.rrset.from_text(domain, 0, dns.rdataclass.IN, dns.rdatatype.A, domain_info['ip'])
                    response.answer.append(rrset)

                    # Log the response
                    self.log_dns_message(response.to_wire(), 'response', static_response=True)

                    # Send the response
                    socket_in.sendto(response.to_wire(), self.client_address)

                    if domain_info['behavior'] == 'once':
                        self.specific_domains[domain]['used'] = True
                    if domain_info['behavior'] == 'flip':
                        self.specific_domains[domain]['flip_next'] = not domain_info['flip_next']

                    return

        # Query Google's DNS server
        response = self.get_google_dns_response(data)

        # Log the response
        self.log_dns_message(response, 'response', static_response=False)

        # Flip the flag for flip behavior even when we used Google
        for question in dns_msg.question:
            domain = str(question.name)
            if domain in self.specific_domains and self.specific_domains[domain]['behavior'] == 'flip':
                self.specific_domains[domain]['flip_next'] = not self.specific_domains[domain]['flip_next']
            if domain in self.specific_domains and self.specific_domains[domain]['behavior'] == 'once':
                self.specific_domains[domain]['used'] = not self.specific_domains[domain]['used']

        # Send the response
        socket_in.sendto(response, self.client_address)


def signal_handler(sig, frame):
    """
    Handles the SIGINT signal (Ctrl+C) by shutting down the server.
    :param sig:
    :param frame:
    :return:
    """
    print('Keyboard exit signal received! Shutting down the server.')
    server.shutdown()  # Shutdown the server


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 53
    server = socketserver.UDPServer((HOST, PORT), DNSHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    signal.signal(signal.SIGINT, signal_handler)

    print("DNS Server is starting...")
    server_thread.start()
    print("DNS Server is running...")

    # Wait for the server thread to finish
    server_thread.join()

    print("DNS Server has stopped.")
