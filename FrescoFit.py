
import numpy as np
from scipy import interpolate
from scipy import optimize as opt
import FrescoClasses as fc
#This file will provide all the algorithms for doing a  
#chi-squared minimization on the the fresco generated cross sections
count = 0

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
    #print ((theory-exper)/(err))**2.0
    return ((theory-exper)/(err))**2.0


#Pretty much the heart of this code given all the inputs changes potential values,
#runs fesco, creates new spline, returns chisquare for minimization.
def elastic_chi(val,fresco,data,pot,term,var):
    #print val
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


#All BFGS based algorithms seem wonky. nelder-mead works fine, but min is far, far away from initial values

def elastic_fit(fresco,data,pot,term,var,bnds=None): #var are the potential parameters to be changed. Optionally bounds may be used to constrain minimization
    fresco = fc.FrescoInput(fresco)
    data = fc.read_data(data)
    x0 = [] #Initial values for potentials
    #Find intial values
    for ele in var:
        for line in fresco.sorted_pots[pot][term]:#Just in case potential has two lines
            if ele in line:
                init = fresco.find_value(ele,line,'=')
                x0.append(float(init))
    x0 = np.asarray(x0)
    f_args = (fresco,data,pot,term,var) #addition arguments for chi^2 function
    #result = opt.basinhopping(elastic_chi,x0,minimizer_kwargs={'method':'SLSQP','args':f_args,'bounds':bnds,'options':{'eps':0.1}},niter=100,stepsize=.01,T=.01)
    result = opt.minimize(elastic_chi,x0,method='nelder-mead',args=f_args)
    return result
