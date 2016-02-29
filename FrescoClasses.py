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
        #I think I made this better.
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

# class Partition():
    
#     def 
