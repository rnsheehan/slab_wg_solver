# Python script for running the Slab-Waveguide Solver executable
# and plotting the results of the solutions generated
# R. Sheehan 7 - 9 - 2016

"""
Import Libraries
"""

import os # operating system interface
import sys # system specific parameters and functions
import glob # use this to check whether certain files are in a directory
import subprocess # use this to run executables

import matplotlib.pyplot as plt #  this is needed for plotting solutions

"""
Function Definitions
"""

def list_1D_array(size):
	# return a python list of length size whose elements are all set to zero
    # indexing starts at zero and ends at size-1
	# alternative is to use [None]*size
	# this method uses list comprehensions

    return [0 for i in range(size)] if size > 0 else None

def list_2D_array(rows, columns):
    # return a 2D python list of size rows*columns whose elements are all set to zero
    # indexing starts at zero and ends at rows-1 / columns-1
    # array accessed as Z[row_index, col_index]
	
    if rows > 0 and columns > 0:
        
        ret_lst = list_1D_array(rows)

        for i in range(rows):
            ret_lst[i] = list_1D_array(columns)

        return ret_lst
    else:
        return None

def transpose_multi_col(data):
    # generate the transpose of a multi-column list
    # this will return the transpose of an array in a manner
    # that is convenient for plotting
    # this is arguably more convenient, and pythonic, than using the get_col or get_row method
    # this method assumes that each column has the same length

    return list( map( list, zip(*data) ) )

def get_matrix_dims(matrix):
    # retrieve the dimensions of a 2D array
    # R. Sheehan 18 - 5 - 2016

    if matrix is not None:
        row_size = len( matrix )
        col_size = len( matrix[0] )

        return [row_size, col_size]
    else:
        return None

def count_lines(thedata, thepath, quiet = 0):
    # count the number of lines in a file that has been opened and read into memory
    # thedata is the stream that contains the data from an open file
    # how do you know if thedata contains data?
    # assume that you only call count_lines inside another function for reading data
    # thepath is the name of the file containing the data
    # R. Sheehan 26 - 4 - 2014

    nlines=0
    for lines in thedata:
        nlines = nlines + 1
    if quiet:
        print "There are %(nlines)d lines in %(path)s"%{"nlines":nlines,"path":thepath}
    
    return nlines

def read_matrix(thepath, ignore_first_line = False, loud = False):
    # read an array of data from a file
    # if ignore_first_line == True, this means the first line of the file
    # contains text and should not be counted when reading in data
    # R. Sheehan 8 - 8 - 2014

    thefile = file(thepath,"r") # open file for reading

    # check that the files are available
    if thefile.closed:
        print "%(path)s could not be opened"%{"path":thepath}
        datapts = -1
    else:
        if loud: print "%(path)s is open"%{"path":thepath}

        thedata = thefile.readlines() # read the data from the file

        nrows = count_lines(thedata, thepath) # count the number of rows

        print "Nrows = ",nrows
        
        if ignore_first_line:
            ncols = len(thedata[1].split(',')) # count the number of columns
            nrows -= 1 # substract one from the number of rows
        else:
            ncols = len(thedata[0].split(',')) # count the number of columns

        if loud: print "rows = ",nrows,"cols = ",ncols

        #datapts = np.zeros([nrows, ncols]) # create an array of zeros of length nlines
        datapts = list_2D_array(nrows, ncols) # use the native list object instead of numpy
            
        for i in range(0, nrows, 1 ):
            for j in range(0, ncols,1):
                if ignore_first_line:
                    datapts[i][j] = float( thedata[i+1].split(',')[j] )
                else:
                    datapts[i][j] = float( thedata[i].split(',')[j] )
        
    del thefile

    return datapts

def run_slab_wg_solver(width, wavelength, n_core, n_sub, n_clad, storage):
    # run the executable for the slab waveguide solver

    # where is the executable located?
    exe_dir = "C:/Users/Robert/Programming/C++/Demo_Projects/Slab_WG_Slv/x64/Release/"

    # what is the name of the executable?
    # prog_name needs a space after it to distinguish it from arg_vals
    prog_name = "Slab_WG_Slv.exe" + " "

    # convert arguments to a string
    # need a space between arguments and "\\" added to storage
    arg_vals = "{:.5f}".format(width) + " " + "{:.5f}".format(wavelength) + " " \
               + "{:.5f}".format(n_core) + " " + "{:.5f}".format(n_sub) + " "\
               + "{:.5f}".format(n_clad) + " " +storage + "\\"

    print arg_vals

    # args is the value that is passed to subprocess
    args = exe_dir + prog_name + arg_vals

    # subprocess.call to run the program without printing to the python shell
    # shell=False is to be used as standard practice unless you
    # really know what you're doing!
    # output = subprocess.call(args, stdin=None, stdout=None, stderr=None, shell=False)

    # use subprocess.check if you want to print the output from the
    # program to the python shell
    # shell=False is to be used as standard practice unless you
    # really know what you're doing!
    print subprocess.check_output(args, shell=False)

