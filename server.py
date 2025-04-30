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

