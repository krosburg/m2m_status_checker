import ooi_web as o
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle


# Define Variables
web_file = '/var/www/html/kcrtest/navigationFile.html'
rsn_file = 'rsn_streams.pkl'

# Load RSN Data Structure
print('Loading %s' % rsn_file)
with open(rsn_file, 'rb') as input:
    rsn = pickle.load(input)

# Print HTML Header
o.writeNavHeader(web_file, 'M2M Engineering Page')

# Loop on Sites, Nodes, Instruments, Streams
for site in rsn.sites:
    if not site.nodes:
        continue

    # Loop on Nodes for Site
    for node in site.nodes:
        if not node.instruments:
            continue

        node.instruments = [i for i in node.instruments
                            if 'ENG' not in i.name
                            and 'IP' not in i.name]

        if not node.instruments:
            continue

        # Write Node Item
        o.writePlotNodeLI(web_file, node.id)

        # Loop on Instruments
        for inst in node.instruments:
            o.writePlotNavInstLI(web_file, node.id, inst.id)

        o.writePlotNodeEnd(web_file)

# Finalize HTML FILE
o.writeNavFooter(web_file)
