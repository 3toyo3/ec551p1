import numpy as np


#For testing
#truthtable=np.zeros((2,2,2,2))
#truthtable[0][0][0][0]=0
#truthtable[0][0][0][1]=0
#truthtable[0][0][1][0]=0
#truthtable[0][0][1][1]=0

#truthtable[0][1][0][0]=0
#truthtable[0][1][0][1]=0
#truthtable[0][1][1][0]=1
#truthtable[0][1][1][1]=0

#truthtable[1][0][0][0]=1
#truthtable[1][0][0][1]=0
#truthtable[1][0][1][0]=0
#truthtable[1][0][1][1]=1

#truthtable[1][1][0][0]=0
#truthtable[1][1][0][1]=1
#truthtable[1][1][1][0]=0
#truthtable[1][1][1][1]=0


#This function counts the number of on-set minterms and maxterms
def count_terms(truthtable):
    countmin=0
    countmax=0

    for A in range(2):
        for B in range(2):
            for C in range(2):
                for D in range(2):
                    if truthtable[A][B][C][D]==1:
                        countmin=countmin+1
                    else:
                        countmax=countmax+1
    return countmin, countmax

#This function flips every value in a truth table
def inv(truthtable):

    truthtable1=truthtable.copy()
    for A in range(2):
        for B in range(2):
            for C in range(2):
                for D in range(2):
                    truthtable1[A][B][C][D]=flip(truthtable[A][B][C][D])
    return truthtable1


#This function writes a string for a row of the truth table
def binary_to_string(a,b,c,d):

    astring=''
    if(a ==1):
        astring="A"
    if(a==0):
        astring="A'"
    
    bstring=''
    if(b ==1):
        bstring="B"
    if(b==0):
        bstring="B'"
    
    cstring=''
    if(c ==1):
        cstring="C"
    if(c==0):
        cstring="C'"
    
    dstring=''
    if(d ==1):
        dstring="D"
    if(d==0):
        dstring="D'"

    return astring,bstring,cstring,dstring


#This function formats a minimized SOP function
def format_sop(terms):
    sum_of_products=''
    for i in range(0,len(terms)):
        if i != 0:
            sum_of_products=sum_of_products+'+'
        sum_of_products=sum_of_products+binary_to_string(terms[i][0],terms[i][1],terms[i][2],terms[i][3])[0]+binary_to_string(terms[i][0],terms[i][1],terms[i][2],terms[i][3])[1]+binary_to_string(terms[i][0],terms[i][1],terms[i][2],terms[i][3])[2]+binary_to_string(terms[i][0],terms[i][1],terms[i][2],terms[i][3])[3]
    return sum_of_products

#This function formats a minimized POS function
def format_pos(terms):
    product_of_sums=''
    for i in range(0,len(terms)):
        product_of_sums=product_of_sums+'('+binary_to_string(flip(terms[i][0]),flip(terms[i][1]),flip(terms[i][2]),flip(terms[i][3]))[0]
        if len(binary_to_string(flip(terms[i][0]),flip(terms[i][1]),flip(terms[i][2]),flip(terms[i][3]))[1]) >0:
            product_of_sums=product_of_sums+'+'+binary_to_string(flip(terms[i][0]),flip(terms[i][1]),flip(terms[i][2]),flip(terms[i][3]))[1]
        if len(binary_to_string(flip(terms[i][0]),flip(terms[i][1]),flip(terms[i][2]),flip(terms[i][3]))[2]) >0:
            product_of_sums=product_of_sums+'+'+binary_to_string(flip(terms[i][0]),flip(terms[i][1]),flip(terms[i][2]),flip(terms[i][3]))[2]
        if len(binary_to_string(flip(terms[i][0]),flip(terms[i][1]),flip(terms[i][2]),flip(terms[i][3]))[3]) >0:
            product_of_sums=product_of_sums+'+'+binary_to_string(flip(terms[i][0]),flip(terms[i][1]),flip(terms[i][2]),flip(terms[i][3]))[3]
        product_of_sums=product_of_sums+')'
    return product_of_sums

