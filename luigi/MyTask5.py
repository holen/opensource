import luigi
from luigi.contrib.simulate import RunAnywayTarget

class MyTask5(luigi.Task):
    x = luigi.IntParameter()
    y = luigi.IntParameter(default=0)

    def output(self):
        return RunAnywayTarget(self)

    def run(self):
        sum = self.x + self.y
        print(sum)
        self.output().done()
        return sum


