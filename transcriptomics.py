# This is a python script that quickly runs a full transcriptomics analysis when given a series of RNA-seq fastq files and a reference genome #
import argparse
import sys

#function to parse command line arguments #
def check_arg(args=None): 
	parser = argparse.ArgumentParser(description= 'Produces a brief analysis of RNA-seq data')
	parser.add_argument('-i', '--input',
		help='path to input file',
		required = 'True')
	parser.add_argument('-o', '--output',
		help = 'output file name',
		required = 'True')
	return parser.parse_args(args)

#retrieve command line arguments and assign to variables
args = check_arg(sys.argv[1:])
infile = args.input
outfile = args.output


# formating the CDS entries of HCMV into a fasta that only contains the protein IDs as entries #
from Bio import SeqIO
import re

def FastGen(fasta): # function that formats a fasta file to only contain the protein id as its header #
    ids = list() # list that will contain all the protein ids #
    seqs = list() # list that will contain all the sequences #
    with open(fasta, 'r') as f: # opening the connection to the fasta file #
        for entry in SeqIO.parse(f, 'fasta'): # for each entry in the fasta reads as a fasta #
            seqs.append(str(entry.seq + '\n')) # add each sequence to the seqs list plus a \n at the end #
            found = re.findall(r"\[protein_id=([^\]]+)\]", entry.description) # regex command to find all of the characters that are found after 'protein_id=' and before the ']'
            for lost in found: 
                ids.append(str('>' + lost + '\n')) # append the protein id flanked by > and \n #
    fin = list() # list to make the final fasta file #
    for i in range(0, len(seqs)): # for each entry #
        fin.append(ids[i]) # add the entry protein id #
        fin.append(seqs[i]) # add the entry sequence #
    fin = ''.join(fin) # join the list into a string #
    return(fin)

with open('hcmv_cds.fasta', 'w') as f:
    f.write(FastGen(infile))

import os
os.system('grep ">" hcmv_cds.fasta | wc -l | cat > cds_count') # unix command that finds all the > in the file, counts the number of times in appears, and writes it into cds_count #
os.system('echo "The HCMV genome (NC_006273.2) has $(cat cds_count) CDS." > PipelineProject.log') # unix command that states the words The HCMV genome (NC_006273.2) has (whatever is in cds_counts) CDS # 

os.system('kallisto index -i hcmv.idx hcmv_cds.fasta') # kallisto command in which an index is made from the viral reference genome #
os.system('mkdir ./results') # unix command to make a directory for the results to go #

os.system('kallisto quant -i hcmv.idx -o ./results/SRR5660030 -b 30 -t 4 ./fastqs/SRR5660030_1.fastq ./fastqs/SRR5660030_2.fastq') # kallisto command that quantifies the number of reads from sample 1 #
os.system('kallisto quant -i hcmv.idx -o ./results/SRR5660033 -b 30 -t 4 ./fastqs/SRR5660033_1.fastq ./fastqs/SRR5660033_2.fastq') # kallisto command that quantifies the number of reads from sample 2 #  
os.system('kallisto quant -i hcmv.idx -o ./results/SRR5660044 -b 30 -t 4 ./fastqs/SRR5660044_1.fastq ./fastqs/SRR5660044_2.fastq') # kallisto command that quantifies the number of reads from sample 3 #
os.system('kallisto quant -i hcmv.idx -o ./results/SRR5660045 -b 30 -t 4 ./fastqs/SRR5660045_1.fastq ./fastqs/SRR5660045_2.fastq') # kallisto command that quantifies the number of reads from sample 4 # 

import csv

def read_tsv(file_path): # function that reads a tsv file when given the file path #
    with open(file_path, 'r') as r: # with read capabilities given to python for the tsv table #
        reader = csv.reader(r, delimiter='\t') # apply the csv wrapper on the tsv file with \t as the delimiter #
        tsv_data = list(reader) # save the tsv wrapper as a list #
    return tsv_data


headers = str('\nsample\tcondition\tmin_tpm\tmed_tpm\tmean_tpm\tmax_tpm') # this will be the first row of the table summarizing the tpm results #
data1 = read_tsv('./results/SRR5660030/abundance.tsv') # the read tsv file of the first donor at the first time of infection

tpm1 = list() # open list that will contain all of the tpms for each individual transcript #
for i in range(1, len(data1)): # over the length of the first tsv file (barring the first row) #
    tpm1.append(float(data1[i][4])) # add the fifth value (the tpm value) for each row to tpm1 #

import statistics
min1 = min(tpm1) # take the minimum value of tpm1 #
max1 = max(tpm1) # take the max value of tpm1 #
med1 = statistics.median(tpm1) # take the median value of tpm1 #
mean1 = statistics.mean(tpm1) # take the mean of tpm1 #

sample1 = 'Donor 1' # sample 1 is from donor 1#
condition1 = '2dpi' # sample 1 was taken 2 days post infection #
fin1 = str('\n' + sample1 + '\t' + condition1 + '\t' + str(min1) + '\t' + str(med1) + '\t' + str(mean1) + '\t' + str(max1)) # add each saved value to a string delimited by tabs \t #

