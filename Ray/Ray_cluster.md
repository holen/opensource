# Ray 集群部署
## 手动部署集群

这个适合小规模的集群部署

### 部署依赖
- 确保集群内的各节点可以正常相互通信
- 每个集群节点必须先安装好 Ray 环境

### 部署集群
在 master 节点上，运行如下命令启动 master 。如果 `--redis-port`参数没有提供，则 Ray 会随机选择一个端口。

    ray start --head --redis-port=6379
    
这命令将会输出启动的 redis-server 服务地址，如下

    Using IP address 192.168.120.202 for this node.
    Process STDOUT and STDERR is being redirected to /tmp/raylogs/.
    Waiting for redis server at 127.0.0.1:6379 to respond...
    Waiting for redis server at 127.0.0.1:62102 to respond...
    Starting local scheduler with the following resources: {'CPU': 2, 'GPU': 0}.
    
    ======================================================================
    View the web UI at http://localhost:8888/notebooks/ray_ui11033.ipynb?token=2ad383130aa98e71ce51b0da78d8990ac8a584dade59131f
    ======================================================================
    
    {'node_ip_address': '192.168.120.202', 'redis_address': '192.168.120.202:6379', 'object_store_addresses': [ObjectStoreAddress(name='/tmp/plasma_store81590734', manager_name='/tmp/plasma_manager65941372', manager_port=49311)], 'local_scheduler_socket_names': ['/tmp/scheduler15702921'], 'raylet_socket_names': [], 'webui_url': 'http://localhost:8888/notebooks/ray_ui11033.ipynb?token=2ad383130aa98e71ce51b0da78d8990ac8a584dade59131f'}
    
    Started Ray on this node. You can add additional nodes to the cluster by calling
    
        ray start --redis-address 192.168.120.202:6379
    
    from the node you wish to add. You can connect a driver to the cluster from Python by running
    
        import ray
        ray.init(redis_address="192.168.120.202:6379")
    
    If you have trouble connecting from a different machine, check that your firewall is configured properly. If you wish to terminate the processes that have been started, run

    ray stop
    
`http://localhost:8888/notebooks/ray_ui11033.ipynb?token=2ad383130aa98e71ce51b0da78d8990ac8a584dade59131f`这个是 Web Ui 的访问地址。如果我们在本地机器上运行 Ray ，那么就可以直接通过这个URL在浏览器上访问。否则，我们就需要做端口转发，将远程机器的8888转发到本地来。当我们 ssh 到远程机器时，可以添加 -L 参数实现端口转发。

    ssh -L <local_port>:localhost:<remote_port> <user>@<ip-address>

在其他节点上运行如下命令就可以加入刚创建的集群了

    ray start --redis-address 192.168.120.202:6379
    
如果你想指定机器的CPU数和GPU数，你可以添加`--num-cpus=10`和`--num-gpus=`参数。如果没有提供这两个参数， Ray 将自动检测 cpu 的个数并默认设置 GPU 为 0 。

现在，我们已经启动所有的 Ray 程序在每个 Ray 节点上，包括
- Some worker processes on each machine.
- An object store on each machine.
- A local scheduler on each machine.
- Multiple Redis servers (on the head node).
- One global scheduler (on the head node).

为了测试一些命令，可以在任意一台集群机器上，启动 python shell ，执行如下命令

    import ray
    ray.init(redis_address="192.168.120.202:6379")
    
现在，我们就可以定义远程功能和执行任务。下面有个例子可以核实有几个节点加入到当前集群里
```python
import time

@ray.remote
def f():
    time.sleep(0.01)
    return ray.services.get_node_ip_address()

# Get a list of the IP addresses of the nodes that have joined the cluster.
set(ray.get([f.remote() for _ in range(1000)]))
```

### 停止 Ray 
当你想停止运行 Ray , 在各个节点上运行 `ray stop`就可以了。

## 部署大型集群
部署 Ray 集群需要一堆的手动工作。在这里我们将声明如何使用 parallel ssh 命令在多台机器上并行运行简单的程序命令。

### 前提准备
在 master 节点上安装 pssh 

    yum install pssh -y
    
### 部署 Ray 集群
附加假设：
- 以下的所有命令都在 master 节点上运行
- master 节点将运行 Redis 和 global scheduler 进程服务
- master 节点可以通过 ssh 免密码登录各个节点机器 
- Ray checkout 在各个机器的 `$HOME/ray` 目录

### 生成节点 IP 地址列表
在 master 节点上，新建一个 `workers.txt` 文件，这个文件每行就是一个节点IP地址。不要把 master 节点IP写进去。

    172.31.27.16
    172.31.29.173
    172.31.24.132
    172.31.29.224
    
确定在 master 上可以 ssh 到各个节点

    for host in $(cat workers.txt); do
      ssh -o "StrictHostKeyChecking no" $host uptime
    done
    
### 启动 Ray
在 master 上启动 Ray

    ray start --head --redis-port=6379
    
在各个节点上启动 Ray

新建`start_worker.sh`，内容如下
```
# Make sure the SSH session has the correct version of Python on its path.
# You will probably have to change the line below.
export PATH=/home/ubuntu/anaconda3/bin/:$PATH
ray start --redis-address=<head-node-ip>:6379
```
这个脚本将在 worker 节点上运行，并启动 Ray 。在这里要把`<head-node-ip>`替换成 Master 节点IP.

现在使用`pssh`命令在各个节点上启动 Ray

    pssh -h workers.txt -P -I < start_worker.sh
    
现在我们已经在各个节点上启动 Ray 。Ray 进程包括如下：
- Some worker processes on each machine.
- An object store on each machine.
- A local scheduler on each machine.
- Multiple Redis servers (on the head node).
- One global scheduler (on the head node).
 
### 停止 Ray 
新建 `stop_worker.sh` 文件，内容如下：
```
# Make sure the SSH session has the correct version of Python on its path.
# You will probably have to change the line below.
export PATH=/home/ubuntu/anaconda3/bin/:$PATH
ray stop
```

这个脚本运行在各个节点上，将停止 Ray 服务。我们必须替换 `/home/ubuntu/anaconda3/bin/` 成我们服务器上的 Python 路径。

现在使用 `pssh` 命令在各个节点上停止 Ray

    pssh -h workers.txt -P -I < stop_worker.sh

在 master 上停止 Ray 

    ray stop 
    

