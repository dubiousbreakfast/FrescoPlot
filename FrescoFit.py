
import numpy as np
from scipy import interpolate
from scipy import optimize as opt
import FrescoClasses as fc
import FrescoPlot as fp
#This file will provide all the algorithms for doing a  
#chi-squared minimization on the the fresco generated cross sections

#First we must create a function from the fresco output
#This uses a cubic spline with documentation found at
#http://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
#Give it an instance of lineobject from frescoclasses and desired angle.
def cross_interpolate(cross):
    x = cross.theta
    y = cross.sigma
    return interpolate.splrep(x,y)
    


#Just function to return chi squared for chi-squared minimization.
def chi_sq(theory,exper,err):
    return ((theory-exper)/(err))**2.0


#Pretty much the heart of this code given all the inputs changes potential values,
#runs fresco, creates new spline, returns chisquare for minimization.
def elastic_chi(val,fresco,data,pot,term,var):
    for i,j in zip(var,val):
        fresco.change_pot(pot,term,i,str(j)) #Change potentials
    fresco.update_all()
    fresco.write('new_input')
    fc.filerun('new_input')
    cross = fc.read_cross('fort.201')
    spline = cross_interpolate(cross)
    theory = interpolate.splev(data.theta,spline)
    exper = data.sigma
    err = data.errx #Might need to consider aysmmetric data in future. Keep eye out.
    chi_list = map(chi_sq,theory,exper,err)
    return .5*np.sum(chi_list)
        


#trying to enforce bounds on the basin hopping with this condition. Ripped straight from scipy page

class BasinBounds(object):
    def __init__(self, xmax, xmin): #should pass upper and lower bounds that we want to the object
         self.xmax = np.array(xmax)
         self.xmin = np.array(xmin)
    def __call__(self, **kwargs):
         x = kwargs["x_new"] #proposed values passed by minimizer
         tmax = bool(np.all(x <= self.xmax)) #see if they fall within range
         tmin = bool(np.all(x >= self.xmin))
         return tmax and tmin

#Because of the constrains by the scipy otimize package this needed to be a class, or I would have had global variables out the ass.
class ElasticFitBasin():

    def __init__(self,fresco,data,pot,term,var,percent_range=.2): #user selects what range they want to vary potentials within defualts to 20%
        self.fresco = fc.FrescoInput(fresco)
        self.data = fc.read_data(data)
        self.f_args = (self.fresco,self.data,pot,term,var) #tuple of arguments to be passed to chi square function 
        self.x0 = [] #inital potential parameters
        for ele in self.f_args[4]: 
            for line in self.fresco.sorted_pots[self.f_args[2]][self.f_args[3]]:#Just in case potential has two lines
                if ele in line:
                    init = self.fresco.find_value(ele,line,'=')
                    self.x0.append(float(init))
        self.x0 = np.asarray(self.x0)
        self.init_chi = elastic_chi(self.x0,*self.f_args) #get inital chi square value
        print "The initial chi squared value is ",self.init_chi 
        self.init_cs = fc.read_cross('fort.201') #the inital cross section data
        self.iterations = 0 #number of basin hops completed
        self.bounds = self.set_bounds(percent_range) #range we are allowed to jump around in. We will still sample, but auto rejected outside this range 

        #These are default parameters that can be set with set_basin
        self.T = 1.0
        self.steps = 50
        self.step_size = .1
        
    def plot(self):
        new_cs = fc.read_cross('fort.201') #the cross section for the fitted data
        plot = fp.CrossSectionPlot([self.init_cs,new_cs],self.data) #create the plot with new_cs vs init_cs vs the data
        plot.ax.set_title('Best Fit')
        plot.plot()

    #callback function that is passed data after each basin iteration    
    def print_fun(self,x, f, accepted):
        self.iterations = self.iterations + 1
        print("at minimum %.4f accepted %d iteration %d" % (f, int(accepted),self.iterations))

    #method that creates a BasinBounds object and returns. Upper and lower created from allowed percent variation
    def set_bounds(self,percent):
        upper = []
        lower = []
        for ele in self.x0: 
                lower.append(ele - (percent*ele))
                upper.append(ele + (percent*ele))
        bounds = BasinBounds(upper,lower)
        return bounds 

    #asks user to give metrolpolis parameters
    def set_basin(self):
        T = float(raw_input('What temperature do you want?'))
        self.T = T
        steps = int(raw_input('How many steps?'))
        self.steps = steps
        step_size = float(raw_input('How large should the trial steps be?'))
        self.step_size = step_size

    #start a basin run
    def run(self):
        result = opt.basinhopping(elastic_chi,self.x0,minimizer_kwargs={'method':'COBYLA','args':self.f_args},
                                  niter=self.steps,stepsize=self.step_size,T=self.T,callback=self.print_fun,accept_test=self.bounds)
        #now use the best result to generate the fit
        elastic_chi(result.x,*self.f_args)
        self.plot()
        
