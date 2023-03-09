# m5C-m6A-identified-by-nanopore

# A pipline used to identify the m5c and m6A modification using the nanopore DNA and RNA sequencing data

# Basecalling
--> fast5 to fastQ (Guppy). this step will take several hours even several days especially for RNA data

   batch file command:
  
   /ont-guppy-cpu/bin/guppy_basecaller --compress_fastq -i  /*.fast5 --save_path /.fastQ --config /.cfg
   
   you also can run the Guupy in the paralel way by adjusting the batch file:
   
   > #SBATCH --output=array_%A_%a.out

   > #SBATCH --error=array_%A_%a.err

   > #SBATCH --array=239-620

   echo "My SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID
   
   guppy_basecaller -i / FAO44045_pass_768f8f04_${SLURM_ARRAY_TASK_ID}.fast5 --save_path /fastQ_1 --config /.cfg
     
    output: file.fastq, sequencing_summary.txt
  
    merge all the generated fastQ files together
    
    cat *.fastq > all.fastq
    
    unique the headers in the fastQ file to be unique (code in the "script" folder)
    
    uniquifyFastq input.fastQ input_unique_header
    
    convert T with U without changing headers in the fastQ
    
    awk '/^[^>]/{ gsub(/U/,"T") }1' _unique.fastq > _unique_new_1.fastq
  
 # Quality control (Minimap2 & Marginalign)
 
    Minimap2 (input: fastq data, genome/transcritome data, output: alighnment data.sam). this step will take several minutes to hours
 
    batch command (minimap2)
    
    genome reads:
    minimap2 -ax map-ont ref.fa ont-reads.fq > aln.sam
    
    direct RNAseq:
    minimap2 -ax splice -uf -k14 ref.fa direct-rna.fq > aln.sam
    
    usually ONT reads were align to the genome (for human: Ensembl primary assembly GRCh38) and transcripttome (combined cDNA and ncRNA reference fasta                            file from Ensembl GECH38.90)
    for the genome alignment, alignment files from minimap2 were converted to bam format, sorted and indexed using samtools. the Bioconductor package Genomic Alignments(v1.32.0) was used to extract juctions from the alignments. for each observed juction, we calculated the distance to the closest annotated juction(the absolute difference between the start positions plus the obsolute difference between the end position)
    for the transcriptome alignments, we used arguments -ax map-ont-N100 to allow more secondary alignments, given the hign similarity among trascript isoforms.
     
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
    
  # m5C and m6A modification identification
  
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
    
    The software "xpore" or "m6anet" can be used to identify the m6A modification without well trained model
    torch==1.6.0 must be installed:
    
    pip install torch==1.6.0 torchvision==0.7.0 --user
   
    if there's issue on the installation, the below way may be help
    some tips to install the xpore & m6anet
    ->deactivate the export PATH in .bashrc
      $cd $HOME
      $nano .bashrc
    ->deactivate the anaconda
      $conda deactivate
    -> create the virtual environment and reinstall the software
      $python3 -m venv m6anet
      $source ./m6anet/bin/activate
      $pip install m6anet
      $pip install xpore      
    ->restart the terminal
    ->type the command agin
      $conda deactivate
      $source ./m6anet/bin/activate
      $module load python
      
      We use m6anet as example: (Python 3.9.5 was tested to be working, tpdm have to be installed)
      1) prepare the eventalign.txt file from nanopolish
      $nanopolish index -d /work_dir -s /sequencing_summary.txt /reads.fastq
      $nanopolish eventalign --reads /reads.fastq --bam /reads.sorted.bam 
      --genome /transcriptome_reference.fa --scale-events --signal-index 
      --summary/sequencing_summary.txt 
      --threads 50 
      > /eventalign.txt
      2)preprocess the segmented raw signal file in the form of nanopolish eventalign file (this step takes several hours)
      $m6anet-dataprep --eventalign /eventalign.txt --out_dir /output_dir --n_processes 4
      3)m6anet-run_inference --input_dir /input_dir --out_dir /output_dir --infer_mod_rate --n_processes 4
      
 # m6A modification comparision (Xpore)
      1) Preprocess the data for each data set
      $ xpore dataprep --eventalign /hbecpolya_eventalign.txt --out_dir /output_dir
      2) Pairwise comparison
      .yml formate configure file is needed in this step,please find the example in the scripts folder
      $xpore diffmod --config config.yml
   
      
      


      
      Run the EEF.PY script, using outputfile_event.tsv as input
      
      selecte out the interested k-mer
      awk '$10=="GGACA"' file_in.txt > file_out.txt
      remove the header from the EEF file from IVT data
      awk 'NR>1' EEF.txt > EEF_new.txt
      replace "modified" with "unmodified"
      sed 's/modified/unmodified/g' EEF_new.txt
      
      Run current_movement_plot.R script to identify the movement of current density 
      
# GO annotation
Extract the reads that have been aligned to the reference
 
$samtools view -F 0x4 file.sam > /aligned_reads.sam
 
 


      
      


    


  
  
  
    






