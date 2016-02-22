import os


def filerun(filename):
    output = str(filename)+'.out'
    command = 'fresco' + '<' + filename + '>' + output
    os.system(command)
    


