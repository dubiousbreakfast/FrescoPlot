
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

