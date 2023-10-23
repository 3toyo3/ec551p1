# Logic Synthesis Engine

## Files
- ec551p1.py 
  This is the program which is responsible for taking user input and runs the canonical outputs
- program1.py
  This program runs (5-12). This means generating graphics and minimizing expressions
- *.blif

These are demo files

## About
This program takes a blif file, and based on user commands can: 
1. Output the canonical function (POS/SOP)
2. Output the inverse canonical function (POS/SOP)
3. Minimize the function and output the resulting function and how many terms saved (POS/SOP)
4. Print the # of prime implicants, essential prime implicants, onset maxterms and onset minterms
5. Output a graphical Kmap and tabular method representation

A few limitations of this program is that it doesn't recognize blif syntax outside of: names, model, input, outputs. It also can't work with functions that have more than four inputs. 

## How to read the code
The code is seperated into two modules simply due to time.
- ec551p1.py

There are a few comments throughout the code explaining what is happening. First, the blif file is parsed so that the model, inputs, outputs, and names are stored. The most important component here is the names. The program works with multiple '.name' sections. For each name section, a truth table is 
generated and stored within a dictionary entry, with the list of variables as the key. There are two dictionaries used, the first stores the truth table as a list of numerical strings [names], and the second stores it as a 2D array [names_tt]. The program then uses each entry(aka name section) to generate strings for the canonical representations.
- program.py
