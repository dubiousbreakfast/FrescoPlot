import re


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
            new_angle = raw_input('Angle not found try again! ')
            find_angle(new_angle)
    
    #Resizes cross section and angle lists that are outside a given angle
    def angle_range(self,ran):
        index = self.find_angle(ran)
        self.theta[:] = [x for x in self.theta if self.theta.index(x) <= index]
        self.sigma[:] = [x for x in self.sigma if self.sigma.index(x) <= index]
                    
        
#new subclass for experimental data. Expasions will include error bars and the like.

class dataobject(Angles):
     def __init__(self,theta,sigma):
         Angles.__init__(self,theta,sigma)





#################################################
###########Classes For Analysis##################
#################################################


class frescoinput():
    
    #method to find a given variable in a list exceptions include elab,nlab,jbord
    #,and jump. Gives a list with original position as first element
    def find_var(self,dat,var):
        for place,string in enumerate(dat):
            if re.match(str(var),string):
                found = [place,string]
                return found
                
    
    #Given element of a list find value change value return optional third
    #if you don't want deliminated by =
    #Expects output from find_var
    def change_value(self,var,new_val,string='='):
        splitlist = re.split(string,var[1])
        splitlist[1] = str(new_val)
        var[1] = splitlist[0]+string+splitlist[1]
        return var
        
    #method to put varlist back in its place without screwing up
    #formatting hopefully. Takes same format list as change_value and find_var returns
    def var_repack(self,block,var):
        del block[var[0]]
        block.insert(var[0],var[1])
        return block
    

    #Function that allows a sensitivity study of a given variable over a given range
    def sensitivity(var,values):
        pass

    