def plot_dispersion_equations(data, polarisation, loud = False):
    # plot the TE and TM dispersion equations

    if data is not None and polarisation == "TE" or polarisation == "TM":

        col_label = 'r-' if polarisation == "TE" else 'g-'
        plt_label = "TE Dispersion Equation" if polarisation == "TE" else "TM Dispersion Equation"
        fig_label = "TE_Disp_Eqn.png" if polarisation == "TE" else "TM_Disp_Eqn.png"

        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        ax.plot(data[0], data[1], col_label, lw = 2)

        plt.xlabel(r'Propagation Constant $\beta (\mu m)^{-1}$', fontsize = 16)
        plt.ylabel('Dispersion', fontsize = 16)
        plt.title(plt_label)
        spacer = 1.0 if polarisation == "TE" else 10.0
        plt.axis( [data[0][0], data[0][-1], min(data[1]) - spacer, max(data[1]) + spacer] )

        plt.hlines(0.0, data[0][0], data[0][-1], 'k', 'solid', lw = 1.0) # line to indicate pi rad on plot

        #plt.text(0.1, line_h+0.1, r'$G = -3 (dB)$', fontsize=15, color = 'black')

        plt.savefig(fig_label)
        if loud: plt.show()
        plt.clf()
        plt.cla()
        plt.close()

def plot_mode(data, polarisation, width, loud = False):
    # plot a mode of the slab waveguide

    if data is not None and polarisation == "TE" or polarisation == "TM":

        labs = ['r-', 'g-', 'b-', 'm-', 'c-', 'k-' ] # plot labels
        dims = get_matrix_dims(data)

        plt_label = "TE Modes" if polarisation == "TE" else "TM Modes"
        fig_label = "TE_Modes.png" if polarisation == "TE" else "TM_Modes.png"

        # make a plot of the computed propagation constants

        min_vals = []
        max_vals = []
        
        fig = plt.figure()
        ax = fig.add_subplot(111)

        for i in range(1, min(dims[0], 7), 1):
            min_vals.append(min(data[i]))
            max_vals.append(max(data[i]))
            ax.plot(data[0], data[i], labs[i-1], lw = 2, label = "Mode %(v1)d"%{"v1":i})

        ax.legend(loc='best')
        plt.xlabel(r'Position $(\mu m)$', fontsize = 16)
        plt.ylabel('Slab Field', fontsize = 16)
        plt.title(plt_label)

        spacer = 1.0 if polarisation == "TE" else 0.01
        plt.axis( [data[0][0], data[0][-1], min(min_vals) - spacer, max(max_vals) + spacer] )

        plt.hlines(0.0, data[0][0], data[0][-1], 'k', 'solid', lw = 1.0)
        plt.vlines(-0.5*width, min(min_vals) - spacer, max(max_vals) + spacer, 'k', 'dashed', lw = 2)
        plt.vlines(0.5*width, min(min_vals) - spacer, max(max_vals) + spacer, 'k', 'dashed', lw = 2)

        #plt.text(0.1, line_h+0.1, r'$G = -3 (dB)$', fontsize=15, color = 'black')

        plt.savefig(fig_label)
        if loud: plt.show()
        plt.clf()
        plt.cla()
        plt.close()
        

def plot_slab_wg_results(width):
    # if everything has worked properly Slab_WG_Slv outputs the computed dispersion equation
    # and computed mode profiles in the files

    # plot the dispersion equations

    TE_disp_file = "TE_Dispersion_Eqn.txt"
    
    TM_disp_file = "TM_Dispersion_Eqn.txt"

    data = read_matrix(TE_disp_file)
    
    data = transpose_multi_col(data)

    plot_dispersion_equations(data, "TE", True)

    data = read_matrix(TM_disp_file)
    
    data = transpose_multi_col(data)

    plot_dispersion_equations(data, "TM", True)

    # plot the mode profiles
    TE_mode_file = "TE_Mode_Profiles.txt"
    
    TM_mode_file = "TM_Mode_Profiles.txt"

    data = read_matrix(TE_mode_file)
    
    data = transpose_multi_col(data)

    plot_mode(data, "TE", width, True)

    data = read_matrix(TM_mode_file)
    
    data = transpose_multi_col(data)

    plot_mode(data, "TM", width, True)
    
    
"""
Call and run script from inside main
"""

def main():
    pass

if __name__ == '__main__':
    main()
    
    # what arguments are needed by prog_name?
    # Slab_WG_Slv needs
    width = 2.5
    wavelength = 1.55
    n_core = 3.38
    n_sub = 3.17
    n_clad = 1.0

##    width = input("Enter waveguide width (um): ")
##    wavelength = input("Enter operating wavelength (um): ")
##    n_core = input("Enter core refractive index: ")
##    n_sub = input("Enter substrate refractive index: ")
##    n_clad = input("Enter cladding refractive index: ")
    
    storage = os.getcwd() # store the solutions in the current directory

    run_slab_wg_solver(width, wavelength, n_core, n_sub, n_clad, storage)

    plot_slab_wg_results(width)


