import numpy as np
import re
import FrescoExe as fe
import os

############################################
#########Classes For Reading################
############################################

class FrescoRead():
    
    def __init__(self):
        self.home = os.getcwd()

    def create_file_list(self,afile):
        f = []
        for line in file(afile):
            line = line.split()
            f.append(line)
        return f

    
    def getfile(self):
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
        
    
    def read_cross(self,filename):
        filelist = self.create_file_list(filename)
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
                jpi = raw_input("What is the spin parity of the state(Ex. 1.5+,1- etc.)?\n")
                J=''
                for s in re.findall('[^\+\-]',jpi):
                    J += s
                par = re.findall('[\+\-]',jpi)[0]
                graphline = lineobject(theta,sigma,E,J,par)
            
        return graphline


    
    def read_data(self,filelist):
        filelist = self.create_file_list(filename)
        theta = []
        sigma = []
        for ele in filelist:
            theta.append(float(ele[0]))                  
            sigma.append(float(ele[1]))
        graphline = dataobject(theta,sigma)
        return graphline











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
        self.sigma_lab = [np.cos(i/2)*j for i,j in zip(self.theta,self.sigma)]

    def scale_it(self,value,angle):
        index = self.theta.index(angle)
        scale = value/self.sigma[index]
        #Added slice overwrite to be a bit more careful with list
        self.sigma[:] = [x*scale for x in self.sigma]
        
            
    #Picks out list index for a given angle.
    def find_angle(self,angle):
        if angle in self.theta:
            return self.theta.index(angle) 
        
        else:
            angle = raw_input('Angle not found try again! \n')
            self.find_angle(angle)
    
    #Resizes cross section and angle lists that are outside a given angle
    def angle_range(self,ran):
        index = self.find_angle(ran)
        return ([j for i,j in enumerate(self.theta) if i <= index],
                [j for i,j in enumerate(self.sigma) if i <= index])
        
                    
        
#new subclass for experimental data. Expasions will include error bars and the like.
class dataobject(Angles):
     def __init__(self,theta,sigma,errx=None,erry=None):
         Angles.__init__(self,theta,sigma)
         self.errx = errx
         self.erry = erry




#################################################
###########Classes For Analysis##################
#################################################


#generic class for changing inputs in fresco file. 
#Note this only works for single elab input 

class frescoinput():

    def __init__(self,thefile):
        
        self.fresco = []
        
        
        with open(thefile,'r') as f:
            for line in f:
                self.fresco.append(line)
        
        #self.pots = self.potentials()


    def write(self,filename,lines):
        with open(filename,'w') as f:
            for line in lines:
                f.write(line)

   #Changes a value for a given variable in a string            
    def change_value(self,var,val,string):
        old_string = re.search(str(var)+'\S+',string).group()
        new_string = str(var)+'='+str(val)
        return (old_string,new_string)
        

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
                    old_string,new_string = self.change_value(var,ele,line)
                    line = line.replace(old_string,new_string)
                new_lines.append(line)
            self.write(name,new_lines)
            fe.filerun(name)
            old_names = os.listdir('.')
            old_names[:] = [ele for ele in old_names if re.search('fort.2\d{2}',ele)]
            new_names = [name+'.'+(re.search('\d{3}',ele)).group() for ele in old_names]
            for i,j in zip(old_names,new_names):
                os.rename(i,j)
        os.chdir('..')
        

    #dE has units of energy. This uses the energy shift to alter prexisting input files to produce a 
    #yield curve
    def yields(self,dE,n):
       
        while True:
            try:
                fint = int(raw_input("Which partition(Ex. 1,2,3):"))
                break
            except ValueError:
                print "Try an integer fool."
                    
        new_lines = []
        
        for line in self.fresco:
                if 'elab' in line:
                    old_string,new_string = self.change_value('elab',None,line)
                    name = old_string + '_yield'
                    temp = re.split('=',old_string)
                    temp[-1] = str(float(temp[-1]) - (.5*float(dE)))
                    new_string = temp[0]+'='+temp[-1]
                    line = line.replace(old_string,new_string)
                new_lines.append(line)
        
        
        try:
            os.mkdir(name)
        except OSError: 
            print 'You have probably already done this study...'
        
        #Sets up the yield curve plots doing the final rescaling of the data.
        os.chdir(name)
        name = name.replace(old_string,new_string)
        self.write(name,new_lines)
        fe.filerun(name)
        if os.path.isfile('fort.20'+str(fint)):
            fort = fr.readfile('fort.20'+str(fint))
        else:
            fortname = str(raw_input('Could not find cross section file enter alternative.'))
            fort = fr.readfile(fortname)
        data = fr.readfres200(fort)
        #frescoplot(data,180,None,n)
        
        os.chdir('..')
        
        
        
