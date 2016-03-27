import matplotlib
import matplotlib.pyplot as plt
import numpy
import FrescoReader as fr
import os
import seaborn as sbs

     


#Set up the plots
def now_plot(notaplot,data=None):
    aplot = plt.subplot()
    #Everything to do with data so scaling+plotting right now
    if data:
        scalebool = raw_input("Scale to data point y or n? \n")
        if scalebool == 'y':
            for i,j in enumerate(data.theta):
                print '{0} {1}'.format(j,data.sigma[i])
            scale_angle = int(raw_input("Scale angle(integer value)?"))
            scale_value = float(raw_input("Scale value?"))
            notaplot.scale_it(scale_value,scale_angle)
        aplot.plot(data.theta,data.sigma,'g^')
    x,y = notaplot.angle_range(float(raw_input("Stop plotting at which angle? \n")))
    aplot.plot(x,y)
    #Finish setting up plots
    aplot.set_title(str(notaplot.E)+' Mev $J^\pi = $'+notaplot.J+notaplot.par)    
    aplot.set_xlabel(r'$\theta$',fontsize = 20)
    aplot.set_ylabel(r'$\sigma(mb)$',fontsize = 20)
    aplot.tick_params(axis='x', labelsize=10)    
    aplot.tick_params(axis='y', labelsize=10)
    aplot.set_yscale('log')
    return aplot


    

#read in files
#Still have to enter data in same order as graphs right now
all_files = fr.getfiles('fort.200')
all_data = fr.getfiles('data')
graphs = []
data_graphs = []

#set up graph objects
graphs[:] = [fr.readfres200(fr.readfile(x)) for x in all_files]
data_graphs[:] = [fr.read_data(fr.readfile(x)) for x in all_data]


#Now plot them all
for i,j in enumerate(graphs):
    try:
        oneplot = now_plot(j,data_graphs[i])
    except IndexError:
        oneplot = now_plot(j)
    plt.savefig(j.J+j.par+' plot.pdf')
    plt.draw()
    plt.clf()

    


# #for i in range(len(graphs)):
#     if i <= len(data_graphs):
#         oneplot = now_plot(graphs[i],data_graphs[i])
#     else:
#         oneplot = now_plot(graphs[i])







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
