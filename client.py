import socket
import sys
from protocal import format_request, parse_response,valid_request

class TupleSpaceClient:
    def __init__(self, host, port, request_file):
        self.host = host
        self.port = port
        self.request_file =request_file

    def run(self):
        with open(self.request_file, 'r') as f:
            requests = [line.strip() for line in f if line]
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
            except ConnectionRefusedError:
                print(f"Connection error: {str(e)}")
                return
            
            for request in requests:
                valid, msg = valid_request(request)
                if not valid:
                    print(f"not valid request'{request}':{msg}")
                    break
                try:
                    # Validate and format the request
                    formatted = format_request(request)
                    print(f"Request: {formatted}")
        
                    # Send the request
                    s.sendall(formatted.encode('utf-8'))
        
                    # Receive response
                    response = s.recv(1024).decode('utf-8')
                    try:
                        size_str, info = response.split(maxsplit=1)
                        size = int(size_str)
                        if len(response) != size:
                            print("Error: Invalid response size")
                            continue
                        parsed = parse_response(response)
                        print(f"Response: {parsed}")
                    except ValueError:
                        print(f"Invalid response format: {response}")
                except ValueError as e:
                    print(f"Invalid request '{request}': {str(e)}")
                    break    

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <request_file>")
        sys.exit(1)
    
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Port must be a number")
        sys.exit(1)
    request_file = sys.argv[3]
    
    client = TupleSpaceClient(host, port, request_file)
    client.run()