#This function prints the truthtable for the function
def print_truthtable(truthtable):

    print('       A\'B\'       A\'B       AB       AB\'')
    print('______________|_________|________|_________')
    print('C\'D\'|   '+str(int(truthtable[0][0][0][0]))+'     |    '+str(int(truthtable[0][1][0][0]))+'    |    '+str(int(truthtable[1][1][0][0]))+'   |    '+str(int(truthtable[1][0][0][0])))
    print('______________|_________|________|_________')
    print('C\'D |   '+str(int(truthtable[0][0][0][1]))+'     |    '+str(int(truthtable[0][1][0][1]))+'    |    '+str(int(truthtable[1][1][0][1]))+'   |    '+str(int(truthtable[1][0][0][1])))
    print('______________|_________|________|_________')
    print('CD  |   '+str(int(truthtable[0][0][1][1]))+'     |    '+str(int(truthtable[0][1][1][1]))+'    |    '+str(int(truthtable[1][1][1][1]))+'   |    '+str(int(truthtable[1][0][1][1])))
    print('______________|_________|________|_________')
    print('CD\' |   '+str(int(truthtable[0][0][1][0]))+'     |    '+str(int(truthtable[0][1][1][0]))+'    |    '+str(int(truthtable[1][1][1][0]))+'   |    '+str(int(truthtable[1][0][1][0])))
    return

#This function converts binary to decimal
def binary_to_dec(a,b,c,d):
    return (8*a)+(4*b)+(2*c)+d


#This function flips the value of a bit
def flip(a):
    if a==1:
        a=0
    elif(a==0):
        a=1
    return a
    
#This function returns 1 if a minterm is contained within an implicant, 0 otherwise
def contains(implicant, minterm):
    A1=implicant[0]
    B1=implicant[1]
    C1=implicant[2]
    D1=implicant[3]

    A2=minterm[0]
    B2=minterm[1]
    C2=minterm[2]
    D2=minterm[3]

    if (A1 == A2 or A1== -1):
        if (B1 == B2 or B1== -1):
            if (C1 == C2 or C1== -1):
                if (D1 == D2 or D1== -1):
                    return 1
    return 0

