import sys
from collections import defaultdict

# assumes that the file format is a certain way, as well as in the same directory
# will output as blif in <blah blah .txt>


#TODO: quinemcklusky, sop, demorgans, address the todos and clean, make for a circuit

model = ""
inputs = []
outputs = []
names = defaultdict(list)

if __name__ == "__main__":
	main()


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
		sop_c()
	#2. return design as a canonical pos
	else if command == "2":
		print("two")
	#3. return design as a inverse canonical sop
	else if command == "3":
		print("three")
	#4. return design as a inverse canonical pos
	else if command == "4":
		print("four")
	#5. return a minimized number of literals representation in sop
	else if command == "5":
		print("five")
		print("Saved literals:")
	#6. return a minimized number of literals representation in pos
	else if command == "6":
		print("six")
		print("Saved literals:")
	#7. return the number of prime implicants
	else if command == "7":
		int primp = 0
		print("seven")
	#8. return the number of essential prime implicants
	else if command == "8":
		print("eight")
	#9. return number of on-set minterms
	else if command == "9":
		print("nine")
	#10. return number of on-set maxterms
	else if command == "10":
		print("ten")
	#11. ???
	else if command == "11":
		print("eleven")
	#12. ???
	else if command == "12":
		print("twelve")
	else:
		print("Unknown command: ", command)
		sys.exit()

def parser(filename):
	currentname = None
	with open(filename, "r") as file:
		for line in file:
			if line.startswith(".model"):
				model += line[len(".model"):].strip()
				print(model)
			elif line.startswith(".inputs"):
				ins = line[len(".inputs"):].strip().split()
				inputs.extend(ins)
				print(inputs)
			elif line.startswith(".outputs"):
				outs = line[len(".outputs"):].strip().split()
				outputs.extend(outs)
				print(outputs)
			#store each "module" of blif
			elif line.startswith(".names"):
				currentname = line[len(".names"):].strip()
				print(currentname)
			elif line.startswith(".end"):
				break
			elif currentname is not None:
				names[currentname].append(line)
				print(names[currentname])
			else:
				pass
	tt() # finish cleaning by turning rows into tt

def tt(): #make truth table for each name, clean up lines and expand to master copy :)
	for entry in names:
		tt = []
		print(entry + "," names[entry])

		#get true values of the chart
		for lines in names[entry]:
			cleanline = lines.rstrip()
			print(cleanline)
			if cleanline.endswith('1')
				cleanline = cleanline[:-1].rstrip()
				print(cleanline, " with True removed")
				tt.append(cleanline)
		print(tt)

		#TODO check that number of variables match length?

		expanded=[]
		ref_tt = tt[:] #TODO make sure this copies

		#look for minimized functions
		for row in ref_tt:
			print(row)
			if '-' in row: #TODO make sure right characters
				expand_row = row
				tt.remove(row) #check that this removes properly IE not messing up index
				#replace multiple dont cares
				for i, char in enumerate(expand_row):
					if char == '-':
						expand_row[i]='0'
						print(expand_row)
						expanded.append(expand_row)
						expand_row[i]='1'
						expanded.append(expand_row)
						print(expand_row)
		ref_tt.clear()

		# add back expanded and put in ref for later
		tt.append(expanded)
		tt = list(set(tt)) #TODO check that this removes dupes
		print(tt)
		#TODO maybe convert to binary
		names[entry] = tt

def sop_c():
	canonicals = []
	for entry in names:
		canoneqn = ""
		variables = entry.split().upper()
		print(entry + "," names[entry])

		canoneqn += f"{variables[-1]}="
		variables.pop() #remove output

		for row in names[entry]:
			print(row)
			row_dupe = row
			#TODO think more
			for i in range(len(row)): #TODO get rid of *
				if row[i] == '1':
					row_dupe[i] = variable[i]
				elif row[i] == '0': #Lower to rep 0 value
					row_dupe[i] = variable[i].lower()
				else
					print("Something is wrong!!")
			print(row_dupe)
			canoneqn += row_dupe+"+"
		canoneqn = canoneqn[:-1] #remove last plus
		canonicals.append(canoneqn) #TODO or return canonical
	return canonicals

def pos_c():
	canonicals = []
	for entry in names:
		#ccc
		#demorgans

def demorgan(): 

def inverse(output): #input the sop or pos things
	inverts = []
	for line in output: 
		inverted = line.swapcase()
		inverts.append(inverted)
	return inverts

def minimizer(): #shout out quinemckluskey
