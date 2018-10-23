
import cPickle as pickle
import numpy as np
from PIL import Image
from os import remove
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from ooi_func import printV, getIPData


# Define Functions:
def saveFig(fname, lgd):
    plt.savefig(fig_file + '.png',
                bbox_extra_artists=(lgd,),
                bbox_inches='tight')
    Image.open(fig_file+'.png').convert('RGB').save(fig_file + '.jpg', 'JPEG')
    remove(fig_file + '.png')


# Define Variables
t_window = 'year'
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
            printV('%s-%s-%s:' % (site.id, node.id, inst.id))
            printV('  %s' % stream.name)

            # Get IP Data
            inst = getIPData(inst, t_window)

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
            plt.ylabel(ylabs[ii-1])
            plt.title(inst.ipTitles[ii-1])
            plt.grid(True, linestyle='dashed', linewidth=2)

            # Tidy up the X-Axis
            ax = plt.gca()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%m-%d'))

            # Add Legend
            box_y = -.45*(1 + ((len(node.instruments)-1)*.225))
            lgd = plt.legend(loc='lower right', bbox_to_anchor=(1.005, box_y),
                             fontsize=20, frameon=False)

            # Save Figures
            fig_file = './' + site.id + '-'
            fig_file += inst.ipTitles[ii-1].replace(' ', '_')
            print(fig_file + '.png')
            saveFig(fig_file, lgd)
        break
    break
