import cPickle as pickle
from ooi_func import printV

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

        # Loop on Instrument for Node
        for inst in node.instruments:
            # Skip if No Streams
            if not inst.streams:
                print('skippin!')
                continue

            # Filter to Science Streams
            streams = [s for s in inst.streams if s.isScienceData()]

            # Skip if Empty
            if not streams:
                continue

            # Print Results
            printV('%s-%s-%s:' % (site.id, node.id, inst.id))
