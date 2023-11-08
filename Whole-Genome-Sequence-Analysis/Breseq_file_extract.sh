#!/usr/bin/env bash

## Breseq files extract by Nkrumah Grant.

################################################################################
#Path to file containing keys
#mapping_file="/mnt/home/grantnkr/results_SeqCoast_Run2/SeqCoast_Run2_IndexFiles/key_to_sample.txt"

#Path to reference genome files
refdir=/mnt/home/grantnkr/Vibrio_genome_refs
gddir=/mnt/home/grantnkr/results_SeqCoast_Run2/GrantLibrary_Breseq_OutputGDs

#Start breseq

source /mnt/home/grantnkr/startbreseq.sh

#Extract all .html files for each of the sequenced samples
for dir in */; do cp "${dir}output/index.html" "${dir%/}_index.html"; done

#Extract all output.gd files for each of the sequenced samples
for dir in */; do cp "${dir}output/output.gd" "${dir%/}_output.gd"; done

# read in the key-to-sample mapping file
# Assumes that the key is located in between the first two instances of a file names underscore. i.e., for some sample named XY_45_33_Some_file.csv, the key is "45."

declare -A key_to_sample
while read -r line; do
  key=$(echo "$line" | awk '{print $1}')
  sample=$(echo "$line" | awk '{print $2}')
  key_to_sample["$key"]="$sample"
done < key_to_sample.txt

# loop through each html file and rename it according to the key-to-sample mapping
for file in *.html; do
  key=$(echo "$file" | cut -d '_' -f 2)
  sample=${key_to_sample["$key"]}
  if [[ "$sample" != "" ]]; then
    new_file="$sample"_index.html
    mv "$file" "$new_file"
  fi
done

# loop through each gd file and rename it according to the key-to-sample mapping
for file in *.gd; do
  key=$(echo "$file" | cut -d '_' -f 2)
  sample=${key_to_sample["$key"]}
  if [[ "$sample" != "" ]]; then
    new_file="$sample"_output.gd
    mv "$file" "$new_file"
  fi
done

#Move extracted files to a new directory
mkdir GrantLibrary_Breseq_IndexFiles
mkdir GrantLibrary_Breseq_OutputGDs

##move files
mv *_index.html GrantLibrary_Breseq_IndexFiles
mv *.gd GrantLibrary_Breseq_OutputGDs

##Compare mutations between GenomeDiff files 
# loop through each reference file in the refdir
# list all the reference genome files in the refdir
refs=($refdir/*.gbk)

# loop through all the gd files in the gddir
out=GrantLibrary_Mutations_Compared.html
ref_files=($(ls $refdir/*.gbk))
input_files=($(ls $gddir/*.gd))

cmd="gdtools ANNOTATE -o $out"
for ref_file in "${ref_files[@]}"; do
    cmd+=" -r $ref_file"
done

for input_file in "${input_files[@]}"; do
    cmd+=" $input_file"
done

echo $cmd # Print the command to the console
eval $cmd # Execute the command
