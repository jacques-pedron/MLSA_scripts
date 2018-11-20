# -*- coding:utf-8 *-*

import sys
import os

# convert .fnodes output file from SiLix
# launch by python3 core.py seq.80.fnodes names.txt
# output file: fam.80.txt


arg1=sys.argv[1]
arg2=sys.argv[2]


# reading .fnodes file
print("reading", arg1)
fichier=open(arg1, 'r')
nodes=[]
for line in fichier :
	colonnes=line.split()
	nodes.append(colonnes)
fichier.close()
nodes.sort()


# reading name.txt file
print ("reading", arg2)
fichier=open(arg2, 'r')
species=[]
for line in fichier :
	line=line[:-1]
	species.append(line)
fichier.close()


# counting genes for each family / species
print ("counting genes for each family / species")
output=[]
fam=nodes[0][0]
line=[fam]
for j in range(len(species)):
	line.append(0)

for i in range(len(nodes)):
	if nodes[i][0]!=fam:
		output.append(line)
		fam=nodes[i][0]
		line=[fam]
		for j in range(len(species)):
			line.append(0)
	for k in range(len(species)):
		if species[k] in nodes[i][1]:
			line[k+1]+=1
				

# writing fam.80.txt output file
print ("writing fam.80.txt output file")
fichier=open("fam.80.txt", "w")
line=""

for i in range(len(species)):
	line=line+"\t"+species[i]
line=line+"\n"
fichier.write(line)

for i in range(len(output)):
	line=""
	for j in range(len(output[i])):
		line=line+str(output[i][j])+"\t"
	line=line[:-1]+"\n"
	fichier.write(line)

fichier.close()

quit()

