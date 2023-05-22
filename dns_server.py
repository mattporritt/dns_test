import socket
import socketserver
import logging
import dns.message
import signal
import sys
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)


class DNSHandler(socketserver.BaseRequestHandler):

    @staticmethod
    def log_dns_message(message, message_type):
        """
        Parses a DNS message and logs info about it.

        :param message: The DNS message in wire format
        :param message_type: The type of the message, either 'request' or 'response'
        """
        # Parse the DNS message
        dns_msg = dns.message.from_wire(message)

        if message_type == 'request':
            # If this is a request, log the domain(s) being requested
            logging.info(f"Client request for domain(s): {', '.join(str(q.name) for q in dns_msg.question)}")
        elif message_type == 'response':
            # If this is a response, log the A records (IPv4 addresses) returned
            for answer in dns_msg.answer:
                logging.info(f"Response: {answer.to_text()}")

    def handle(self):
        """
        Handles a DNS request.
        """
        # Receive data from client
        data = self.request[0].strip()
        socket_in = self.request[1]

        # Log the request message
        self.log_dns_message(data, 'request')

        # Forward the request to Google's DNS server
        dns_query = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dns_query.sendto(data, ("8.8.8.8", 53))

        # Receive response from Google's DNS server
        response, _ = dns_query.recvfrom(1024)

        # Log the response message
        self.log_dns_message(response, 'response')

        # Respond back to the client
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
    HOST, PORT = "localhost", 53
    server = socketserver.UDPServer((HOST, PORT), DNSHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    signal.signal(signal.SIGINT, signal_handler)

    print("DNS Server is starting...")
    server_thread.start()
    print("DNS Server is running...")

    # Wait for the server thread to finish
    server_thread.join()

    print("DNS Server has stopped.")
