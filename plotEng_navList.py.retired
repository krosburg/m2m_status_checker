from ooi_web import writeNavHeader, writeEngNavNodeLI, writeNavFooter
from ooi_web import writeENGSummary
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle


# Define Variables
web_file = '/var/www/html/engm2m/navigationFile.html'
eng_file = 'rsn_eng_streams.pkl'

# Load RSN Data Structure
print('Loading %s' % eng_file)
with open(eng_file, 'rb') as input:
    rsn = pickle.load(input)

# Print HTML Header
writeNavHeader(web_file, 'M2M Engineering Page')

# Print Summary Links
writeENGSummary(web_file)

# Loop on Sites, Nodes, Instruments, Streams
for site in rsn.sites:
    if not site.nodes:
        continue

    # Loop on Nodes for Site
    for node in site.nodes:
        if not node.instruments:
            continue

        # Filter Instruments to IP Only
#        node.filtIPOnly()
        if not node.instruments:
            continue

        writeEngNavNodeLI(web_file, node.id)

# Finalize HTML FILE
writeNavFooter(web_file)
