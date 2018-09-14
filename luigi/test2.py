import luigi
from luigi.contrib.simulate import RunAnywayTarget

class MyTask3(luigi.Task):
    x = luigi.IntParameter()
    y = luigi.IntParameter(default=0)

    def output(self):
        return RunAnywayTarget(self)

    def run(self):
        sum = self.x + self.y
        print(sum)
        self.output().done()
        return sum


class MyTask4(luigi.Task):
    x = luigi.IntParameter()
    y = luigi.IntParameter(default=1)
    z = luigi.IntParameter(default=2)

    def requires(self):
        return [MyTask3(x=self.x)]

    def run(self):
        print(self.x * self.y * self.z)


if __name__ == '__main__':
    luigi.build([MyTask4(x=20, z=3)])
