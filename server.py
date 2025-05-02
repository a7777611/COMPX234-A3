import socket
import threading
from time import sleep, time
from tuple_space import TupleSpace

class Tuple_spaceServer:
    def __init__(self, port):
        self.port = port
        self.tuple_space = TupleSpace()
        self.running = False  # wether server is running
        # When the main thread exits, the daemon thread will automatically exit
        self.stats_thread = threading.Thread(target=self._print_stats_periodically, daemon=True)

    def start_server(self):
        self.running = True
        self.stats_thread.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', self.port))
            s.listen(10) # because we have 10 txt file ,to avoid connection lost(I don't sure if 10 is right)
            print(f"Server listening on port {self.port}")

            while self.running:
                try:
                    conn, addr = s.accept()
                    self.tuple_space.add_client()
                    threading.Thread(target=self.handle_client, args=(conn, addr)).start()
                except Exception as e:
                    if self.running:
                        print(f"Error accepting connection:{e}")
                    break

    def stop_server(self):
        self.running = False
        self.stats_thread.join()

    # print the statistics per 10s
    def _print_stats_periodically(self):
        while self.running:
            sleep(10)
            stats = self.tuple_space.get_stats()
            print("\n=== Server Statistics ===")
            print(f"Tuples: {stats['num_tuples']}")
            print(f"Avg tuple size: {stats['avg_tuple_size']:.2f}")
            print(f"Avg key size: {stats['avg_key_size']:.2f}")
            print(f"Avg value size: {stats['avg_value_size']:.2f}")
            print(f"Clients: {stats['total_clients']}")
            print(f"Operations: {stats['total_operations']}")
            print(f"READs: {stats['total_reads']}, GETs: {stats['total_gets']}, PUTs: {stats['total_puts']}")
            print(f"Errors: {stats['total_errors']}")
            print(f"Uptime: {time() - stats['start_time']:.2f} seconds")
            print("=======================\n")

    def handle_client(self, conn, addr):
        print(f"New connection from {addr}")
        try:
            while True:
                try:
                    data = conn.recv(1024).decode('utf-8').strip()
                    if not data:
                        break

                    # Parse the request (NNN R k, NNN G k, NNN P k v)
                    try:
                        size_str, info = data.split(maxsplit = 1)
                        size = int (size_str)
                        if len(data) != size:
                            response = 'ERR Invalid request size'
                        else:
                            operation = info[0]
                            content = info[2:]
                            
                            # three action
                            if operation == 'R':
                                response = self.tuple_space.read(content)
                            
                            elif operation == 'G':
                                response == self.tuple_space.get(content)
                            
                            elif operation == 'P':
                                try:
                                    key, value = content.split(maxsplit = 1)
                                    response = self.tuple_space.put(key, value)
                                except ValueError:
                                    response = "ERR PUT requires both key and value"
                            
                            else:
                                response = "ERR Invalid operation"
                    
                    except ValueError as e:
                        response = f"ERR Invalid request format: {str(e)}"

                    response_size = len(response) + 4# 3 for size digits and 1 for space
                    format_response = f"{response_size:03d} {response}"
                    #send response to client
                    conn.sendall(format_response.encode('utf-8'))
                
                except Exception as e:
                    error_msg = f"ERR Internal server error: {str(e)}"
                    formatted_error = f"{len(error_msg)+4:03d} {error_msg}"
                    conn.sendall(formatted_error.encode('utf-8'))
                    break
        
        except Exception as e:
            print(f"Error with client {addr}: {str(e)}")
        
        finally:
            conn.close()
            print(f"Connection closed with {addr}")

# main code
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        if not (50000 <= port <= 59999):
            print("Port must be between 50000 and 59999")
            sys.exit(1)
    except ValueError:
        print("Port must be a number")
        sys.exit(1)

    server = Tuple_spaceServer(port)
    try:
        server.start_server()
    except KeyboardInterrupt:
        server.stop_server()
        print("\nServer stopped")


