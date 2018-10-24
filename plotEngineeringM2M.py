import sys
import matplotlib
matplotlib.use('Agg')
import numpy as np
from PIL import Image
from os import remove
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from ooi_func import printV, getIPData
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle


# Define Functions:
def saveFig(fname, lgd):
    plt.savefig(fname + '.png',
                bbox_extra_artists=(lgd,),
                bbox_inches='tight')
    Image.open(fig_file+'.png').convert('RGB').save(fig_file + '.jpg', 'JPEG')
    remove(fig_file + '.png')

def getArgs():
    """Retrieves importand cmd-line args."""
    if len(sys.argv) < 2:
        print('No time windows supplied, using day.')
        return 'day'
    else:
        t_win = str(sys.argv[1]).lower()
        if t_win not in ['day', 'week', 'month', 'year']:
            raise Exception('Invalid time window, using day')
            return 'day'
        return t_win


# Define Variables
t_window = getArgs()
img_dir = '/var/www/html/engm2m/images/' + t_window + '/'
tstrs = ['Port Currents', 'Port Temps', 'Port GFD High', 'Port GFD Low']
ylabs = ['milliAmps', 'deg', 'microAmps', 'microAmps']

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

    # Loop on Nodes for Site
    for node in site.nodes:
        # Skip if No Instruments
        if not node.instruments:
            continue

        # Filter Instruments to IP Only
        node.filtIPOnly()

        # Loop on Instrument for Node
        for inst in node.instruments:
            # Skip if No Streams
            if not inst.streams:
                continue

            # Isoloate Stream
            stream = inst.streams[0]

            # Print Results
            printV('%s-%s-%s' % (site.id, node.id, inst.id))

            # Get IP Data
            inst, t_start, t_end = getIPData(inst, t_window)
            if not inst:
                continue

            # Loop on IP Parameters to Plot
            figNum = 1
            for data in inst.ipData:
                # Instantiate/Switch-to the Figure
                fig = plt.figure(figNum, figsize=(18, 4.475))

                # Assemble Plot Label
                plt_lab = 'J%s avg: %2.2f, max: %2.2f' % (inst.id,
                                                          np.nanmean(data),
                                                          np.nanmax(data))
                # Plot Data
                plt.plot(inst.time, data, label=plt_lab)
                figNum += 1

        # Loop Back Through Figures to Add Important Info
        for ii in range(1, 5):
            # Switch To Figure
            fig = plt.figure(ii, figsize=(18, 4.475))

            # Add Y-Label, Title, and Grid
            tstr = node.id + ' ' + tstrs[ii-1]
            plt.xlim(t_start, t_end)
            plt.ylabel(ylabs[ii-1])
            plt.title(tstr)
            plt.grid(True, linestyle='dashed', linewidth=2)

            # Tidy up the X-Axis
            ax = plt.gca()
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%m-%d-%y'))

            # Add Legend
            box_y = -.45*(1 + ((len(node.instruments)-1)*.225))
            lgd = plt.legend(loc='lower right', bbox_to_anchor=(1.005, box_y),
                             fontsize=20, frameon=False)

            # Save Figures
            fig_file = img_dir + site.id + '-' + tstr.replace(' ', '_')
            print(fig_file + '.png')
            saveFig(fig_file, lgd)
        plt.close('all')
