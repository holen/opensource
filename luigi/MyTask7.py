import luigi
import random
import datetime
from luigi import date_interval as d
from collections import defaultdict

class Streams(luigi.Task):
    date = luigi.DateParameter()

    def run(self):
        with self.output().open('w') as output:
            for _ in range(100):
                output.write('{} {} {}\n'.format(
                    random.randint(0, 999),
                    random.randint(0, 999),
                    random.randint(0, 999)))

    def output(self):
        return luigi.LocalTarget(self.date.strftime('data/streams_%Y_%m_%d_faked.tsv'))


class AggregateArtists(luigi.Task):
    date_interval = luigi.DateIntervalParameter()
    print(date_interval)
    print(type(date_interval))

    def output(self):
        return luigi.LocalTarget("data/artist_streams_%s.tsv" % self.date_interval)

    def requires(self):
        return [Streams(date) for date in self.date_interval]

    def run(self):
        artist_count = defaultdict(int)

        for input in self.input():
            with input.open('r') as in_file:
                for line in in_file:
                    timestamp, artist, track = line.strip().split()
                    artist_count[artist] += 1

        with self.output().open('w') as out_file:
            for artist, count in artist_count.items():
                out_file.write("{} {} {} \n".format(out_file, artist, count))


if __name__ == '__main__':

    # for cls in [d.Year, d.Month, d.Week, d.Date, d.Custom]:
    #     i = cls.parse(s)
    luigi.build([AggregateArtists(d.Month.parse('2018-07'))])
