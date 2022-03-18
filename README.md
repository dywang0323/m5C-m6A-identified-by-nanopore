# m5C-m6A-identified-by-nanopore

A pipline used to identify the m5c and m6A modification using the nanopore DNA and RNA sequencing data

1. Basecalling --> fast5 to fastQ (Guppy). this step will take several hours even several days especially for RNA data

    batch file command:
    /ont-guppy-cpu/bin/guppy_basecaller --compress_fastq -i  /*.fast5 --save_path /.fastQ --config /.cfg
     
    output: file.fastq, sequencing_summary.txt
  
    merge all the generated fastQ files together
    
    cat *.fastq > all.fastq
  
 2. Quality control (Minimap2 & Marginalign)
 
    Minimap2 (input: fastq data, genome/transcritome data, output: alighnment data.sam). this step will take several minutes to hours
 
    batch command (minimap2)
    
    genome reads:
    minimap2 -ax map-ont ref.fa ont-reads.fq > aln.sam
    
    direct RNAseq
    minimap2 -ax splice -uf -k14 ref.fa direct-rna.fq > aln.sam
    
 


