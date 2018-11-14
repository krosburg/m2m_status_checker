from ooi_web import writeNavHeader, writeEngNavNodeLI, writeNavFooter
from ooi_web import writeENGSummary

node_list = ['LJ01A', 'LJ01B', 'LJ01C', 'LJ01D', 'LJ03A', 'LV01A', 'LV01B',
             'LV01C', 'LV03A', 'MJ01A', 'MJ01B', 'MJ01C', 'MJ03A', 'MJ03B', 
             'MJ03C', 'MJ03D', 'MJ03E', 'MJ03F', 'PC01A', 'PC01B', 'PC03A',
             'PD01A', 'PD01B', 'PD03A', 'SF01A', 'SF01B', 'SF03A']


# Define Variables
web_file = '/var/www/html/engm2m/navigationFile.html'

# Print HTML Header
writeNavHeader(web_file, 'M2M Engineering Page')

# Print Summary Links
writeENGSummary(web_file)

# Loop on Sites, Nodes, Instruments, Streams
for node in node_list:

    writeEngNavNodeLI(web_file, node)

# Finalize HTML FILE
writeNavFooter(web_file)
