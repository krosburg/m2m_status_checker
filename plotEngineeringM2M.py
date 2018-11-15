import sys
import matplotlib
matplotlib.use('Agg')
import numpy as np
from PIL import Image
from os import remove
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from datetime import datetime
from ooi_func import getIPData, getTimeWinArg, getPDData
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle


# Define Functions:
def saveFig(fname, lgd):
    """Saves the figure"""
    if err_flag:
        plt.savefig(fname + '.png', bbox_inches='tight')
    else:
        plt.savefig(fname + '.png',
                    bbox_extra_artists=(lgd,), 
                    bbox_inches='tight')
    Image.open(fname + '.png').convert('RGB').save(fname + '.jpg', 'JPEG')
    remove(fname + '.png')


def saveFigNL(fname):
    """Saves the figure"""
    plt.savefig(fname + '.png', bbox_inches='tight')
    Image.open(fname + '.png').convert('RGB').save(fname + '.jpg', 'JPEG')
    remove(fname + '.png')


def makePlotNice():
    """Add xlims, ylabel, title, and grid to plot"""
    plt.xlim(t_start, t_end)
    plt.ylabel(ylabs[ii-1], fontsize=label_size, fontweight=label_wt)
    plt.title(tstr, fontsize=title_size, fontweight=title_wt)
    plt.grid(True, linestyle='dashed', linewidth=2)

def tidyXAxis(date_fmt, tsize):
    """Formats xaxis dates"""
    ax = plt.gca()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt))
    plt.tick_params(labelsize=tsize)

def addLegend():
    """Adds legend to plot."""
    box_y = -.50*(1 + ((len(node.instruments)-1)*.225))
    return plt.legend(loc='lower right', bbox_to_anchor=(1.005, box_y),
                      fontsize=20, frameon=False)

def errorPlot():
    """Plots default error plot and returns new x-axis limits."""
    print('No Data. Making error plot.')
    plt.plot()
    plt.text(0, 0, 'ERROR',
             ha='center', va='center', size=60, color='red')
    plt.text(0, -0.02, 'No Data Returned from M2M Query',
             ha='center', va='center', size=40, color='black')
    return plt.xlim()


# Define Variables
t_window = getTimeWinArg()
img_dir = '/var/www/html/engm2m/images/' + t_window + '/'
tstrs = ['Port Currents', 'Port Temps', 'Port GFD High', 'Port GFD Low']
ylabs = ['milliAmps', 'deg', 'microAmps', 'microAmps']

# Define Plotting Variables
label_size = 23
title_size = 30
value_size = 22
legtx_size = 24
label_wt = "bold"
title_wt = "bold"

# Define RSN Streams Object File
in_file = 'rsn_eng_streams.pkl'


# Load RSN Data Structure
print('Loading %s' % in_file)
with open(in_file, 'rb') as input:
    rsn = pickle.load(input)

