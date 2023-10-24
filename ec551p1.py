import sys
import numpy as np
from collections import defaultdict
from program1 import *

model = ""
inputs = []
outputs = []
names = defaultdict(list)
names_tt = {}

def main():
	if len(sys.argv) != 3:
		print("Usage: python ec551p1.py <file> <1-12>")
		sys.exit()
	else:
		filename = sys.argv[1]
		command = sys.argv[2]
	#TODO check if file exists

	#TODO make it so that can continually output answers

	# set up program from file
	parser(filename)

	#1. return design as a canonical sop
	if command == "1":
		sops = sop_c()
		print("Canonical SOP:")
		print(sops)
	#2. return design as a canonical pos
	elif command == "2":
		poss = pos_c()
		print("Canonical POS:")
		print(poss)
	#3. return design as a inverse canonical sop
	elif command == "3":
		sops = sop_c()
		inverted = inverse_sop(sops)
		print("Inverted SOP:")
		print(inverted)
	#4. return design as a inverse canonical pos
	elif command == "4":
		poss = pos_c()
		inverted = inverse_pos(poss)
		print("Inverted POS:")
		print(inverted)
	#5. return a minimized number of literals representation in sop
	elif command == "5":
		print("Minimized SOP(s):")
		for entry in names_tt:
			truthtable = names_tt[entry]
			sample = prime_implicants(names_tt[entry])
			sample1 = essential_prime_implicants(sample,truthtable)
			preserved_prime_implicants = sample.copy()
			print(format_sop(choose_terms(sample,sample1,truthtable)))
	#6. return a minimized number of literals representation in pos
	elif command == "6":
		print("Minimized POS(s):")
		for entry in names_tt:
			truthtable = names_tt[entry]
			print("Saved literals:")
			sample_inv=prime_implicants(inv(truthtable))
			sample_inv1=essential_prime_implicants(sample_inv,truthtable)
			print(format_pos(choose_terms(sample_inv,sample_inv1,inv(truthtable))))
	#7. return the number of prime implicants
	elif command == "7":
		for entry in names_tt:
			truthtable = names_tt[entry]
			sample=prime_implicants(truthtable)
			sample1=essential_prime_implicants(sample,truthtable)
			preserved_prime_implicants=sample.copy()
			print("There are "+str(len(preserved_prime_implicants)+len(sample1))+" prime implicants for: "+entry)
	#8. return the number of essential prime implicants
	elif command == "8":
		for entry in names_tt:
			truthtable = names_tt[entry]
			sample=prime_implicants(truthtable)
			sample1=essential_prime_implicants(sample,truthtable)
			print("There are "+str(len(sample1))+" essential prime implicants for: "+entry)
	#9. return number of on-set minterms
	elif command == "9":
		for entry in names_tt:
			truthtable = names_tt[entry]
			print('There are '+str(count_terms(truthtable)[0])+' On-set minterms for: '+entry)
	#10. return number of on-set maxterms
	elif command == "10":
		for entry in names_tt:
			truthtable = names_tt[entry]
			print('There are '+str(count_terms(truthtable)[1])+' On-set maxterms for: '+entry)
	#11. K Map
	elif command == "11":
		for entry in names_tt:
			truthtable = names_tt[entry]
			print(" KMap for: "+entry)
			print_truthtable(truthtable)
			print()
			print()
	#12. Coverage Table
	elif command == "12":
		for entry in names_tt:
			truthtable = names_tt[entry]
			sample=prime_implicants(truthtable)
			sample1=essential_prime_implicants(sample,truthtable)
			preserved_prime_implicants=sample.copy()
			print(" Coverage table for: "+entry)
			print_coverage_table(preserved_prime_implicants, sample1,truthtable)
			print()
			print()
	else:
		print("Unknown command: ", command)
		sys.exit()

def parser(filename):
	global model
	global inputs
	global outputs
	global names
	currentname = None
	with open(filename, "r") as file:
		for line in file:
			if line.startswith(".model"):
				model += line[len(".model"):].strip()
				print("Model: " + model)
			elif line.startswith(".inputs"):
				ins = line[len(".inputs"):].strip().split()
				inputs.extend(ins)
				print("Inputs: " + ", ".join(str(i) for i in inputs))
			elif line.startswith(".outputs"):
				outs = line[len(".outputs"):].strip().split()
				outputs.extend(outs)
				print("Outputs: "+ ", ".join(str(i) for i in outputs))
			#store each "module" of blif in the case of multiple outputs
			elif line.startswith(".names"):
				currentname = line[len(".names"):].strip()
			elif line.startswith(".end"):
				break
			elif currentname is not None:
				names[currentname].append(line.rstrip())
			else:
				pass
	truet() #string/list representation for names dictionary
	tt_translate() #array representation for names_tt dictionary
	print()

def truet(): #make truth table for each name, clean up lines and expand for list representation
	global names
	for entry in names:
		truet = []
		#get true values of the chart
		for lines in names[entry]:
			cleanline = lines.rstrip()
			if cleanline.endswith('1'):
				cleanline = cleanline[:-1].rstrip()
				truet.append(cleanline)

		ref_truet = truet[:]

		#expand dont cares
		for row in ref_truet:
			expanded = []
			if '-' in row:
				hyphenate = []
				hyphenate.append(row)
				truet.remove(row)

				hyphen = 2**row.count('-') #possibilities
				#replace multiple dont cares
				while len(expanded) != hyphen:
					expand_row = list(hyphenate.pop(0))
					x = expand_row.index('-')
					expand_row[x]='0'
					if expand_row.count('-')==0:
						expanded.append(''.join(expand_row))
						expand_row[x]='1'
						expanded.append(''.join(expand_row))
					else:
						hyphenate.append(''.join(expand_row))
						expand_row[x]='1'
						hyphenate.append(''.join(expand_row))
			truet.extend(expanded)
		ref_truet.clear()

		# add back expanded and put in ref for later
			#truet.extend(expanded)
		#print("Truth table for " + entry)
		truet = list(set(truet)) #removes dupes
		#print(truet)
		names[entry] = truet

