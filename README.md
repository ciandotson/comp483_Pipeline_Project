# comp483_Pipeline_Project
This repository is a walkthrough of an analysis of the transcriptomes of individuals 2 and 6 days post infection (dpi) with Huamn herpevirus, or Huamn cytomegalovirus, or HCMV.

# **Step 1: Downloading the Raw Fastq Files**
The raw fastq files for RNA-Seq data we are interested in ar found in these four links:

Donor 1 (2dpi): https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660030/SRR5660030

Donor 1 (6dpi): https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660033/SRR5660033

Donor 2 (2dpi): https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660044/SRR5660044

Donor 2 (6dpi): https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660045/SRR5660045

To get the SRA Normalized data for each of these accessions, simply use `wget`:

`wget https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660030/SRR5660030`

`wget https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660033/SRR5660033`

`wget https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660044/SRR5660044`  

`wget https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660045/SRR5660045`

These files are not yet readable as fastq files, but you can extract the fastq files by using `fasterq-dump` NCBI's SRA-toolkit:

`fasterq-dump SRR5660030`

`fasterq-dump SRR5660033`

`fasterq-dump SRR5660044`

`fasterq-dump SRR5660045`
