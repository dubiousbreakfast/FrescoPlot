import matplotlib
import matplotlib.pyplot as plt
import numpy
import re



#class for each line at a given energy

class lineobject():
    def __init__ (self,theta,sigma,E):
        self.theta = theta
        self.sigma = sigma
        self.E = E
    
    


#reads files in and creates lineobject for each energy.
#outputs graphline list which is a single list containing each lineobject as a element.

def readfile(filename):
    
    graphline = []
    theta = []
    sigma = []
    global n  #total number of partitions
    n = 0
    for line in file(filename): 
        line = line.split()
        if line[0] == '#legend':
            energy = re.findall('[0-9.0]+',line[6])   #picks out the lab energy
            E = float(energy[0])
        if len(line) == 2 and line[0] != '@legend' and line[0] != '@subtitle':
            theta.append(float(line[0]))              #finds theta and sigma values for each energy    
            sigma.append(float(line[1]))
        if line[0] == 'END':
            z = lineobject(theta,sigma,E)
            graphline.append(z)
            n = n + 1
            theta = []
            sigma = []
    
    return graphline
     




graphs = readfile('fort.16')


plotparity = 0 

if n%2 != 0: plotparity = 1 #determines if there are an even or odd amount of plots, so that odd plots can be centered 

f=[]

scale = 1 #set to 1 for log scale else 0



if plotparity == 1:
    for x in range((n+1)/2):                                             #creates subplots using a nx3 grid leaving the middle column blank 
        if len(f) == (n-1):
            f.append(plt.subplot2grid((((n+1)/2),3),(((n+1)/2)-1,1)))
        else:
            for j in range(2):
                y = 2*j                          
                f.append(plt.subplot2grid((n,3),(2*x,y)))
        
else:
    for x in range((n+1)/2):
        for j in range(2):
            y = 2*j                          
            f.append(plt.subplot2grid((n,3),(2*x,y)))

for x in range(n):
    f[x].plot(graphs[x].theta,graphs[x].sigma)
    f[x].set_title(str(graphs[x].E)+' Mev')    
    f[x].set_xlabel(r'$\theta$',fontsize = 20)
    f[x].set_ylabel(r'$\sigma(mb)$',fontsize = 20)
    f[x].tick_params(axis='x', labelsize=8)    
    f[x].tick_params(axis='y', labelsize=8)
    if scale == 1: f[x].set_yscale('log')	

        
#plt.errorbar(expt,exps,xerr = 5,fmt = 'ro',lw=2)

plt.savefig('multi_plot_test.pdf')
plt.draw()
plt.show() 




#The rest of these lines are for labeling of states on the plot with arrows
#At this point they are not used. 


#plt.ylim(0,2)


#plt.annotate('',xy=(40, 10E-08),xytext=(40, 0.2177E-05),
                #arrowprops=dict(facecolor='black'))
                #horizontalalignment='down', verticalalignment='bottom',
                #)
#plt.annotate('0+',xy=(20,.000001),fontsize = 20,weight = 'bold')
#plt.annotate('3-',xy=(30,.0001),fontsize = 20,weight = 'bold')
#plt.annotate('2+',xy=(50,.00001),fontsize = 20,weight = 'bold')
