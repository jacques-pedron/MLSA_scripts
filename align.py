# -*- coding:utf-8 *-*

import sys
import os
import re

# extract protein sequences from core.80.txt, seq.80.fnodes and sequences.fasta
# align homologous protein sequences with Muscle
# concatenate aligned sequences
# launch by python3 align.py core.80.txt seq.80.fnodes sequences.fasta names.txt
# output file: align.fasta

arg1=sys.argv[1]
arg2=sys.argv[2]
arg3=sys.argv[3]
arg4=sys.argv[4]

print ("reading input files")

# core.80.txt
fichier=open(arg1, 'r')
fam=[]
for line in fichier :
	line=line[:-1]
	fam.append(line)
fichier.close()
fam.sort()

# seq.80.fnodes
fichier=open(arg2, 'r')
nodes=[]
for line in fichier :
	nodes.append(line.split())
fichier.close()
nodes.sort()

# sequences.fasta
fichier=open(arg3, 'r')
fasta=[]
name=""
sequence=""
line=fichier.readline()
while len(line)!=0:
	if line[0]==">": 
		name=line[1:-1]
		line=fichier.readline()
		sequence=line[:-1]
	fasta.append([name,sequence])
	line=fichier.readline()
fichier.close()
fasta.sort()

# names.txt
# output file: align.fasta
fichier=open(arg4, 'r')
names=[]
for line in fichier :
	names.append(line[:-1])
fichier.close()
names.sort()


print ("searching correspondance between homologous families and genes")
begin=0
output=[]
for i in range(len(fam)):
	found=False
	lost=False
	j=begin
	while not lost and j<len(nodes):
		if fam[i]==nodes[j][0]:
			found=True
			output.append(nodes[j])
		else:
			if found:
				lost=True
				begin=j
		j=j+1


print ("extracting homologous protein sequences")
for i in range(len(output)):
	j=0
	found=False
	while not found and j<len(fasta):
		if output[i][1]==fasta[j][0]:
			output[i].append(fasta[j][1])
			found=True
		j=j+1

# removal of gene number
for i in range(len(output)):
	tmp=output[i][1]
	last=tmp[-1:]
	while last !=".":
		tmp=tmp[:-1]
		last=tmp[-1:]
	output[i][1]=tmp[:-1]
	

print ("writing family.fasta files for Muscle alignment")
name=output[0][0]
fichier=open(name+".fasta", "w")
for i in range(len(output)):
	if name==output[i][0]:
		line=">"+output[i][1]+"\n"+output[i][2]+"\n"
		fichier.write(line)
	else:
		name=output[i][0]
		fichier.close()
		fichier=open(name+".fasta", "w")
		line=">"+output[i][1]+"\n"+output[i][2]+"\n"
		fichier.write(line)
fichier.close()


print ("Muscle alignment of family.fasta files")
for name in fam:
	commande="muscle -quiet -in "+name+".fasta -out "+name+".muscle"
	os.system(commande)
	commande="rm "+name+".fasta"
	os.system(commande)


print ("concatenation of .muscle alignment files")

concat=[]
for i in range(len(names)):
	concat.append("")
	
for name in fam:
	fichier=open(name+".muscle", "r")
	tmp=[]
	genome=""
	sequence=""
	for line in fichier:
		if line[0]==">":
			tmp.append([genome, sequence])
			genome=line[1:-1]
			sequence=""
		else:
			sequence=sequence+line[:-1]
	tmp.append([genome, sequence])
	tmp.remove(["",""])
	tmp.sort()
	for i in range(len(concat)):
		concat[i]=concat[i]+tmp[i][1]
	commande=("rm "+name+".muscle")
	os.system(commande)	

fichier=open("align.fasta", "w")

for i in range(len(names)):
	line=">"+names[i]+"\n"+concat[i]+"\n"
	fichier.write(line)

	


	
	


quit()
		
		

		
		
		
		
		