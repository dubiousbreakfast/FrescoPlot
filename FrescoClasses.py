
#This is the tenenative class for graphs. It includes scaling for elastic fits.
class lineobject():
    def __init__ (self,theta,sigma,E=None,J=None,par=None):
        self.E = E
        self.J = J
        self.par = par
        self.theta = theta
        self.sigma = sigma
        

    def scale_it(self,value,angle):
        index = self.theta.index(angle)
        scale = value/self.sigma[index]
        if scale != 1.0:
            self.sigma = map(lambda x:x*scale,self.sigma)

    #Picks out list index for a given angle
    def find_angle(self,angle):
        if angle in self.theta and angle != 180:
            return self.theta.index(angle)
        
        elif angle == 180:
            return (len(self.theta)-1)
            
        else:
            print "Angle not found!"
            return (len(self.theta)-1)
    
    #Deletes elements of cross section and angle lists that are outside a given angle
    def angle_range(self,ran):
        #Make it exclusive on the bottom if it is not
        index = self.find_angle(ran)
        if index != (len(self.theta)-1):
            index = index + 1
        #that lack of enclusive slicing...ugh
        del self.theta[index:-1]
        del self.theta[-1]
        del self.sigma[index:-1]
        del self.sigma[-1]    
        
