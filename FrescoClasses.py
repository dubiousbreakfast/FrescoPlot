from scipy.optimize import root
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
        
#Reads fort.200 files returns lineobject    
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

        # End of file create the lineobject ask user for state information 
        elif ele[0] == 'END':
            # jpi = raw_input("What is the spin parity of the state(Ex. 1.5+,1- etc.)?\n")
            # J=''
            # for s in re.findall('[^\+\-]',jpi):
            #     J += s
            # par = re.findall('[\+\-]',jpi)[0]
            graphline = lineobject(theta,sigma,E,'0','+')

    return graphline

#Reads two col. data files returns dataobject
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
            
    graphline = dataobject(theta,sigma,errx,erry)
    return graphline

#Reads fort 17 file and returns a wavefunction class object to plot
#def read_wavefunction(filename):









############################################
#########Classes For Plotting###############
############################################

#new generic class for angular distrubutions
class Angles():
    def __init__(self,theta,sigma):
        self.theta = theta
        self.sigma = sigma


#This is the tenenative class for graphs. It includes scaling for elastic fits.
class lineobject(Angles):
    def __init__ (self,theta,sigma,E,J,par):
        self.E = E
        self.J = J
        self.par = par
        Angles.__init__(self,theta,sigma)

    def scale_it(self,value,angle,constant=None):
        if constant:
            self.sigma[:] = [x*value for x in self.sigma]
        else:
            index = self.find_angle(angle)
            scale = value/self.sigma[index]
            print 'Factor is: ', scale 
            #Added slice overwrite to be a bit more careful with list
            self.sigma[:] = [x*scale for x in self.sigma]

            
    #Picks out list index for a given angle.
    def find_angle(self,angle):
        if angle in self.theta:
            return self.theta.index(angle) 
        
        else:
            angle = raw_input('Angle not found try again! \n')
            print self.theta
            self.find_angle(angle)
    
    #Resizes cross section and angle lists that are outside a given angle
    def angle_range(self,ran):
        index = self.find_angle(ran)
        return ([j for i,j in enumerate(self.theta) if i <= index],
                [j for i,j in enumerate(self.sigma) if i <= index])
        
    #function for angle 
    def com_fun(self,x,a,b):
        return (a - (np.sin(x)/(b+np.cos(x))))
        
    #function for cross section
    def com_cross(self,x,a,b,c):
        return (a - ((1+b**2+2*b*np.cos(c))**(3.0/2.0))/(abs(1+b*np.cos(c)))*x)
        
    #Transfers lab frame data to center of mass.
    def make_com(self,massa,massb,massc,massd,Elab,Q,angle,sigma):
        angle = angle*(np.pi)/(180.0)
        rho = np.sqrt((massa*massc)/(massd*massb)*Elab/(Elab+Q))
        tan_lab = np.tan(angle)
        #root is from scipy optimize
        sol = root(self.com_fun,0.0,(tan_lab,rho))
        #now alter sigma
        cs_sol = root(self.com_cross,0.0,(sigma,rho,sol.x[0]))
        com_angle = sol.x[0]*(180.0/np.pi)
        return (com_angle,cs_sol.x[0])
        
    #Now a function to shift the whole data set
    def labtocom(self,ma,mb,mc,md,Elab,Q):
        angle = self.theta
        sigma = self.sigma
        new_sigma = []
        new_theta = []
        for ang,sig in zip(angle,sigma):
            ang,sig = self.make_com(ma,mb,mc,md,Elab,Q,ang,sig)
            new_sigma.append(sig)
            new_theta.append(ang)
        angle[:] = new_theta
        sigma[:] = new_sigma
                    
        
#new subclass for experimental data.
class dataobject(lineobject):
    def __init__(self,theta,sigma,errx,erry):
        Angles.__init__(self,theta,sigma)
        #We do not expect all data files to have errors
        if errx:
            self.errx = errx
        if erry:
            self.erry = erry
            
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
        self.parameters = FrescoNamelist('','/',thefile,).data #Empty string is always true and iteration cuts off first line 
        self.partitions = FrescoNamelist('/','&partition',thefile).data
        self.potentials = FrescoNamelist('&partition','&pot',thefile).data
        self.overlaps = FrescoNamelist('&pot','&overlap',thefile).data
        self.couplings = FrescoNamelist('&overlap','&coupling',thefile).data

        #Common types of potentials used in fresco
        self.pot_types= {'type=0':'Coulomb',
                         'type=1':'Volume',
                         'type=2':'Surface',
                         'type=3':'Proj Spin-Orbit',
                         'type=4':'Target Spin-Orbit',
                         }

               
        #Hold over from first implementation since I don't want to redo sensitivity
        #routine right now.
        self.fresco = []
        
        with open(thefile,'r') as f:
            for line in f:
                self.fresco.append(line)
        
        #Dict of potentials
        self.sorted_pots = self.find_pots()

    #Simple write function that writes a newinput file
    def write(self,filename):
        with open(filename,'w') as f:
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
    
    
    #This is really only set up for the parameters list so far.
    #Does appear to work with elab, so that is cool.
    def sensitivity(self,var,values):
        try:
            os.mkdir(str(var)+'_sensitivity')
        except OSError: 
            print 'You have probably already done this study...'
            
        os.chdir(str(var)+'_sensitivity')
        
        for ele in values:
            new_lines = []
            name = str(var)+'='+str(ele)
            for line in self.fresco:
                if str(var) in line:
                    line = self.change_value(var,ele,line)
                new_lines.append(line)
            self.write(name,new_lines)
            filerun(name)
            old_names = os.listdir('.')
            old_names[:] = [ele for ele in old_names if re.search('fort.2\d{2}',ele)]
            new_names = [name+'.'+(re.search('\d{3}',ele)).group() for ele in old_names]
            for i,j in zip(old_names,new_names):
                os.rename(i,j)
        os.chdir('..')

    #This method sorts out all potentials    
    def find_pots(self):
        all_pots = OrderedDict() #Keeps entries in order for looping over later
        
        for ele in self.potentials:
            #We check to see which partition it belongs to as if it is part of an
            #exsisting one.
            if 'kp' in ele:
                #I make the assumtion that type is on the same line as kp
                index = self.find_value('kp',ele,'=')
                pot_type = self.pot_types[self.find_value('type',ele)]
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
        for key,item in self.sorted_pots.iteritems():
            for in_key,in_item in item.iteritems():
                for ele in in_item:
                    new_potentials.append(ele)
        self.potentials[:] = new_potentials
                       
            
            
    
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
        new_fresco = [self.fresco[0]]+self.parameters+self.partitions+self.potentials+self.overlaps+self.couplings #fresco[0] is so that the first line is still there 
        self.fresco[:] = new_fresco
