import scipy.optimize as optimize 
import numpy as np
import re
import os
from collections import OrderedDict

############################################
###############Functions####################
############################################


def filerun(filename):
    output = str(filename)+'.out'
    command = 'fresco' + '<' + filename + '>' + output
    os.system(command)


def create_file_list(afile):
    f = []
    with open(afile,'r') as g: 
        for line in g:
            line = line.split()
            f.append(line)
    return f

    
def getfile():
    drp = os.listdir('.')
    go = True
    while go: 
        temp = raw_input("Input a file cd changes directory and ls lists contents.\n")
        if temp == 'cd':
            os.chdir(raw_input("What's the path?\n"))
            drp = os.listdir('.')
        elif temp == 'ls':
            print drp
        elif temp == 'fuck':
            go = False
            
        else:
            if temp in os.listdir('.'):
                afile = temp
                go = False
            else:
                print(temp+" ain't no file!\n")
    return afile
        
#Reads fort.200 files returns LineObject    
def read_cross(filename):
    filelist = create_file_list(filename)
    #Initialize lists for angular information
    theta = []
    sigma = []
    for ele in filelist:
        #This picks out the cross section at each angle.
        if len(ele) == 2 and ele[0] != '@legend' and ele[0] != '@subtitle':
            theta.append(float(ele[0]))                  
            sigma.append(float(ele[1]))

        #looks for lab energy. 
        elif ele[0] == '@legend' or ele[0] == '#legend':
            if 'energy' in ele:
                energy = re.findall('[0-9.0]+',ele[6])
                E = float(energy[0])

        # End of file create the LineObject ask user for state information 
        elif ele[0] == 'END':
            # jpi = raw_input("What is the spin parity of the state(Ex. 1.5+,1- etc.)?\n")
            # J=''
            # for s in re.findall('[^\+\-]',jpi):
            #     J += s
            # par = re.findall('[\+\-]',jpi)[0]
            graphline = LineObject(theta,sigma,E,'0','+')

    return graphline

#Reads two col. data files returns DataObject
def read_data(filename):
    filelist = create_file_list(filename)
    theta = []
    sigma = []
    errx = []
    erry = []
    for ele in filelist:
        theta.append(float(ele[0]))                  
        sigma.append(float(ele[1]))
        try:
            errx.append(float(ele[2]))
        except IndexError:
            pass
        try:
            erry.append(float(ele[3]))
        except IndexError:
            pass
            
    graphline = DataObject(theta,sigma,errx,erry)
    return graphline

#Reads fort 17 file and returns a wavefunction class object to plot
#def read_wavefunction(filename):


#do a sum of two cross sections that have the same angles
def cs_sum(cs1,cs2):
    if not cs1.theta == cs2.theta:
        print "These cross sections don't have the same angles!"
    else:
        return LineObject(cs1.theta,cs1.sigma+cs2.sigma,cs1.E,cs1.J,cs1.par)





############################################
#########Classes For Plotting###############
############################################

#new generic class for angular distrubutions
class Angles():
    def __init__(self,theta,sigma):
        self.theta = np.asarray(theta)
        self.sigma = np.asarray(sigma)


