import time
import ray

ray.init()

def f1():
    time.sleep(1)

@ray.remote
def f2():
    time.sleep(1)

print(time.time())
[ f1() for _ in range(10) ]
print(time.time())

ray.get([f2.remote() for _ in range(10)])
print(time.time())
