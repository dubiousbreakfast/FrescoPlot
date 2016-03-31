import re
import FrescoExe as fe
import os

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

    def scale_it(self,value,angle):
        index = self.theta.index(angle)
        scale = value/self.sigma[index]
        if scale != 1.0:
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
     def __init__(self,theta,sigma):
         Angles.__init__(self,theta,sigma)





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
    def senstivity(self,var,values):
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
                    line.replace(old_string,new_string)
                new_lines.append(line)
            self.write(name,new_lines)
            fe.filerun(name)
            old_names = os.listdir('.')
            old_names[:] = [ele for ele in old_names if re.search('fort.2\d{2}',ele)]
            new_names = [name+'.'+(re.search('\d{3}',ele)).group() for ele in old_names]
            for i,j in zip(old_names,new_names):
                os.rename(i,j)
        os.chdir('..')
        

    #dE has units of energy. 
    def yields(self,dE):
        
        new_lines = []
        
        for line in self.fresco:
                if 'elab' in line:
                    old_string,new_string = self.change_value('elab',None,line)
                    name = old_string + '_yield'
                    temp = re.split('=',old_string)
                    temp[-1] = str(float(temp[-1]) - (.5*float(dE)))
                    new_string = temp[0]+'='+temp[-1]
                    line.replace(old_string,new_string)
                new_lines.append(line)
        self.write(name,new_lines)
        
        try:
            os.mkdir(name)
        except OSError: 
            print 'You have probably already done this study...'
            
        os.chdir(name)
        
        fe.filerun(name)
        
        os.chdir('..')
        
        