def tt_translate(): #translates from list/string representation to 4D array
	global names
	global names_tt
	for entry in names: # variable count check
		truthtable=np.zeros((2,2,2,2))
		if len(names[entry][0]) < 4:
			if len(names[entry][0]) == 2:
				for row in names[entry]:
					A = int(row[0])
					B = int(row[1])
					truthtable[A][B][0][0] = 1
					truthtable[A][B][0][1] = 1
					truthtable[A][B][1][1] = 1
					truthtable[A][B][1][0] = 1
			elif len(names[entry][0]) == 3:
				for row in names[entry]:
					A =int(row[0])
					B = int(row[1])
					C = int(row[2])
					truthtable[A][B][C][0] = 1
					truthtable[A][B][C][1] = 1
			elif len(names[entry][0]) == 1:
				for row in names[entry]:
					A = int(row[0])
					truthtable[A][0][0][0] = 1
					truthtable[A][0][0][1] = 1
					truthtable[A][0][1][1] = 1
					truthtable[A][0][1][0] = 1
					truthtable[A][1][0][0] = 1
					truthtable[A][1][0][1] = 1
					truthtable[A][1][1][1] = 1
					truthtable[A][1][1][0] = 1
			else:
				print("Something is wrong in TT translation")

		elif len(names[entry][0]) == 4: #if equal to 4
			for row in names[entry]:
				A = int(row[0])
				B = int(row[1])
				C = int(row[2])
				D = int(row[3])
				truthtable[A][B][C][D] = 1
		else:
			printf("Representing this into a 4x4 array is beyond this program.")
		names_tt[entry] = truthtable

def sop_c(): #turns truet into a string with accurate variable names
	global names
	canonicals = []
	for entry in names:
		canoneqn = ""
		variables = entry.split()
		canoneqn += f"{variables[-1]}= "
		variables.pop() #remove output
		for row in names[entry]:
			row_dupe = list(row)
			for i in range(len(row)): 
				if row[i] == '1':
					row_dupe[i] = variables[i] + "*"
				elif row[i] == '0': 
					row_dupe[i] = variables[i] + "'*"
				else:
					print("Something is wrong in SOP generation")
				if i == len(row) -1:
					row_dupe[i] = row_dupe[i][:-1] #removes last * by slicing
			canoneqn +=''.join(row_dupe)+" + "
		canoneqn = canoneqn[:-3] #removes last plus by slicing
		canonicals.append(canoneqn)
	return canonicals

def pos_c(): #turns TT into POS
	canonicals = []
	global names_tt
	for entry in names_tt:
		canoneqn = ""
		maxterms=[]
		variables = entry.split()
		canoneqn += f"{variables[-1]}= ("
		variables.pop()

		tt = names_tt[entry]
		#gather max terms
		if len(variables) == 4:
			for A in range(2):
				for B in range(2):
					for C in range(2):
						for D in range(2):
							if tt[A][B][C][D] == 0:
								maxterms.append(str(A)+str(B)+str(C)+str(D))
		elif len(variables) == 3:
			D = 0
			for A in range(2):
				for B in range(2):
					for C in range(2):
						if tt[A][B][C][D] == 0:
							maxterms.append(str(A)+str(B)+str(C))
		elif len(variables) == 2:
			C = 0
			D = 0
			for A in range(2):
				for B in range(2):
					if tt[A][B][C][D] == 0:
						maxterms.append(str(A)+str(B))
		else:
			print("Something is wrong in POS")
		maxterms=list(set(maxterms))
		#turn to a string
		for term in maxterms:
			term_dupe = list(term)
			for i in range(len(term)):
				if term[i] == '1':
					term_dupe[i] = variables[i]
				elif term[i] == '0':
					term_dupe[i] = variables[i]+"'"
				else:
					print("Something is wrong in POS during text translation")
			canoneqn +='+'.join(term_dupe)+")("
		canoneqn = canoneqn[:-1]
		canonicals.append(canoneqn)
	return canonicals

def inverse_sop(sops): #takes the SOP string and inverts the literals
	inverts = []
	for line in sops:
		inverted = ""
		for i in range(len(line)-1):
			if line[i].isalpha():
				if i == 0: #checks if the output
					new = line[i].casefold()
					inverted+=new
				elif line[i+1] == '*':
					new = line[i]+"'" #end of literal
					inverted+=new
				elif line[i+1] == " ": #end of minterm
					new = line[i]+"'"
					inverted+=new
				elif i == len(line)-1: #avoids skipping last letter
					new = line[i]+"'"
					inverted+=new
				else:
					new = line[i]
					inverted+=new
			elif line[i] == "'":
				pass
			else:
				new = line[i]
				inverted+=new
		inverts.append(inverted)
	return inverts

def inverse_pos(poss): #takes the POS string and inverts the literals
	inverts  = []
	for line in poss:
		inverted = ""
		for i in range(len(line)-1):
			if line[i].isalpha():
				if i == 0:
					new = line[i].casefold()
					inverted+=new
				elif line[i+1] == "+": #end of literal
					new = line[i]+"'"
					inverted+=new
				elif line[i+1] == ")": #end of maxterm
					new = line[i]+"'"
					inverted+=new
				else:
					inverted+=line[i]
			elif line[i] == "'":
				pass
			else:
				inverted+=line[i]
		inverted+=line[-1]
		inverts.append(inverted)
	return inverts

if __name__ == "__main__":
	main()
