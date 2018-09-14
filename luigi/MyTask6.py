import luigi
from MyTask5 import MyTask5

class MyTask6(luigi.Task):
    x = luigi.IntParameter()
    y = luigi.IntParameter(default=1)
    z = luigi.IntParameter(default=2)

    def requires(self):
        return [MyTask5(x=self.x)]

    def run(self):
        print(self.input())
        print(self.x * self.y * self.z)


if __name__ == '__main__':
    luigi.build([MyTask6(x=20, z=3)])
