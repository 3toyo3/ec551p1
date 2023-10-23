import sys
import numpy as np
from collections import defaultdict
from program1 import *

# assumes that the file format is a certain way, as well as in the same directory
# will output as blif in <blah blah .txt>


#TODO: quinemcklusky, sop, demorgans, address the todos and clean, make for a circuit

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

	#TODO clean outputs here, check input outputs
	#1. return design as a canonical sop
	if command == "1":
		sops = sop_c()
		print(sops)
	#2. return design as a canonical pos
	elif command == "2":
		poss = pos_c()
		print(poss)
	#3. return design as a inverse canonical sop
	elif command == "3":   #TODO check
		sops = sop_c()
		print(sops)
		inverted = inverse(sops)
		print(inverted)
	#4. return design as a inverse canonical pos
	elif command == "4":
		poss = pos_c()
		inverted = inverse(poss)
		print(inverted)
	#5. return a minimized number of literals representation in sop
	elif command == "5":
		print("five")
		print("Saved literals:")
		sample=prime_implicants(truthtable)
		sample1=essential_prime_implicants(sample)
		print(format_sop(choose_terms(sample,sample1,truthtable)))
		
	#6. return a minimized number of literals representation in pos
	elif command == "6":
		print("six")
		print("Saved literals:")
		sample_inv=prime_implicants(inv(truthtable))
		sample_inv1=essential_prime_implicants(sample_inv)
		print(format_pos(choose_terms(sample_inv,sample_inv1,inv(truthtable))))
	#7. return the number of prime implicants
	elif command == "7":
		print("seven")
		sample=prime_implicants(truthtable)
		sample1=essential_prime_implicants(sample)
		preserved_prime_implicants=sample.copy()
		print("There are "+str(len(preserved_prime_implicants)+len(sample1))+" prime implicants")
		
	#8. return the number of essential prime implicants
	elif command == "8":
		print("eight")
		sample=prime_implicants(truthtable)
		sample1=essential_prime_implicants(sample)
		print("There are "+str(len(sample1))+" essential prime implicants")
	
	#9. return number of on-set minterms
	elif command == "9":
		print("nine")
		print('There are '+str(count_terms(truthtable)[0])+' On-set minterms')
	#10. return number of on-set maxterms
	elif command == "10":
		print("ten")
		print('There are '+str(count_terms(truthtable)[1])+' On-set maxterms')
	#11. K Map
	elif command == "11":
		print("eleven")
		print_truthtable(truthtable)
	#12. Coverage Table
	elif command == "12":
		print("twelve")
		sample=prime_implicants(truthtable)
		sample1=essential_prime_implicants(sample)
		preserved_prime_implicants=sample.copy()
		print_coverage_table(preserved_prime_implicants, sample1,truthtable)
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
				print("Model:" + model)
			elif line.startswith(".inputs"):
				ins = line[len(".inputs"):].strip().split()
				inputs.extend(ins)
				print("Inputs:")
				print(inputs)
			elif line.startswith(".outputs"):
				outs = line[len(".outputs"):].strip().split()
				outputs.extend(outs)
				print("Outputs:")
				print(outputs)
			#store each "module" of blif
			elif line.startswith(".names"):
				currentname = line[len(".names"):].strip()
				#print(currentname)
			elif line.startswith(".end"):
				break
			elif currentname is not None:
				#print("Current line: "+ line )
				names[currentname].append(line.rstrip())
				#print(names[currentname])
			else:
				pass
	truet() # finish cleaning by turning rows into tt

