#!/bin/bash

echo "Cyclic will run for 30 seconds on a 98 priority."
mkdir -p ../report
file_name=$(date "+cyclictest_%y_%m_%d_%H_%M_%S")
cyclictest -D 30 -m -p98 -S -h 100 >> ../report/${file_name}
python ../src/cycl_plot.py -f ../report/${file_name}