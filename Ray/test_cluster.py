import ray
import time

ray.init(redis_address="192.168.120.202:6379")

@ray.remote
def f():
    time.sleep(1)
    return ray.services.get_node_ip_address()

# Get a list of the IP addresses of the nodes that have joined the cluster.
print(time.time())
print(ray.get([f.remote() for _ in range(10)]))
print(time.time())