def truet(): #make truth table for each name, clean up lines and expand to master copy :)
	global names
	for entry in names:
		truet = []
		#print(entry)

		#get true values of the chart
		for lines in names[entry]:
			cleanline = lines.rstrip()
			#print("Cleaned line: "+ cleanline)
			if cleanline.endswith('1'):
				cleanline = cleanline[:-1].rstrip()
				#print(cleanline, " with True removed")
				tt.append(cleanline)
		#print("Truth table for :" + entry)
		#print(tt)

		expanded=[]
		ref_truet = truet[:]

		#look for minimized functions
		for row in ref_truet:
			#print("Working on: " + row)
			if '-' in row:
				expand_row = list(row)
				truet.remove(row) #check that this removes properly IE not messing up index
				#replace multiple dont cares
				for i, char in enumerate(expand_row):
					if char == '-':
						expand_row[i]='0'
						#print(expand_row)
						expanded.append(''.join(expand_row))
						expand_row[i]='1'
						expanded.append(''.join(expand_row))
						#print(expand_row)
		ref_truet.clear()

		# add back expanded and put in ref for later
		truet.extend(expanded)
		print("Truth table for " + entry)
		#print(tt)
		truet = list(set(truet)) #removes dupes
		print(truet)
		#TODO maybe convert to binary
		names[entry] = truet

def tt_translate():
	global names
	global names_tt
	for entry in names: # variable count check
		truthtable=np.zeros((2,2,2,2))
		if len(names[entry][0]) < 4:
			if len(names[entry][0] == 2):
				for row in names[entry]:
					A = row[0]
					B = row[1]
					truthtable[A][B][0][0] = 1
					truthtable[A][B][0][1] = 1
					truthtable[A][B][1][1] = 1
					truthtable[A][B][1][0] = 1
			elif len(names[entry][0] == 3):
				for row in names[entry]:
					A = row[0]
					B = row[1]
					C = row[2]
					truthtable[A][B][C][0] = 1
					truthtable[A][B][C][1] = 1
			elif len(names[entry][0] == 1):
				for row in names[entry]:
					A = row[0]
					truthtable[A][0][0][0] = 1
					truthtable[A][0][0][1] = 1
					truthtable[A][0][1][1] = 1
					truthtable[A][0][1][0] = 1
					truthtable[A][1][0][0] = 1
					truthtable[A][1][0][1] = 1
					truthtable[A][1][1][1] = 1
					truthtable[A][1][1][0] = 1
			else:
				print("Something is wrong line 193")
	
		elif len(names[entry][0] == 4): #if equal to 4
			for row in names[entry]:
				A = row[0]
				B = row[1]
				C = row[2]
				D = row[3]
				truthtable[A][B][C][D] = 1
		else:
			printf("Representing this into a 4x4 array is beyond this program.")
		names_tt[entry] = truthtable

def sop_c():
	global names
	canonicals = []
	for entry in names:
		canoneqn = ""
		variables = entry.upper().split()
		#print(entry)
		#print(names[entry])

		canoneqn += f"{variables[-1]}="
		variables.pop() #remove output

		for row in names[entry]:
			#print(row)
			row_dupe = list(row)
			#TODO think more
			for i in range(len(row)): 
				if row[i] == '1':
					row_dupe[i] = variables[i]
				elif row[i] == '0': #Lower to rep 0 value
					row_dupe[i] = variables[i].lower()
				else:
					print("Something is wrong!!")
			#print(row_dupe)
			canoneqn +=''.join(row_dupe)+"+"
		canoneqn = canoneqn[:-1] #remove last plus
		canonicals.append(canoneqn)
	return canonicals

def pos_c(): #TODO make into variable names FIX
	canonicals = []
	global names
	for entry in names:
		canonicaleqn = "G=("
		for row in names[entry]:
			print(row)
			row_dupe = '+'.join(row)
			for i in range(len(row_dupe)):
				if row_dupe[i] == 1:
					row_dupe[i] = 0
				elif row_dupe[i] == 0:
					row_dupe[i] = 1
				else:
					pass
			canonicaleqn += row_dupe +")("
		canonicaleqn = canonicaleqn[:-1]
		canonicals.append(canonicaleqn)
	return canonicals

#def demorgan(): #idk if i need to do this afterall

def inverse(output): #input the sop or pos things
	inverts = []
	for line in output: 
		inverted = line.swapcase()
		inverts.append(inverted)
	return inverts

#def minimizer(): #shout out quinemckluskey

#TODO onset minterms, onset maxterms, 11 and 12

# 11 kmap
# 12 hazards

if __name__ == "__main__":
	main()
 
