# m5C-m6A-identified-by-nanopore
A pipline used to identify the m5c and m6A modification using the nanopore DNA and RNA sequencing data

1. Basecalling --> fast5 to fastQ (Guppy). this process will take several hours even several days especially for RNA data

  batch file command:

  /ont-guppy-cpu/bin/guppy_basecaller --compress_fastq -i  /*.fast5 --save_path /.fastQ --config /.cfg