#This function returns the prime implicants of a function
def prime_implicants(truthtable):

    #initialize arrays
    prime_implicants=[]
    three_var_terms=[]
    two_var_terms=[]


    #Use four for loops to loop through the entire truth table
    for A in range(2):
        for B in range(2):
            for C in range(2):
                for D in range(2):
                    
                    if truthtable[A][B][C][D]==1: #We want to build implicants from 1s in the table

                        foundimplicant=False #We will need to check if our square finds an implicant

                        #Check adjacent square by flipping A
                        if (truthtable[flip(A)][B][C][D]==1):
                            foundimplicant=True
                            if binary_to_dec(flip(A),B,C,D)<binary_to_dec(A,B,C,D):
                                three_var_terms.append([-1,B,C,D])
                        
                        
                        #Check adjacent square by flipping B
                        if (truthtable[A][flip(B)][C][D]==1):
                            foundimplicant=True
                            if (binary_to_dec(A,flip(B),C,D)>binary_to_dec(A,B,C,D)):
                                three_var_terms.append([A,-1,C,D])
                                
                        #Check adjacent square by flipping C
                        if (truthtable[A][B][flip(C)][D]==1):
                            foundimplicant=True
                            if binary_to_dec(A,B,flip(C),D)>binary_to_dec(A,B,C,D):
                                three_var_terms.append([A,B,-1,D])

                        #Check adjacent square by flipping D
                        if (truthtable[A][B][C][flip(D)]==1):
                            foundimplicant=True
                            if((binary_to_dec(A,B,C,flip(D))>binary_to_dec(A,B,C,D))):
                                three_var_terms.append([A,B,C,-1])
                                
                        #If the square never found an implicant, then the cube is a prime implicant
                        if(not foundimplicant):
                            prime_implicants.append([A,B,C,D])



    #######################Looking for combinations of 3 variable terms############################
    #These for loops allow us to compare every term to every other term once
    for i in range (len(three_var_terms)):

        matchfound=False #If this is still false after comparing with all other terms, then it is a prime implicant

        #Grab values of inputs from given term
        A1=three_var_terms[i][0]
        B1=three_var_terms[i][1]
        C1=three_var_terms[i][2]
        D1=three_var_terms[i][3]

        for j in range (0,len(three_var_terms)):

            #Grab values of inputs from comparison term
            A2=three_var_terms[j][0]
            B2=three_var_terms[j][1]
            C2=three_var_terms[j][2]
            D2=three_var_terms[j][3]

            #compare the terms
            compare=(A1==A2)+(B1==B2)+(C1==C2)+(D1==D2)
            #If there is exactly one unlike input, we combine terms
            if (compare==3):
                matchfound=True
                if i<j:
                    if (A1 != A2):
                        two_var_terms.append([-1,B1,C1,D1])
                    elif (B1 != B2):
                        two_var_terms.append([A1,-1,C1,D1])
                    elif (C1 != C2):
                        two_var_terms.append([A1,B1,-1,D1])
                    elif (D1 != D2):
                        two_var_terms.append([A1,B1,C1,-1])
            
            #If there is a duplicate, skip it and let the last copy be added
            elif(compare==4 and i<j):
                matchfound=True

        #If a term has no expansion, it's a prime implicant
        if matchfound==False:
            prime_implicants.append([A1,B1,C1,D1])

    ############################Looking for combinations of 2 variable terms#############################

    #These for loops allow us to compare every term to every other term once
    for i in range (len(two_var_terms)):

        matchfound=False #If this is still false after comapring with all other terms, then it is a prime implicant

        #Grab values of inputs from given term
        A1=two_var_terms[i][0]
        B1=two_var_terms[i][1]
        C1=two_var_terms[i][2]
        D1=two_var_terms[i][3]

        for j in range (0,len(two_var_terms)):

            #Values of the inputs in the comparison term
            A2=two_var_terms[j][0]
            B2=two_var_terms[j][1]
            C2=two_var_terms[j][2]
            D2=two_var_terms[j][3]

            #If there is exactly one unlike input, we combine terms
            compare=(A1==A2)+(B1==B2)+(C1==C2)+(D1==D2)
            if (compare==3):
                matchfound=True
                if i<j:
                    if (A1 != A2):
                        prime_implicants.append([-1,B1,C1,D1])
                    elif (B1 != B2):
                        prime_implicants.append([A1,-1,C1,D1])
                    elif (C1 != C2):
                        prime_implicants.append([A1,B1,-1,D1])
                    elif (D1 != D2):
                        prime_implicants.append([A1,B1,C1,-1])
            
            #If there is a duplicate, skip it and let the last copy be added
            elif(compare==4 and i<j):
                matchfound=True

        #If a term has no expansion, it's a prime implicant
        if matchfound==False:
            prime_implicants.append([A1,B1,C1,D1])
            
    #Duplicate Handling
    prime_implicants_copy=prime_implicants.copy()
    prime_implicants=[]
    for i in range(len(prime_implicants_copy)):
        duplicate_found=False
        for j in range(i+1,len(prime_implicants_copy)):
            if prime_implicants_copy[i]==prime_implicants_copy[j]:
                duplicate_found=True
        if not duplicate_found:
            prime_implicants.append(prime_implicants_copy[i])

    return prime_implicants