data2 = read_tsv('./results/SRR5660033/abundance.tsv') # same but for sample 2 #

tpm2 = list()
for i in range(1, len(data2)):
    tpm2.append(float(data2[i][4]))

import statistics
min2 = min(tpm2)
max2 = max(tpm2)
med2 = statistics.median(tpm2)
mean2 = statistics.mean(tpm2)

sample2 = 'Donor 1'
condition2 = '6dpi'
fin2 = str('\n' + sample2 + '\t' + condition2 + '\t' + str(min2) + '\t' + str(med2) + '\t' + str(mean2) + '\t' + str(max2))

data3 = read_tsv('./results/SRR5660044/abundance.tsv') # same but for sample 3 #

tpm3 = list()
for i in range(1, len(data3)):
    tpm3.append(float(data3[i][4]))

import statistics
min3 = min(tpm3)
max3 = max(tpm3)
med3 = statistics.median(tpm3)
mean3 = statistics.mean(tpm3)

sample3 = 'Donor 3'
condition3 = '2dpi'
fin3 = str('\n' + sample3 + '\t' + condition3 + '\t' + str(min3) + '\t' + str(med3) + '\t' + str(mean3) + '\t' + str(max3))

data4 = read_tsv('./results/SRR5660045/abundance.tsv') # same but for sample 4 #

tpm4 = list()
for i in range(1, len(data4)):
    tpm4.append(float(data4[i][4]))

import statistics
min4 = min(tpm4)
max4 = str(max(tpm4)) + '\n'
med4 = statistics.median(tpm4)
mean4 = statistics.mean(tpm4)

sample4 = 'Donor 3'
condition4 = '6dpi'
fin4 = str('\n' + sample4 + '\t' + condition4 + '\t' + str(min4) + '\t' + str(med4) + '\t' + str(mean4) + '\t' + str(max4))

with(open('PipelineProject.log', 'a')) as f:
    f.write(headers)
    f.write(fin1)
    f.write(fin2)
    f.write(fin3)
    f.write(fin4)

os.system('Rscript hcmv.R') # Rscript that analyzes the output of kallisto and gives differential gene expression #

os.system('echo "$(cat hcmv_sigs.tsv)" >> PipelineProject.log') # write the output of the significant results to PipelineProject.log #

# Point 5: using bowtie2 to map the reads to the reference genome #
os.system('bowtie2-build "hcmv_genome.fasta" ./hcmv_gen/hcmv_gen') # create a bowtie index from the full genome of the virus #

os.system('bowtie2 --quiet -x ./hcmv_gen/hcmv_gen -1 ./fastqs/SRR5660030_1.fastq -2 ./fastqs/SRR5660030_2.fastq -S d1i2.sam --al-conc d1i2_mapped_reads.fq') # map the reads from the transcriptome to the refernce genome of the virus in sample 1 #
os.system('bowtie2 --quiet -x ./hcmv_gen/hcmv_gen -1 ./fastqs/SRR5660033_1.fastq -2 ./fastqs/SRR5660033_2.fastq -S d1i6.sam --al-conc d1i6_mapped_reads.fq') # map the reads from the transcriptome to the refernce genome of the virus in sample 2 #
os.system('bowtie2 --quiet -x ./hcmv_gen/hcmv_gen -1 ./fastqs/SRR5660044_1.fastq -2 ./fastqs/SRR5660044_2.fastq -S d3i2.sam --al-conc d3i2_mapped_reads.fq') # map the reads from the transcriptome to the refernce genome of the virus in sample 3 #
os.system('bowtie2 --quiet -x ./hcmv_gen/hcmv_gen -1 ./fastqs/SRR5660045_1.fastq -2 ./fastqs/SRR5660045_2.fastq -S d3i6.sam --al-conc d3i6_mapped_reads.fq') # map the reads from the transcriptome to the refernce genome of the virus in sample 4 #

os.system('mkdir reads_mapped') # make a directory for the reads that were mapped to the reference genome by bowtie2 #
os.system('mv *mapped* reads_mapped') # move all the reads that mapped to reads_mapped #

os.system('grep "@SRR" ./fastqs/SRR5660030_2.fastq | wc -l | cat > d1i2_pre_count') # find all of the gene entries in the original, unmapped file, count the number of occurences, and output it to the pre_count #
os.system('grep "@SRR" ./reads_mapped/d1i2_mapped_reads.2.fq | wc -l | cat > d1i2_read_count') # find all of the gene entries of the mapped reads, count the number of occurences, and output it to the read_count #
os.system('echo "Donor 1 (2dpi) had $(cat d1i2_pre_count) read pairs before Bowtie2 filtering and $(cat d1i2_read_count) read pairs after." | cat >> PipelineProject.log') # paste the text with the pre_count and read_cunt to the end of PipelineProject.log #

