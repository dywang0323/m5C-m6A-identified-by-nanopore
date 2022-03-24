# m5C-m6A-identified-by-nanopore

A pipline used to identify the m5c and m6A modification using the nanopore DNA and RNA sequencing data

1. Basecalling --> fast5 to fastQ (Guppy). this step will take several hours even several days especially for RNA data

   batch file command:
  
   /ont-guppy-cpu/bin/guppy_basecaller --compress_fastq -i  /*.fast5 --save_path /.fastQ --config /.cfg
     
    output: file.fastq, sequencing_summary.txt
  
    merge all the generated fastQ files together
    
    cat *.fastq > all.fastq
    
    unique the headers in the fastQ file to be unique (code in the "script" folder)
    
    uniquifyFastq input.fastQ input_unique_header
    
    convert T with U without changing headers in the fastQ
    
    awk '/^[^>]/{ gsub(/U/,"T") }1' _unique.fastq > _unique_new_1.fastq
  
 2. Quality control (Minimap2 & Marginalign)
 
    Minimap2 (input: fastq data, genome/transcritome data, output: alighnment data.sam). this step will take several minutes to hours
 
    batch command (minimap2)
    
    genome reads:
    minimap2 -ax map-ont ref.fa ont-reads.fq > aln.sam
    
    direct RNAseq:
    minimap2 -ax splice -uf -k14 ref.fa direct-rna.fq > aln.sam
    
    when using Marginalign, a virtual environment need to be built as below:
    
    module load Python/2.7.14-intel-2018a
    cd marginAlign
    make clean
    make
    virtualenv --python=python2.7 --no-site-packages --distribute env && source env/bin/activate && pip install -r requirements.txt
    
    To calculate the median/avg/min/max identity of reads in a sam file do
    
    marginStats --localAlignment input.sam read.fastq reference.fasta  --readIdentity --alignmentIdentity --readCoverage --mismatchesPerAlignedBase --                     deletionsPerReadBase --insertionsPerReadBase --readLength --printValuePerReadAlignment
    
    To calculate the substitution 
    
    marginAlign/scripts/substitutions _unique.fastq reference.fa _minimap_pass.sam output_directory
    
    *using the script "identityPlots.R" and "substitution_plot.R" to plot the QC results
    
  3. m5C and m6A modification identification
  
   1) prepare the proper files format (samtools)
    
    sam2bam
    
    samtools view -b -S -o output_file.bam _minimap_pass.sam
    
    samtools sort -T tmp -o output_file.sorted.bam output_file.bam
    
    samtools index output.sorted.bam
    
    2) DNA m5C modification detectation
    
    nanopolish index -d output_dir _unique.fastq
    
    nanopolish call-methylation -t 8 -r input.fastq -b inputfile.sorted.bam -g reference.fasta > output.tsv
    
    calculate_methylation_frequency.py output.tsv > m5c_frequency.tsv
    
    3) DNA m6A modification identification
    
    align signal-level events to k-mers of a reference genome
    
    nanopolish index -d /work/schroederrna/methylation/hbecpolya -s sequencing_summary.txt _unique.fastq
    
    nanopolish eventalign --scale-events -n -t 8 --reads _unique_new.fastq --bam input.sorted.bam --genome reference.fa > outputfile_event.tsv
    
    mCaller.py <-m GATC or -p positions.txt> -r <reference>.fasta -d r95_twobase_model_NN_6_m6A.pkl -e <filename>.eventalign.tsv -f <filename>.fastq -b A 
    
    4) RNA m6A modification identfication


    


  
  
  
    






