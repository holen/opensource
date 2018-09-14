import luigi
import random
class Streams(luigi.Task):
    date = luigi.DateParameter()

    def run(self):
        with self.output().open('w') as output:
            for _ in range(1000):
                output.write('{} {} {}\n'.format(
                    random.randint(0, 999),
                    random.randint(0, 999),
                    random.randint(0, 999)))

    def output(self):
        return luigi.LocalTarget(self.date.strftime('data/streams_%Y_%m_%d_faked.tsv'))
