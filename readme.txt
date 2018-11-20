Dependancies:

Python version 3.7.1

Blast version 2.6.0. To install:

conda install blast 

SiLix version 1.2.9. Dowloading: http://lbbe.univ-lyon1.fr/Download.html
To install:

tar zxvf silix-1.x.x.tar.gz
cd silix-1.x.x
./configure
make
make check
make install

Muscle version 3.8.1551
To install:

conda install muscle







Predicted nucleotide protein sequences (.fasta) of all genomes located in the sequences/ directory are first concatenated in a single fasta file (sequences.fasta):

cat sequences/* | awk '/^>/ {print "\n"$0} /^[a-z]/ {printf $0} /^[A-Z]/ {print $0}' > sequences.fasta

The next command generates a names.txt file containing names of genomes:

ls sequences/ | sed 's/.fasta//g' > names.txt

The sequences.fasta file is used to create a Blastp database:

makeblastdb -in sequences.fasta -dbtype nucl -out dbblastall

A Blastn all vs all is then performed:

blastn -db dbblastall -query sequences.fasta -outfmt 6 -out blastall.blastn -num_threads 8 -evalue 0.00001

The blastp outut (blastall.blastn file) is then processed by the SiLix software that clusters homologous genes in families with a 80% threshold. SiLix generates the seq.80.fnodes file:

silix sequences.fasta blastall.blastn -f FAM -i 0.80 > seq.80.fnodes

The seq.80.fnodes is processed with the python script core.py that generates a matrix (output fam.80.txt file) with species in columns and number of homologous genes in rows. The script needs the seq.80.fnodes and names.txt files as arguments:

python3 core.py seq.80.fnodes names.txt

The homologous.py script then searches for homologous genes present in all genomes (core genome). The core.80.txt output file is a list of homologous families:

python3 homologous.py fam.80.txt

The align.py script extracts homologous sequences, aligns with Muscle and concatenates aligned sequences. The output file is align.fasta:

python3 align.py core.80.txt seq.80.fnodes sequences.fasta names.txt

Molecular phylogeny is performed by using the multiplatform GUI Seaview software version 4.6.5. Input file is the align.fasta alignment. First, alignment is curated by Gbloks tool with default parameters to remove all gaps or X positions. Phylogeny is performed with PhyML algorithm with the following settings: substitution model GTR, 100 bootstraps, nucleotide equilibrium frequencies, invariable sites optimized, tree searching NNI, starting tree BioNJ.