#This function generates a table to help find essential prime implicants
def generate_coverage_table(minterms,prime_implicants):
    #Setup a coverage table
    coveragetable=np.zeros((len(prime_implicants),len(minterms)))
    

    #See which minterms are covered by each implicant
    for implicant in range(len(prime_implicants)):
        for minterm in range(len(minterms)):

            #Compare minterms and implicants
            A1=prime_implicants[implicant][0]
            B1=prime_implicants[implicant][1]
            C1=prime_implicants[implicant][2]
            D1=prime_implicants[implicant][3]

            A2=minterms[minterm][0]
            B2=minterms[minterm][1]
            C2=minterms[minterm][2]
            D2=minterms[minterm][3]

            if (A1 == A2 or A1== -1):
                if (B1 == B2 or B1== -1):
                    if (C1 == C2 or C1== -1):
                        if (D1 == D2 or D1== -1):
                            coveragetable[implicant][minterm]=1
    
    return coveragetable

def essential_prime_implicants(prime_implicants):

    essential_prime_implicants=[]

    #Generate Minterms
    minterms=[]
    for A in range(2):
        for B in range(2):
            for C in range(2):
                for D in range(2):                
                    if truthtable[A][B][C][D]==1:
                        minterms.append([A,B,C,D])

    

    #Generate a coverage table
    coveragetable=generate_coverage_table(minterms,prime_implicants)

    

    minterm_index=0
    while 1:

        #If the index is equal to the length, all "solo columns" have been taken care of
        
        if minterm_index >= len(minterms):
            break
       
        #If there is a minterm that is only covered by one implicant...
        working_column= coveragetable[:,minterm_index]
        
        if sum(working_column)==1:
            

            
          
            #The implicant that covers it is a prime implicant
            index=np.where(coveragetable[:,minterm_index]==1)
            

            
            essential_prime_implicants.append(prime_implicants[index[0][0]])
            
            

            #Get rid of the minterms covered by the prime implicant
            minterms_covered_index=np.where(coveragetable[index[0][0],:]==1)
 
            minterms_copy=minterms.copy()
            for i in range(0,len(minterms_covered_index[0])):
                
                minterms_copy.remove(minterms[minterms_covered_index[0][i]])
            
                

            minterms=minterms_copy
                
            
            #Get rid of the prime implicant
            prime_implicants.remove(prime_implicants[index[0][0]])

            #Generate a new coveragetable
            
            coveragetable=generate_coverage_table(minterms,prime_implicants)
            
            minterm_index=0

        else:
            minterm_index=minterm_index+1


    return essential_prime_implicants


def choose_terms(prime_implicants,essential_prime_implicants,truthtable):

    terms=essential_prime_implicants.copy()

    #Generate Minterms
    minterms=[]
    for A in range(2):
        for B in range(2):
            for C in range(2):
                for D in range(2):                
                    if truthtable[A][B][C][D]==1:
                        minterms.append([A,B,C,D])

    #Keep track of which minterms still need to be covered
    minterms_remaining=[]

    #Minterms covered by essential prime implicants are all set
    for i in range(0,len(minterms)):
        covered_by_essential=False
        for j in range(0,len(essential_prime_implicants)):
            
            if contains(essential_prime_implicants[j],minterms[i]):
                covered_by_essential=True
                

        if not covered_by_essential:
            minterms_remaining.append(minterms[i])
            

        

    #Now, use prime implicants to cover the remaining minterms
    
    
    while len(minterms_remaining)>0:

        #This index will keep track of which prime implicant we are using
        prime_implicants_index=0

        

        #Generate a coveragetable
        coveragetable=generate_coverage_table(minterms_remaining,prime_implicants)

        #We want to know which prime implicant covers the most remainign minterms
        sumrows=[]
        for i in range(0, len(prime_implicants)):
            sumrows.append(sum(coveragetable[i,:]))
        max_minterms_covered=np.max(sumrows)
        prime_implicants_index=np.where(sumrows==max_minterms_covered)
        

        #Add this prime implicant to out list of terms
        terms.append(prime_implicants[prime_implicants_index[0][0]])

        #Remove the minterms covered
        minterms_remaining_copy=minterms_remaining.copy()
        for i in range(0,len(minterms_remaining)):
            if contains(prime_implicants[prime_implicants_index[0][0]],minterms_remaining[i]):
                minterms_remaining_copy.remove(minterms_remaining[i])
        minterms_remaining=minterms_remaining_copy

        #Remove the prime implicant
        prime_implicants.remove(prime_implicants[prime_implicants_index[0][0]])

        

    return terms

