import threading
from time import time

class TupleSpace:
    def __init__(self):
        # a dictionary to store key-value pairs
        self.tuples = {}
        # a threading lock to ensure multithreading security
        self.lock = threading.Lock()
        # a dictionary to record the static info
        # the total number of clients , the total number of operations, total READs, total GETs, total PUTs, and how many errors.
        self.stats ={
            'total_clients':0,
            'total_operation':0,
            'total_reads':0,
            'total_gets':0,
            'total_puts':0,
            'total_errors':0,
            'start_time':time()
        }
    # read(k)
    def read(self,key):
        with self.lock:
            self.stats['total_operations'] +=1
            self.stats['total_reads'] +=1
            if key in self.tuples:
                return f"OK ({key},{self.tuples[key]} read"
            else:
                self.stats['total_errors'] +=1
                return f"ERR {key} does not exist"
    # get(k)
    def get(self,key):
        with self.lock:
            self.stats['total_operations'] +=1
            self.stats['total_gets'] +=1
            if key in self.tuples:
                value = self.tuples.pop(key)
                return f"OK ({key}, {value}) removed"
            else:
                self.stats['total_errors'] +=1
                return f"ERR {key} does not exist"
    # put(k,v)        
    def put(self,key,value):
        with self.lock:
            self.stats['total_operations'] +=1
            self.stats['total_puts'] +=1
            if key not in self.tuples:
                self.tuples[key] = value
                return f"OK ({key}, {value}) added"
            else:
                self.stats['total_errors'] += 1
                return f"ERR {key} already exists"
    
    def total_client(self):
        with self.lock:
            self.stats['toatl_clients'] +=1
    
    # Server output：the number of tuples , the average tuple size, the average key size, the average value size (string),
    def get_stats(self):
        with self.lock:
            num_tuples = len(self.tuples)
            stats = {
                'num_tuples':num_tuples,
                **self.stats
            }

            if num_tuples > 0:
                total_key_size = sum(len(k) for k in self.tuples.keys())
                total_value_size = sum(len(v) for v in self.tuples.values())
                avg_tuple_size = (total_key_size + total_value_size) / num_tuples
                avg_key_size = total_key_size / num_tuples
                avg_value_size = total_value_size / num_tuples
            else:
                avg_tuple_size = 0.0
                avg_key_size = 0.0
                avg_value_size = 0.0

            stats.update({
                'avg_tuple_size':  avg_tuple_size,
                'avg_key_size': avg_key_size,
                'avg_value_size': avg_value_size
            })
        
        return stats
