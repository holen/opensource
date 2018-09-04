# 高性能分布式框架 -- Ray 
Ray 是 UC Berkeley RISELab 新推出的高性能分布式执行框架，它使用了和传统分布式计算系统不一样的架构和对分布式计算的抽象方式，具有比Spark更优异的计算性能。  

Ray 带有加速深度学习和强化学习开发的函数库：
- [Tune](https://ray.readthedocs.io/en/latest/tune.html): 可扩展的超参数搜索
- [RLib](https://ray.readthedocs.io/en/latest/rllib.html): 可扩展的强化学习

## 安装 Ray 
Ray 支持 python2 和 python3 。安装命令如下：

    pip install ray
    
Ray 提供 web UI ，这个 web UI 提供用于调试 Ray jobs 的工具。  

安装 Web UI:

    pip install jupyter ipywidgets bokeh
    
## 教程
学习 Ray 之前，我们需要明白下列两点：
- Ray 是如何实现异步并行执行任务
- Ray 是如何使用对象 id 代表不变的远程对象

## 简介
Ray 是一个基于 Python 的分布式执行引擎。相同的代码可以在单个机器上运行以实现高效的多处理，并且可以在群集上用于大量的计算。 

Ray 系统架构  
![Ray架构](http://thyrsi.com/t6/365/1535695957x1822611437.png)

使用Ray时，涉及以下几个相关概念:

- worker(工作): 多个 worker 进行执行任务，并将结果存储在_对象库_中，每个进程是一个独立的处理单位
- object store(对象库): 每个节点都有一个对象库。每个对象库存储不可变的对象在共享内存中，并允许 workers 在相同节点上高效复制和反序列化对象
- local scheduler(本地调度器)：每个节点上有一个本地调度器，用于分配任务给本节点的 workers 
- global scheduler(全局调度器)：一个全局调度器调度从 本地调度器接收任务，并将它们分配到其他地方本地调度器
- driver(驱动): 一个 driver 是用户控制的 python 程序。例如，如果用户正在运行脚本或使用 python shell ，那么 driver 就是运行的脚本或者 python 进程。driver 与 worker 类似，都可以将任务提交给本地调度程序，并从对象库中获取对象，但不同之处在于本地调度程序不会讲任务分配给 driver 执行
- Redis server: 一个Redis服务器维护大量的系统状态。例如，他跟踪哪些对象在哪些机器上以及任务描述（而不是数据）上，他可以直接用于调试目的的查询。

## 启动 Ray
开始使用Ray，启动 Python 然后执行下面的命令
```python
import ray
ray.init()
```

## 不可变的远程对象
在 Ray 中，我们可以创建和计算 object 。我们将这些 object 称为远程对象，并使用对象ID来引用它们。远程对象存储在对象库中，并且群集中每个节点都有一个对象库。在集群设置中，我们可能实际上并不知道每个对象所在的机器。

一个对象ID本质上是一个唯一的ID可以被用来指代一个远程对象。如果您对 Futures 熟悉，我们的对象ID在概念上是相似的。

我们假设远程对象是不可变的。也就是说，它们的值在创建后不能改变。这允许远程对象在多个对象库中被复制，而不需要同步复制。

## Put 和 Get 
命令 `ray.get` 和 `ray.put` 可用于 _Python 对象_与_对象ID_之间进行转换，如示于以下的例子：
```python
x = "example"
ray.put(x)  # ObjectID(b49a32d72057bdcfc4dda35584b3d838aad89f5d)
```
该命令`ray.put(x)`将由工作进程或驱动程序进程运行（驱动程序进程是运行脚本的进程）。它需要一个 Python 对象，并将其复制到本地对象库（这里的本地指同一个节点上）。一旦对象被存储在对象库中，其值就不能被改变。

另外，`ray.put(x)`返回一个对象ID，它本质上是一个可以用来引用新创建的远程对象的ID。如果我们把对象ID保存在一个变量中如`x_id = ray.put(x)`，那么我们就可以把`x_id`传递给远程函数，这些远程函数将在相应的远程对象上运行。

命令`ray.get(x_id)`获取一个对象ID，并从相应的远程对象中创建一个Python对象。对于像数组这样的对象，我们可以使用共享内存，避免复制对象。对于其他对象，这将对象从对象库复制到工作进程的堆。如果与对象ID相对应的远程对象`x_id`没有存活在相同的节点上像 worker 调用 `ray.get(x_id)`，则远程对象将首先从具有该远程对象的对象库转移到需要它的对象库。
```python
x_id = ray.put("example")
ray.get(x_id)  # "example"
```
如果与对象ID对应的远程对象`x_id`尚未创建，则该命令`ray.get(x_id)`将进入等待，直到创建远程对象  

一个非常常见的用例`ray.get`是获取对象ID的列表。在这种情况下，你可以调用`ray.get(object_ids)`, 其中`object_ids`的对象ID的列表。
```python
result_ids = [ray.put(i) for i in range(10)]
ray.get(result_ids)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## Ray 异步计算

Ray 允许任意 Python 函数异步执行。这是通过将 Python 函数指定为远程函数来完成的。 

例如，一个普通的Python函数看起来像这样：
```python
def add1(a, b):
    return a + b
```
一个远程函数看起来像这样:
```python
@ray.remote
def add2(a, b):
    return a + b
```

## 远程函数
鉴于调用`add(1,2)`返回`3`并导致 Python 解释器阻塞，直到计算完成，调用`add2.remote(1, 2)` 立即返回一个对象ID并创建一个任务。该任务将由系统调度并异步执行(可能在不同的机器上)。当任务完成执行时，其返回值将被存储在对象库中。
```python
x_id = add2.remote(1, 2)
ray.get(x_id)  # 3
```

以下示例简单地演示了如何使用异步任务来并行化计算
```python
import time

def f1():
    time.sleep(1)

@ray.remote
def f2():
    time.sleep(1)

# 这个任务将消耗 10s
[f1() for _ in range(10)]

# 这个任务只消耗 1s (如果服务器上有10个cpus).
ray.get([f2.remote() for _ in range(10)])
```

这里提交任务和执行任务之间存在明显的区别。当调用远程函数时，执行该函数的任务将被提交给本地调度器，并立即返回任务输出的对象ID。但是，任务不会被执行直到系统在 worker 上执行这个任务。任务执行不是懒惰地完成的。系统将输入数据移动到任务中，一旦输入相关性可用并且有足够的资源进行计算，任务将立即执行。

提交任务时，每个参数可以通过值或对象ID传入。例如，这些行都能返回相同的结果
```python
add2.remote(1, 2)
add2.remote(1, ray.put(2))
add2.remote(ray.put(1), ray.put(2))
```

远程函数永远不会返回实际值，它们总是返回对象ID

当远程函数被实际执行时，它对 Python 对象进行操作。也就是说，如果使用任何对象ID调用远程函数，系统将从对象库中检索相应的对象

请注意，远程函数可以返回多个对象ID
```python
@ray.remote(num_return_vals=3)
def return_multiple():
    return 1, 2, 3

a_id, b_id, c_id = return_multiple.remote()
```

## 表达任务之间的依赖关系
程序员可以通过将一个任务的对象ID输出作为参数传递给另一个任务来表达任务之间的依赖关系。例如，我们可以启动三个任务，每个任务都依赖于前一个任务。
```python
@ray.remote
def f(x):
    return x + 1

x = f.remote(0)
y = f.remote(x)
z = f.remote(y)
ray.get(z) # 3
```
上面的第二个任务将不会执行，直到第一个任务完成，第三个任务将不会执行直到第二个任务完成。在这个例子中，没有并行的机会。

构建任务的能力可以很容易地表达有趣的依赖关系。考虑下面的一个树减少的实现
```python
import numpy as np

@ray.remote
def generate_data():
    return np.random.normal(size=1000)

@ray.remote
def aggregate_data(x, y):
    return x + y

# Generate some random data. This launches 100 tasks that will be scheduled on
# various nodes. The resulting data will be distributed around the cluster.
data = [generate_data.remote() for _ in range(100)]

# Perform a tree reduce.
while len(data) > 1:
    data.append(aggregate_data.remote(data.pop(0), data.pop(0)))

# Fetch the result.
ray.get(data)
```
## 远程功能嵌套远程功能
到目前为止，我们一直只从 driver 调用远程功能。但是工作进程也可以调用远程函数。为了说明这一点，请考虑下面的例子
```python
@ray.remote
def sub_experiment(i, j):
    # Run the jth sub-experiment for the ith experiment.
    return i + j

@ray.remote
def run_experiment(i):
    sub_results = []
    # Launch tasks to perform 10 sub-experiments in parallel.
    for j in range(10):
        sub_results.append(sub_experiment.remote(i, j))
    # Return the sum of the results of the sub-experiments.
    return sum(ray.get(sub_results))

results = [run_experiment.remote(i) for i in range(5)]
ray.get(results) # [45, 55, 65, 75, 85]
```
当`run_experiment`远程功能在 worker 上执行时,它调用远程功能 `sub_experiment`多次。这是一个例子，说明多个实验，每个实验在内部利用并行性，都可以并行运行。

## 参考文献
[ray tutorial](https://ray.readthedocs.io/en/latest/tutorial.html)   
[Ray：面向AI应用的分布式执行框架 ](https://www.ctolib.com/topics-129020.html)