os.system('grep "@SRR" ./fastqs/SRR5660033_2.fastq | wc -l | cat > d1i6_pre_count')  # same as above just with the first donor 6 dpi #
os.system('grep "@SRR" ./reads_mapped/d1i6_mapped_reads.2.fq | wc -l | cat > d1i6_read_count')
os.system('echo "Donor 1 (6dpi) had $(cat d1i6_pre_count) read pairs before Bowtie2 filtering and $(cat d1i6_read_count) read pairs after." | cat >> PipelineProject.log')

os.system('grep "@SRR" ./fastqs/SRR5660044_2.fastq | wc -l | cat > d3i2_pre_count') # same as above except with third donor 2 dpi #
os.system('grep "@SRR" ./reads_mapped/d3i2_mapped_reads.2.fq | wc -l | cat > d3i2_read_count')
os.system('echo "Donor 3 (2dpi) had $(cat d3i2_pre_count) read pairs before Bowtie2 filtering and $(cat d3i2_read_count) read pairs after." | cat >> PipelineProject.log')

os.system('grep "@SRR" ./fastqs/SRR5660045_2.fastq | wc -l | cat > d3i6_pre_count') # same as above except with the third donor 6 dpi #
os.system('grep "@SRR" ./reads_mapped/d3i6_mapped_reads.2.fq | wc -l | cat > d3i6_read_count')
os.system('echo "Donor 3 (6dpi) had $(cat d3i6_pre_count) read pairs before Bowtie2 filtering and $(cat d3i6_read_count) read pairs after." | cat >> PipelineProject.log')

# Point 6: Running SPAdes on the mapped reads #
os.system('spades.py -k 77 -t 2 --only-assembler --pe-1 1 ./reads_mapped/d1i2_mapped_reads.1.fq --pe-2 1 ./reads_mapped/d1i2_mapped_reads.2.fq --pe-1 2 ./reads_mapped/d1i6_mapped_reads.1.fq --pe-2 2 ./reads_mapped/d1i6_mapped_reads.2.fq -o d1_assembly/') # creates a de novo assembly using only the mapped reads for donor 1#
os.system('spades.py -k 77 -t 2 --only-assembler --pe-1 1 ./reads_mapped/d3i2_mapped_reads.1.fq --pe-2 1 ./reads_mapped/d3i2_mapped_reads.2.fq --pe-1 2 ./reads_mapped/d3i6_mapped_reads.1.fq --pe-2 2 ./reads_mapped/d3i6_mapped_reads.2.fq -o d3_assembly/') # creates a de novo assembly using only the mapped reads for donor 3#
os.system('echo "spades.py -k 77 -t 2 --only-assembler --pe-1 1 ./reads_mapped/d1i2_mapped_reads.1.fq --pe-2 1 ./reads_mapped/d1i2_mapped_reads.2.fq --pe-1 2 ./reads_mapped/d1i6_mapped_reads.1.fq --pe-2 2 ./reads_mapped/d1i6_mapped_reads.2.fq -o d1_assembly/" | cat >> PipelineProject.log') # output the spades command for donor 1 to the end of PipelineProject.log #
os.system('echo "spades.py -k 77 -t 2 --only-assembler --pe-1 1 ./reads_mapped/d3i2_mapped_reads.1.fq --pe-2 1 ./reads_mapped/d3i2_mapped_reads.2.fq --pe-1 2 ./reads_mapped/d3i6_mapped_reads.1.fq --pe-2 2 ./reads_mapped/d3i6_mapped_reads.2.fq -o d3_assembly/" | cat >> PipelineProject.log') # output the spades command for donor 3 to the end of PipelineProject.log #

# Point 7: Blasting the Longest Contig #
raw_fasta1 = SeqIO.parse('./d1_assembly/contigs.fasta', 'fasta') 
seqs1 = list()
ids1 = list()
for i in raw_fasta1:
	seqs1.append(i.seq)
	ids1.append(i.id)

lenseq1 = 0
maxseq1 = str()
maxid1 = str()
for i in range(0, len(seqs1)):
	if len(seqs1[i]) > lenseq1:
		maxseq1 = seqs1[i]
		maxid1 = ids1[i]
		lenseq1 = len(seqs1[i])

fin1 = str('>' + maxid1 + '\n' + maxseq1)

raw_fasta3 = SeqIO.parse('./d3_assembly/contigs.fasta', 'fasta') 
seqs3 = list()
ids3 = list()
for i in raw_fasta3:
	seqs3.append(i.seq)
	ids3.append(i.id)

lenseq3 = 0
maxseq3 = str()
maxid3 = str()
for i in range(0, len(seqs3)):
	if len(seqs3[i]) > lenseq3:
		maxseq3 = seqs3[i]
		maxid3 = ids3[i]
		lenseq3 = len(seqs3[i])

fin3 = str('>' + maxid3 + '\n' + maxseq3)

with open('d3_contig.fasta','w') as f:
	f.write(fin3)

	