#This is the tenenative class for graphs. It includes scaling for elastic fits.
class LineObject(Angles):
    def __init__ (self,theta,sigma,E,J,par):
        self.E = E
        self.J = J
        self.par = par
        Angles.__init__(self,theta,sigma)

    def scale_it(self,value,angle,constant=None):
        if constant:
            self.sigma = constant*self.sigma
        else:
            index = self.find_angle(angle)
            scale = value/self.sigma[index]
            print 'Factor is: ', scale 
            #Added slice overwrite to be a bit more careful with list
            self.sigma = scale*self.sigma

            
    #Picks out list index for a given angle.
    def find_angle(self,angle):
        angle = float(angle)
        if angle in self.theta:
            return np.argwhere(self.theta == angle) 
        
        else:
            angle = float(raw_input('Angle not found try again! \n'))
            print self.theta
            self.find_angle(angle)
        
    #function for angle ref Ian Thompsons's book written in a form for root finding since it is transendental
    def com_fun(self,x,a,b):
        return (np.tan(a) - (np.sin(x)/(b+np.cos(x))))
        
    #function for cross section
    def cross_factor(self,com_angle,rho):
        return ((1+rho**2+2*rho*np.cos(com_angle))**(3.0/2.0))/(np.abs(1+rho*np.cos(com_angle)))

    #lab angle transformation
    def lab_fun(self,a,b):
        return (np.arctan((np.sin(a)/(b+np.cos(a)))))

    
    #Transfers lab frame data to center of mass.
    def to_com(self,massa,massb,massc,massd,Elab,Q):
        angle = self.theta*(np.pi/180.0) #to radians 
        rho = np.sqrt((massa*massc)/(massd*massb)*Elab/(Elab+Q))
        #root is from scipy optimize
        sol = optimize.fsolve(self.com_fun,angle,(angle,rho)) #solve transformation for angles. 
        #now alter sigma
        cs_scale = self.cross_factor(sol,rho) #solve transformation for cross section
        com_angle = sol*(180.0/np.pi) #to degrees
        self.theta = com_angle
        self.sigma = cs_scale*self.sigma

    #from com to lab
    def to_lab(self,massa,massb,massc,massd,Elab,Q):
        angle = self.theta*(np.pi/180.0)
        rho = np.sqrt((massa*massc)/(massd*massb)*Elab/(Elab+Q))
        lab_scale = (self.cross_factor(angle,rho))**(-1.0) #uses com angles for scale
        lab_angle = self.lab_fun(angle,rho)
        self.theta = lab_angle*(180.0/np.pi)
        self.sigma = lab_scale*self.sigma
        
#new subclass for experimental data.
class DataObject(LineObject):
    def __init__(self,theta,sigma,errx,erry):
        Angles.__init__(self,theta,sigma)
        #We do not expect all data files to have errors
        self.errx = np.asarray(errx)
        self.erry = np.asarray(erry)

    ### def to_lab(self,massa,massb,massc,massd,Elab,Q):
    ###     LineObject.to_lab(self,massa,massb,massc,massd,Elab,Q)
    ###     rho = np.sqrt((massa*massc)/(massd*massb)*Elab/(Elab+Q))
    ###     if self.errx.any(): #x errors require only angle transformations
    ###         angle = self.errx*(np.pi/180.0)
    ###         lab_ang_errors = self.lab_fun(angle,rho)
    ###         self.errx = lab_ang_errors*(np.pi/180.0)
    ###     if self.erry.any():
    ###         lab_cross_errors = self.erry
            
            
#################################################
###########Classes For Analysis##################
#################################################

#Generic Class that tries to capture basic format of each fresco namelist
class FrescoNamelist():
    def __init__(self,start,stop,thefile=None,ispart=False):
        self.start = start #Character or string for start of namelist
        self.stop = stop  #Character for stop
        self.data = []
        self.ispart = ispart
        if thefile:
            self.get_data(thefile)
         

    #Iterator for the list useful for picking out namelists
    def fresco_iter(self,afile):
        with open(afile,'r') as f:
            #Since the file is open within the with statement
            #when the break happens the line position is maintained.
            for line in f:
                if self.start in line: 
                    break
            for line in f:
                yield line
                if self.stop in line:
                    break

    #Use the iterator to add data based on namelist properties
    def get_data(self,afile):
        for line in self.fresco_iter(afile):
            self.data.append(line)

   
