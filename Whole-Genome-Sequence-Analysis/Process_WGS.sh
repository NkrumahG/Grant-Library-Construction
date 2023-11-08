#!/usr/bin/env bash

## Process_WGS.sh authored by Nkrumah Grant.

## This shell script takes whole genome sequence data of randomly selcted wells from the Grant library and aligns them to several reference genomes. The goal of these alignments are multi-faceted. I intend to, 1) identify whether transposons have homologously recombined into the correct position of C6706 , and 2) if there are any spurious recombination events. I suspect that I will also find evidence of cross contamination, if it exists. On this note, while DNA from each of the wells were sent individually, I might be able to multiplex several samples.

#As of 04/09/2023 I can take this code and add it to the Breseq_file_extract.sh file. Doing so will allow me to go from raw paired reads to the genoome diff annotation step. Great analysis so far. 

#################################################################

## Load Breseq environment

source ./startbreseq.sh

# Set the path to the directory containing the sequence files
seqdir=/mnt/home/grantnkr/Seqcoast_Run2/HCD_WGS_GrantLibrary_20230406

# Set the path to the reference genome file(s)
refdir=/mnt/home/grantnkr/Vibrio_genome_refs

#mkdir
mkdir results_SeqCoast_Run2

# Set the output directory
outdir=./results_SeqCoast_Run2

# Loop through all pairs of sequence files
for file1 in ${seqdir}/*_R1_001.fastq.gz; do
  file2=${file1/_R1_001/_R2_001}
  outfile=${file1##*/}_output

  # Run the breseq command
  sbatch -p scavenger --mem=10G --time=24:00:00 -c 8 --wrap="breseq -j 8 -o ${outdir}/${outfile} -r ${refdir}/pSC189.gbk -r ${refdir}/pMMB67EH-tfoX-qstR-CmR.gbk -r ${refdir}/C6706_C1.gbk -r ${refdir}/C6706_C2.gbk ${file1} ${file2}"
done
