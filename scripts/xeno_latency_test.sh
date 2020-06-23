#!/bin/bash

echo "Xenomai's Latency test will run for 20 seconds."
mkdir -p ../report
file_name=$(date "+xeno_latency_%y_%m_%d_%H_%M_%S")
/usr/xenomai/bin/latency -T 20 -q -h -g ../report/${file_name}
python ../src/xenomai_plot.py -f ../report/${file_name}

