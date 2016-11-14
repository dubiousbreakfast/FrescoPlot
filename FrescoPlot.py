import matplotlib
import matplotlib.pyplot as plt
import numpy
import os
import seaborn as sbs
import FrescoClasses as fc


sbs.set_context('poster')

class CrossSectionPlot():

    def __init__(self,files,data=None,q_name=None):
        self.lines = []
        #Create the list of lineobjects from file names given. If not given iterable it is assumed to be a single file.
        #Can also pass list of lineobjects
        if isinstance(files,tuple):
            for ele in files:
                self.lines.append(fc.read_cross(ele))
        elif isinstance(files,str):
            self.lines.append(fc.read_cross(files))
        else:
            for ele in files:
                self.lines.append(ele)
            
        self.data = data

        #Initialize the plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        
    #Reads in data from a lineobject and scales the values to a point    
    def scale(self,factor=None):
        if factor:
            for line in self.lines:
                line.scale_it(factor,0,True)
        else:
            for i,j in enumerate(self.data.theta):
                print '{0} {1}'.format(j,self.data.sigma[i])
            scale_angle = float(raw_input("Scale angle(Ex. 1, 1.5, etc.)?"))
            scale_value = float(raw_input("Scale value?"))
            for line in self.lines:
                line.scale_it(scale_value,scale_angle)


    #method for labeling fits by J^Pi
    def label(self):
        pass

    #draw the plot and set prameters. Saving and titles will be done through widget for now
    def plot(self,angle=None):
        wid = 1.3
        if self.data:
            if self.data.erry or self.data.errx:
                self.ax.errorbar(self.data.theta,self.data.sigma,yerr=self.data.erry,xerr=self.data.errx,lw=wid,fmt='o')
                
            else:
                self.ax.plot(self.data.theta,self.data.sigma,'ro')
        for line in self.lines:
            if angle:
                x,y = line.angle_range(float(angle))
            else:    
                x,y = line.theta,line.sigma
            self.ax.plot(x,y)

        self.ax.set_xlabel(r'$\theta$',fontsize = 25)
        self.ax.set_ylabel(r'$\sigma(mb)$',fontsize = 25)
        self.ax.tick_params(axis='x', labelsize=15)    
        self.ax.tick_params(axis='y', labelsize=15)
        self.ax.set_yscale('log')
        self.fig.show()

    #Quick plots are intended for one off plots just to check general features of a cross section.
    #Options are for auto saving figures for sensitivity studies.
    def quick_plot(self,q_name):
        for line in self.lines:
            x,y = line.theta,line.sigma
        self.ax.plot(x,y)
        self.ax.set_xlabel(r'$\theta$',fontsize=25)
        self.ax.tick_params(axis='x', labelsize=15)    
        self.ax.set_ylabel(r'$\sigma(mb)$',fontsize = 25)
        self.ax.tick_params(axis='y', labelsize=15)
        self.ax.set_yscale('log')
        if q_name:
            self.fig.savefig(q_name+'.png',format='png') #Just default to png, since is just for quick check
        else:
            self.fig.show()

    #Multiple Plots based on the seaborn FacetGrid
    def multi_plot(self):
        pass
        






# plotparity = 0 

# if n%2 != 0: plotparity = 1 #determines if there are an even or odd amount of plots, so that odd plots can be centered 

# f=[]

# scale = 1 #set to 1 for log scale else 0



# if plotparity == 1:
#     for x in range((n+1)/2):                                             #creates subplots using a nx3 grid leaving the middle column blank 
#         if len(f) == (n-1):
#             f.append(plt.subplot2grid((((n+1)/2),3),(((n+1)/2)-1,1)))
#         else:
#             for j in range(2):
#                 y = 2*j                          
#                 f.append(plt.subplot2grid((n,3),(2*x,y)))
        
# else:
#     for x in range((n+1)/2):
#         for j in range(2):
#             y = 2*j                          
#             f.append(plt.subplot2grid((n,3),(2*x,y)))

# for x in range(n):
#     f[x].plot(graphs[x].theta,graphs[x].sigma)
#     f[x].set_title(str(graphs[x].E)+' Mev')    
#     f[x].set_xlabel(r'$\theta$',fontsize = 20)
#     f[x].set_ylabel(r'$\sigma(mb)$',fontsize = 20)
#     f[x].tick_params(axis='x', labelsize=8)    
#     f[x].tick_params(axis='y', labelsize=8)
#     if scale == 1: f[x].set_yscale('log')	

        
# plt.errorbar(expt,exps,xerr = 5,fmt = 'ro',lw=2)

# plt.savefig('multi_plot_test.pdf')
# plt.draw()
# plt.show() 




# The rest of these lines are for labeling of states on the plot with arrows
# At this point they are not used. 


# plt.ylim(0,2)


# plt.annotate('',xy=(40, 10E-08),xytext=(40, 0.2177E-05),
#                 arrowprops=dict(facecolor='black'))
#                 horizontalalignment='down', verticalalignment='bottom',
#                 )
# plt.annotate('0+',xy=(20,.000001),fontsize = 20,weight = 'bold')
# plt.annotate('3-',xy=(30,.0001),fontsize = 20,weight = 'bold')
# plt.annotate('2+',xy=(50,.00001),fontsize = 20,weight = 'bold')
