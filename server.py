import socket
import threading
import sys
import argparse

HOST = "0.0.0.0"

def handle_tcp_client(client_socket, client_address):
    """Handle TCP client connection"""
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            message = data.decode(errors="ignore").strip()
            print(f"[{client_address[0]}] {message}")
    except Exception as e:
        print(f"[-] Error handling TCP client {client_address[0]}: {e}")
    finally:
        client_socket.close()

def run_udp_server(port):
    """Run UDP syslog server"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, port))
    
    print(f"[+] Listening for UDP syslog messages on {HOST}:{port}")
    
    while True:
        try:
            data, addr = sock.recvfrom(4096)
            message = data.decode(errors="ignore").strip()
            print(f"[{addr[0]}] {message}")
        except KeyboardInterrupt:
            print("\n[-] Server stopped")
            break
        except Exception as e:
            print(f"[-] UDP Error: {e}")
    
    sock.close()

def run_tcp_server(port):
    """Run TCP syslog server"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, port))
    sock.listen(5)
    
    print(f"[+] Listening for TCP syslog connections on {HOST}:{port}")
    
    try:
        while True:
            client_socket, client_address = sock.accept()
            print(f"[+] New TCP connection from {client_address[0]}")
            
            # Handle each client in a separate thread
            client_thread = threading.Thread(
                target=handle_tcp_client, 
                args=(client_socket, client_address)
            )
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[-] Server stopped")
    except Exception as e:
        print(f"[-] TCP Error: {e}")
    finally:
        sock.close()

def show_help():
    """Display help information for using the SIEM server application"""
    help_text = """
SIEM Server - A simple syslog message receiver

DESCRIPTION:
    This application creates a SIEM (Security Information and Event Management) server
    that listens for syslog messages over UDP or TCP protocols. It displays received
    messages along with the source IP address.

USAGE:
    python server.py --protocol <PROTOCOL> [--port <PORT>] [--help]

REQUIRED ARGUMENTS:
    --protocol, -p      Protocol to use for the server (udp or tcp)

OPTIONAL ARGUMENTS:
    --port.             Port number to bind to (default: 5140)
                        Note: Use port 514 for standard syslog (requires root privileges)
    --help, -h          Show this help message and exit

EXAMPLES:
    # Start UDP server on default port 5140
    python server.py --protocol udp
    
    # Start TCP server on port 514 (requires root)
    sudo python server.py --protocol tcp --port 514
    
    # Start UDP server on custom port 9999
    python server.py -p udp -P 9999

PROTOCOLS:
    UDP - Connectionless protocol, suitable for high-volume syslog messages
    TCP - Connection-oriented protocol, ensures message delivery reliability

NOTES:
    - Press Ctrl+C to stop the server
    - TCP mode supports multiple simultaneous client connections
    - UDP mode processes messages as they arrive
    - Standard syslog port 514 requires root privileges
    """
    print(help_text)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='SIEM Server - A simple syslog message receiver',
        add_help=False  # We'll handle help ourselves
    )
    
    parser.add_argument(
        '--protocol', '-p',
        required=True,
        choices=['udp', 'tcp'],
        help='Protocol to use for the server (udp or tcp)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5140,
        help='Port number to bind to (default: 5140)'
    )
    
    parser.add_argument(
        '--help', '-h',
        action='store_true',
        help='Show help message and exit'
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Handle help argument
    if args.help:
        show_help()
        sys.exit(0)
    
    # Validate port range
    if not (1 <= args.port <= 65535):
        print(f"[-] Error: Port must be between 1 and 65535, got {args.port}")
        sys.exit(1)
    
    # Warn about privileged ports
    if args.port < 1024:
        print(f"[!] Warning: Port {args.port} is a privileged port and may require root privileges")
    
    print(f"[+] Starting SIEM server with {args.protocol.upper()} protocol on port {args.port}")
    
    try:
        if args.protocol.lower() == "udp":
            run_udp_server(args.port)
        elif args.protocol.lower() == "tcp":
            run_tcp_server(args.port)
    except PermissionError:
        print(f"[-] Permission denied: Cannot bind to port {args.port}")
        print("[-] Try using a port number >= 1024 or run with sudo for privileged ports")
        sys.exit(1)
    except OSError as e:
        print(f"[-] Socket error: {e}")
        sys.exit(1)