#Building off of FrescoNamelist structure to actually represent a whole input file.
class FrescoInput():

    def __init__(self,thefile):
        
        #Initializes all the common namelists into lists where each line is one string.
        self.title = [] #title line that is excluded due to funkyness on the namelist read.
        self.parameters = FrescoNamelist('','/',thefile,).data #Empty string is always true and iteration cuts off first line 
        self.partitions = FrescoNamelist('/','&partition',thefile).data
        self.potentials = FrescoNamelist('&partition','&pot',thefile).data
        self.overlaps = FrescoNamelist('&pot','&overlap',thefile).data
        self.couplings = FrescoNamelist('&overlap','&coupling',thefile).data
        
        
        self.fresco = [] #file as a list
        #Common types of potentials used in fresco
        self.pot_types= {'type=0':'Coulomb',
                         'type=1':'Volume',
                         'type=2':'Surface',
                         'type=3':'Proj Spin-Orbit',
                         'type=4':'Target Spin-Orbit',
                         }
    
        #Dict of potentials
        self.sorted_pots = self.find_pots()

        #get the title line
        with open(thefile,'r') as f:
            for line in f:
                self.fresco.append(line)

        self.title = [self.fresco[0]] #title line that is excluded due to funkyness on the namelist read.
        
    def write(self,name):
        with open(str(name),'w') as f:
            for line in self.fresco:
                f.write(line)
        
    #Find given variable in string. Splt_char can be used to split to return just value 
    def find_value(self,var,string,splt_char=''):
        non_split = (re.search(str(var)+'\S+',string).group()) 
        if splt_char:
            return non_split.split(splt_char)[1]
        return non_split

                
    #Changes a value for a given variable in a string            
    def change_value(self,var,val,s):
        old_string = self.find_value(var,s)
        new_string = str(var)+'='+str(val)
        s = s.replace(old_string,new_string)
        return s
    
    
    #Sensitivty study for parameters namelist
    def sensitivity(self,var,values):
        try:
            os.mkdir(str(var)+'_sensitivity') #see if the sensitivity directory already exists
        except OSError: 
            print 'You have probably already done this study...'
            
        os.chdir(str(var)+'_sensitivity') #switch into created sensitivity directory
        
        for ele in values:
            new_lines = [] #what will become the updated values
            name = str(var)+'='+str(ele) #name we will rename everything
            for line in self.parameters:
                if str(var) in line:
                    line = self.change_value(var,ele,line)
                new_lines.append(line)
            self.parameters[:] = new_lines #update parameters namelist
            self.update_all() #create the new file list
            self.write(name) #create the input file
            filerun(name) #run fresco
            old_names = os.listdir('.') 
            old_names[:] = [ele for ele in old_names if re.search('fort.2\d{2}',ele)] #find the cross section files fort.200s 
            new_names = [name+'.'+(re.search('\d{3}',ele)).group() for ele in old_names] #name is new parameter value + .200s
            for i,j in zip(old_names,new_names):
                os.rename(i,j) #change all the names
        os.chdir('..') #go to original directory

    #This method sorts out all potentials    
    def find_pots(self):
        all_pots = OrderedDict() #Keeps entries in order for looping over later
        
        for ele in self.potentials:
            #We check to see which partition it belongs to as if it is part of an
            #existing one.
            if 'kp' in ele:
                #I make the assumtion that type is on the same line as kp
                index = self.find_value('kp',ele,splt_char='=')
                #type does not have to be specified, and if it is not assumed to be a coulomb potential
                if 'type' in ele:
                    pot_type = self.pot_types[self.find_value('type',ele)]
                else:
                    pot_type = 'Coulomb'
                #See if this is another potential partition or just another type
                if index in all_pots:
                    all_pots[index][pot_type] = []
                    all_pots[index][pot_type].append(ele)
                else:
                    all_pots[index] = OrderedDict()
                    all_pots[index][pot_type] = []
                    all_pots[index][pot_type].append(ele)
                
            #Scoop up the two line potentials    
            elif '/' in ele:
                all_pots[index][pot_type].append(ele)        
                
        return all_pots


    #Updates the potential block so that we can make a new input file
    def update_pot(self):
        #pretty jank way to do this. Making up for orignal newline that is omitted in sorting process.
        new_potentials = [' \n']
        for key,item in self.sorted_pots.iteritems(): #each partitions associated potentials
            for in_key,in_item in item.iteritems(): #each type of potential for a given partition
                for ele in in_item: #actual namelist items
                    if '&pot' in ele: #this terminates the namelist so it must be last line
                        last_line = ele
                    else:
                        new_potentials.append(ele)
        self.potentials[:] = new_potentials 
        self.potentials.append(last_line) 
            
            
    
    #To be used for searchs later. Destructive to orginal value. 
    def change_pot(self,pot,term,var,val):
        for index,ele in enumerate(self.sorted_pots[pot][term]):
            if var in ele:
                ele = self.change_value(var,val,ele)
                self.sorted_pots[pot][term][index] = ele 


    #Reassembles all namelists into the singular self.fresco list
    def update_all(self):
        #First make sure all namelists are current.
        self.update_pot()
        #Add the others when the time comes.
        #Now join the lists. 
        new_fresco = self.title+self.parameters+self.partitions+self.potentials+self.overlaps+self.couplings
        self.fresco[:] = new_fresco
