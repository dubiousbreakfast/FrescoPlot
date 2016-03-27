import os
import FrescoClasses as fc
from re import findall 

#funtion to do file stuff. Return a list of all input files.
def getfiles(filetype):
    files = []
    drp = os.listdir('.')
    go = True
    while go: 
        temp = raw_input("Input a "+str(filetype)+" file cd changes directory, ls lists contents, done exits.\n")
        if temp == 'cd':
            os.chdir(raw_input("What's the path?\n"))
            drp = os.listdir('.')
        elif temp == 'ls':
            print drp
        elif temp == 'done':
            go = False
        else:
            if temp in os.listdir('.'):
                files.append(temp)
            else:
                print(temp+" ain't no file!\n")
    return files


#the generic file read funciton. Goes line by line returns nested list of each line in file
def readfile(filename):
    f = []
    for line in file(filename):
        line = line.split()
        f.append(line)
    return f


#Writes a file from file list formatting is wonky but appears to be good enough for fresco to
#use file

def writefile(filelist,output):
    f = open(output,'w')
    for ele in filelist:
        line = " ".join(ele)
        f.write(line+"\n")
    f.close()




#If readfile was called on fort.200 file this function gets lab energy and differential cross sections
#Returns a instance of the lineobject class form FrescoClasses.
def readfres200(filelist):
    
    #Initialize lists for angular information
    theta = []
    sigma = []
    for ele in filelist:
        #This picks out the cross section at each angle.
        if len(ele) == 2 and ele[0] != '@legend' and ele[0] != '@subtitle':
            theta.append(float(ele[0]))                  
            sigma.append(float(ele[1]))
        
        #looks for lab energy. Let this haunt your dreams until you think of a better way.
        elif ele[0] == '@legend' or ele[0] == '#legend':
            if 'energy' in ele:
                energy = findall('[0-9.0]+',ele[6])
                E = float(energy[0])

        # End of file create the lineobject ask user for state information
        elif ele[0] == 'END':
            J,par = raw_input("What is the spin parity of the state?\n")
            graphline = fc.lineobject(theta,sigma,E,J,par)
            
    return graphline



#This is used for raw data files assumes two columns
def read_data(filelist):
    theta = []
    sigma = []
    for ele in filelist:
        theta.append(float(ele[0]))                  
        sigma.append(float(ele[1]))
    graphline = fc.dataobject(theta,sigma)
    return graphline


#Takes file list and returns an instance of the inputfile class.

    
#def readfresinput(filelist):

    
