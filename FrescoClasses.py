
#This is the tenenative class for graphs. It includes scaling for elastic fits.
class lineobject():
    def __init__ (self,theta,sigma,E,J,par,scale=1.0):
        self.E = E
        self.J = J
        self.par = par
        self.scale = scale
        self.theta = theta
        self.sigma = sigma
        
    def scaleit(self):
        if self.scale != 1.0:
            self.scaled_theta = []
            self.scaled_sigma = []
            for i in range(len(self.theta)): 
                self.scaled_theta.append(self.theta[i]/self.scale)
            for i in range(len(self.sigma)): 
                self.scaled_sigma.append(self.theta[i]/self.scale)

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
        
