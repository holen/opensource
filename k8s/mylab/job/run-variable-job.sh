#!/bin/bash

mkdir ./jobs

$ for i in apple banana cherry
do
  cat variable-job.yaml | sed "s/\$ITEM/$i/" > ./jobs/job-$i.yaml
done

