# -*- coding:utf-8 *-*

import sys
import os

# extract homologous families from fam.80.txt
# launch by python3 homologous.py fam.80.txt
# output file: core.80.txt

arg1=sys.argv[1]

# fam.80.txt reading
print("reading", arg1, "file")
fichier=open(arg1, 'r')
fam=[]

for line in fichier :
	line=line[:-1]
	colonnes=line.split("\t")
	fam.append(colonnes)
fichier.close()
del fam[0]

# conversion to binary matrix
print("conversion to binary matrix")
for i in range(len(fam)):
	for j in range(1, len(fam[i])):
		if int(fam[i][j])>0:
			fam[i][j]=1

# search for homologous genes
print("search for homologous genes")
homol=[]
n=len(fam[0])-1
for i in range(len(fam)):
	sum=0
	for j in range(1, len(fam[i])):
		sum=sum+int(fam[i][j])
	if sum==n:
		homol.append(fam[i][0])

# output writing
print("writing core.80.txt output file")
fichier=open("core.80.txt", "w")
for i in range(len(homol)):
	line=homol[i]+"\n"
	fichier.write(line)
fichier.close()