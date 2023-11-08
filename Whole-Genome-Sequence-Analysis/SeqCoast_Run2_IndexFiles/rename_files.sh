#!/usr/bin/env bash

## rename_html_files by Nkrumah Grant.

################################################################################
# Path to file containing keys
#mapping_file="/mnt/home/grantnkr/results_SeqCoast_Run2/SeqCoast_Run2_IndexFiles/key_to_sample.txt"

#Extract all .html files for each of the sequenced samples
#for dir in */; do cp "${dir}output/index.html" "${dir%/}_index.html"; done

#Move extracted files to a new directory
#mkdir name_of_new_directory
##move files
#mv *_index.html name_of_new_directory

# read in the key-to-sample mapping file
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