# Loop on Sites, Nodes, Instruments, Streams
for site in rsn.sites:
    # Skip if No Nodes
    if not site.nodes:
        continue

    # Filter only for PD nodes
    nodes = [n for n in site.nodes if 'PD' not in n.id]

    # Loop on Nodes for Site
    for node in nodes:
        print(datetime.now())
        # Skip if No Instruments
        if not node.instruments:
            continue

        # Skip "Bad" site-node pairs
        if site.id == "RS01OSBP":
            if node.id == "PC01B" or node.id == "SF01B":
                continue
        elif site.id == "RS01SUM1":
            continue

        # Filter Instruments to IP Only
        node.filtIPOnly()

        # Loop on Instrument for Node
        err_flag = True
        for inst in node.instruments:

            # Skip if No Streams
            if not inst.streams:
                continue

            # Get IP Data
            inst, t_start, t_end = getIPData(inst, t_window)

            if not inst:
                print(' Data return empty: Skipping...')
                continue
            else:
                err_flag = False

            # Loop on IP Parameters to Plot
            figNum = 1
            for data in inst.ipData:
                # Assemble Plot Label
                plt_lab = 'J%s avg: %2.2f, max: %2.2f' % (inst.id,
                                                          np.nanmean(data),
                                                          np.nanmax(data))
                # Instantiate Figure and Plot Data; Incrament Counter
                fig = plt.figure(figNum, figsize=(18, 4.475))
                plt.plot(inst.time, data, label=plt_lab)
                figNum += 1

        # Loop Back Through Figures to Add Important Info
        for ii in range(1, 5):
            # Switch To Figure
            fig = plt.figure(ii, figsize=(18, 4.475))

            if err_flag:
                t_start, t_end = errorPlot()

            # Add Y-Label, Title, and Grid
            tstr = node.id + ' ' + tstrs[ii-1]
            makePlotNice()

            # Tidy up the X-Axis
            if not err_flag:
                tidyXAxis('%H:%M\n%m-%d-%y', value_size)

            # Setup File Names
            fig_file = img_dir + site.id + '-' + tstr.replace(' ', '_')
            print(fig_file + '_NL.png updated')
            saveFigNL(fig_file + '_NL')

            # Add Legend
            if err_flag:
                lgd = []
            else:
                lgd = addLegend()

            # Save Figures
            fig_file = img_dir + site.id + '-' + tstr.replace(' ', '_')
            print(fig_file + '.png updated')
            saveFig(fig_file, lgd)
        plt.close('all')
        print(' ')


# == NOW PLOT ONLY FOR PD STREAMS ===========
with open(in_file, 'rb') as input:
    rsn = pickle.load(input)
tstrs = ['Dock Temperature', 'Dock 12 Volt Current', 'Dock Humidity']
# Loop on Sites, Nodes, Instruments, Streams
for site in rsn.sites:
    # Skip if No Nodes
    if not site.nodes:
        continue

    # Filter only for PD nodes
    nodes = [n for n in site.nodes if 'PD' in n.id]

    # Skip if filtering results in empty list
    if not nodes:
        continue

    # Loop on Nodes for Site
    for node in nodes:
        print('%s %s-%s' % (datetime.now(), site.id,node.id))
        # Skip if No Instruments
        if not node.instruments:
            continue

        # Loop on Instrument for Node
        err_flag = True
        for inst in node.instruments:

            # Skip if No Streams
            if not inst.streams:
                continue

            # Get IP Data
            inst, t_start, t_end = getPDData(inst, t_window)

            if not inst:
                print(' Data return empty: Skipping...')
                continue
            else:
                err_flag = False


            # Plot Temperature
            fig = plt.figure(1, figsize=(18, 4.475))
            plt.plot(inst.time, inst.data[0], label='Dock Temp')
            plt.plot(inst.time, inst.data[1], label='Heat Sink Temp')
            if err_flag:
                t_start, t_end = errorPlot()
                

            # Plot Current
            fig = plt.figure(2, figsize=(18, 4.475))
            plt.plot(inst.time, inst.data[2], label='12 Volt Current')
            if err_flag:
                t_start, t_end = errorPlot()

            # Plot Current
            fig = plt.figure(3, figsize=(18, 4.475))
            plt.plot(inst.time, inst.data[3], label='Relative Humidity')
            if err_flag:
                t_start, t_end = errorPlot()

            # Return toe ach plot and clean up
            for ii in range(1, 3):
                fig = plt.figure(ii, figsize=(18, 4.475))
                tstr = node.id + ' ' + tstrs[ii-1]
                makePlotNice()
                if err_flag:
                    lgd = []
                else:
                    tidyXAxis('%H:%M\n%m-%d-%y', value_size)
                    lgd = addLegend()
                fig_file = img_dir + site.id + '-' + tstr.replace(' ', '_')
                print(fig_file + '.png updated')
                saveFig(fig_file, lgd)
            plt.close('all')
        print(' ')
