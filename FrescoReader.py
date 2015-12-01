#We look to take the output of the fort.3 and fort.16 files 
#and put them in an easy to read file for plotting. The file 
#called FresDat.dat




#Spits out a nested list with each sublist being 1 line in the input file
def readin(thefile):
    total = []
    for line in file(thefile):
        line = line.split()
        total.append(line)
    return total




#class for the partition object


class Partition():

    def __init__(self,data,namep,namet):
        self.data = data
        self.namep = namep
        self.namet = namet


#This class takes lists and tears them down according to rules for each file of interest

class FresFil():

    def __init__(self,list1):
        self.data = list1


    #Method for fort.3 file type which creates a list for each partition
    #and is addressed to a key in a dictionary
    def partitions(self):
        parts = {}
        read = False
        part = []
        n = 0
        for el in list(self.data):
            #These if statements pick out the partitions
            #The order is dictated by the layout of the fort.3 file
            
            if el == ['&STATES']:
                read = True
            
            if el == ['/']:
                read = False
            
            if read:
                part.append(el)
                parts.update({n:part})

            if el == ['&PARTITION']:
                read = True
                n = n + 1
                print n 
                part = [] 
            
        return parts
        
            
                
                    
                    
    #Once the user has selected the desired partition and either projectile or target states
    #this method picks them out and returns a list of spins
    #def states(self,part,torp):
        




