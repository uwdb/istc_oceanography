# istc_oceanography

Placeholder for datasets, todo items for the ISTC hackathon and demo.

Access the TX-E1 cluster via `ssh USERNAME@txe1-login.mit.edu`.
Make sure your user account is in the `istcdata` group.

Main folder is `/home/gridsan/groups/istcdata/datasets/ocean_metagenome`

We need to find a link between the metadata and the genomics data that has been processed in the `overlapped_trimmed_data` folder.




## README file on TX-E1

Simons metagenomics samples

Directories and sample processing steps:

1) `raw_data`: directory containing the raw Illumina NextSeq data from BioMicro. Each subfolder (150122Chi, etc) represents the BioMicro project name.
2) `renamed_raw_data`: directory with symbolic links to the original raw file. Links are renamed in the format S0010_1_sequence.fastq etc, where "S0010" would be sample #10 from Maddie's master extraction spreadsheet. Done to simplify naming and make bulk preprocessing simple. Renaming is based on the `simons_mg_samplekey.txt` file, using the script `renamefiles.sh`
3) `overlapped_trimmed_data`: Output of the "metagenome_preprocessing.sh" script. Steps are:
   a: run `cutadapt_1.8.1` to remove any adapter sequences in the raw sequence data
   b: run `clc_overlap_reads` to overlap any paired-end data (min 75 bp output)
   c: run `clc_quality_trim` on nonoverlapping reads to remove low-quality reads/sections of reads (min 75 bp output)