#This fucntion prints a chart that shows which implicants cover which minterms
def print_coverage_table(p_implicants, ep_implicants,truthtable):

    for i in range(0, len(ep_implicants)):
        p_implicants.append(ep_implicants[i])

    #Generate Minterms
    minterms=[]
    for A in range(2):
        for B in range(2):
            for C in range(2):
                for D in range(2):                
                    if truthtable[A][B][C][D]==1:
                        minterms.append([A,B,C,D])

    
    coveragetable=generate_coverage_table(minterms,p_implicants)

    header='         '
    
    headerlengths=[]
    for i in range(0,len(minterms)):
        header1=''
        header1+=binary_to_string(minterms[i][0],minterms[i][1],minterms[i][2],minterms[i][3])[0]
        
        header1+=binary_to_string(minterms[i][0],minterms[i][1],minterms[i][2],minterms[i][3])[1]
        
        header1+=binary_to_string(minterms[i][0],minterms[i][1],minterms[i][2],minterms[i][3])[2]
        
        header1+=binary_to_string(minterms[i][0],minterms[i][1],minterms[i][2],minterms[i][3])[3]
        header1+=' | '
        header+=header1
        headerlengths.append(len(header1))

    print(header)

    for i in range(0, len(p_implicants)):
        line=''
        line+= binary_to_string(p_implicants[i][0],p_implicants[i][1],p_implicants[i][2],p_implicants[i][3])[0]
        line+= binary_to_string(p_implicants[i][0],p_implicants[i][1],p_implicants[i][2],p_implicants[i][3])[1]
        line+= binary_to_string(p_implicants[i][0],p_implicants[i][1],p_implicants[i][2],p_implicants[i][3])[2]
        line+= binary_to_string(p_implicants[i][0],p_implicants[i][1],p_implicants[i][2],p_implicants[i][3])[3]
        line+='\t    '
        for j in range(0, len(minterms)):
            
            if contains(p_implicants[i],minterms[j]):
                line+='X'
            else:
                line+=' '
            for k in range(0,headerlengths[j]-1):
                line+=' '
            
                

        print(line)
    return




############################################### HW Deliverables #########################################################
#sample=prime_implicants(truthtable)
#sample1=essential_prime_implicants(sample)


#5: Sum of Products
#print('Sum of Products:')
#preserved_prime_implicants=sample.copy()
#print(format_sop(choose_terms(sample,sample1,truthtable)))
#print()

#6: Product of Sums
#sample_inv=prime_implicants(inv(truthtable))
#sample_inv1=essential_prime_implicants(sample_inv)

#print('Product of Sums')
#print(format_pos(choose_terms(sample_inv,sample_inv1,inv(truthtable))))
#print()

#7: Number of Prime Implicants
#print("There are "+str(len(preserved_prime_implicants)+len(sample1))+" prime implicants")

#8: Number of Essential Prime Implicants
#print("There are "+str(len(sample1))+" essential prime implicants")

#9: On Minterms
#print('There are '+str(count_terms(truthtable)[0])+' On-set minterms')

#10: On Maxterms
#print('There are '+str(count_terms(truthtable)[1])+' On-set maxterms')

#11: Print K map
#print_truthtable(truthtable)
#print()
#print()

#12: Print Coverage Table
#print_coverage_table(preserved_prime_implicants, sample1,truthtable)
