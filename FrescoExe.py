import os


def filerun():
    filename = raw_input("Name of input file? ")
    output = str(filename)+'.out'
    command = 'fresco' + '<' + filename + '>' + output
    os.system(command)
    

filerun()
