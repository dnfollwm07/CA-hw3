#!/bin/bash

trace_files=("462.libquantum.gz" "464.h264ref.gz" "403.gcc.gz" "445.gobmk.gz")
associativities=(1 4 8 16 32)
block_sizes=(128 256 512 2048 4096 16384)

file_name="403.gcc.gz"
cache_size=16384

output_file="results.txt"

> $output_file

for trace_file in "${trace_files[@]}"; do
    for a in "${associativities[@]}"; do
        for b in "${block_sizes[@]}"; do
            output=$(python3 sim_sa.py $file_name $cache_size $a $b 1000)
            
            cpi_stall=$(echo "$output" | grep "CPI_stall" | awk '{print $2}')
            miss_rate=$(echo "$output" | grep "miss_rate" | awk '{print $2}')
            amat=$(echo "$output" | grep "AMAT" | awk '{print $2}')
            
            echo -e "Trace: $trace_file, Associativity: $a, Block Size: $b\nCPI_stall: $cpi_stall\nmiss_rate: $miss_rate\nAMAT: $amat\n=====================================" >> $output_file
        done
    done
done

echo "Results have been saved to $output_file"