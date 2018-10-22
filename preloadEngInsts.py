import requests
import time
import ooi_classes as ooi
import cPickle as pickle
from ooi_func import printV, getStreamType, getData
from ooi_func import getSites, getInstruments, getStreams
from ooi_globals import U, wanted_nodes


# Disable Annoying HTTPS Warnings
requests.packages.urllib3.disable_warnings()

# Engineering Only or Science Only? (True=Eng,False=Sci)
ENG_ONLY = True

# Instantiate a Container
rsn = ooi.Array()

# Loop on Sites
for siteID in getSites():

    # Define A New Site Instance
    newSite = ooi.Site(name='', siteID=siteID)

    # Requests Nodes at a Given Site
    printV('Getting nodes for %s' % siteID)
    res = getData(U + siteID)

    # Filter Node List for Nodes in the Wanted Nodes List
    nodeIDs = [node for node in res if node in wanted_nodes]

    # Skip if Empty
    if not nodeIDs:
        continue

    # Loop on Nodes for the Given Site
    for nodeID in nodeIDs:

        # Create New Node Object
        newNode = ooi.Node(name='', nodeID=nodeID, parSite=siteID)

        # Request Instruments at Given Node
        printV('  Getting instruments for %s' % nodeID)
        instIDs = getInstruments(siteID, nodeID, ENG_ONLY)

        # Skip if No Instruments
        if not instIDs:
            continue

        # Loop on Instruments for the Given Node
        for instID in instIDs:

            # Create New Instrument Object
            newInst = ooi.Inst(name='',
                               instID=instID,
                               parSite=siteID,
                               parNode=nodeID)

            # Get Streams for Instrument
            streams = getStreams(siteID, nodeID, instID)

            # Skip if no Streams
            if not streams:
                continue

            # Loop on Streams
            for stream in streams:

                # Add Stream to Instrument
                printV('       Adding stream %s to inst %s' % (stream, instID))
                newInst.addStream(name=stream,
                                  method='',
                                  stream_type=getStreamType(stream),
                                  parSite=siteID,
                                  parNode=nodeID,
                                  parInst=instID)

            # Add Instrument to Node
            printV('      Adding inst %s to node %s' % (instID, nodeID))
            newNode.addInst(newInst)

        # Add Node to Site
        printV('    Adding node %s to site %s' % (nodeID, siteID))
        newSite.addNode(newNode)

    # Add Site to Container
    printV('  Adding site %s to array container...' % siteID)
    rsn.addSite(newSite)

    printV(' ')
    time.sleep(3)

# Save The Structure
out_file = './rsn_eng_streams.pkl'
print('Saving as ' + out_file + '... ', '')
with open(out_file, 'wb') as output:
    pickle.dump(rsn, output, pickle.HIGHEST_PROTOCOL)
print('Done!')
