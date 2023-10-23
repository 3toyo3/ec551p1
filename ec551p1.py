import sys
import numpy as np
from collections import defaultdict

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

	#1. return design as a canonical sop
	if command == "1":
		sops = sop_c()
		print(sops)
	#2. return design as a canonical pos
	elif command == "2":
		poss = pos_c()
		print(poss)
	#3. return design as a inverse canonical sop
	elif command == "3":
		sops = sop_c()
		print(sops)
		inverted = inverse_sop(sops)
		print(inverted)
	#4. return design as a inverse canonical pos
	elif command == "4":
		poss = pos_c()
		inverted = inverse_pos(poss)
		print(inverted)
	#5. return a minimized number of literals representation in sop
	elif command == "5":
		print("five")
	#6. return a minimized number of literals representation in pos
	elif command == "6":
		print("six")
	#7. return the number of prime implicants
	elif command == "7":
		print("seven")
	#8. return the number of essential prime implicants
	elif command == "8":
		print("eight")
	#9. return number of on-set minterms
	elif command == "9":
		print("nine")
	#10. return number of on-set maxterms
	elif command == "10":
		print("ten")
	#11. prints out KMap representation
	elif command == "11":
		print("eleven")
	#12. prints out tabular method table representation
	elif command == "12":
		print("twelve")
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
			#store each "module" of blif in the case of multiple outputs
			elif line.startswith(".names"):
				currentname = line[len(".names"):].strip()
			elif line.startswith(".end"):
				break
			elif currentname is not None:
				names[currentname].append(line.rstrip())
			else:
				pass
	truet() # finish cleaning by turning rows into tt

def truet(): #make truth table for each name, clean up lines and expand to master copy :)
	global names
	for entry in names:
		truet = []
		#get true values of the chart
		for lines in names[entry]:
			cleanline = lines.rstrip()
			if cleanline.endswith('1'):
				cleanline = cleanline[:-1].rstrip()
				truet.append(cleanline)
		expanded=[]
		ref_truet = truet[:]

		#expand dont cares
		for row in ref_truet:
			if '-' in row:
				expand_row = list(row)
				truet.remove(row) #check that this removes properly IE not messing up index

				#replace multiple dont cares
				for i, char in enumerate(expand_row):
					if char == '-':
						expand_row[i]='0'
						expanded.append(''.join(expand_row))
						expand_row[i]='1'
						expanded.append(''.join(expand_row))
		ref_truet.clear()

		# add back expanded and put in ref for later
		truet.extend(expanded)
		print("Truth table for " + entry)
		truet = list(set(truet)) #removes dupes
		print(truet)
		names[entry] = truet

def tt_translate(): #translates from list/string representation to 4D array
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
					print("Something is wrong!!")
				if i == len(row) -1:
					row_dupe[i] = row_dupe[i][:-1] #removes last * by slicing
			canoneqn +=''.join(row_dupe)+" + "
		canoneqn = canoneqn[:-3] #removes last plus by slicing
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
