import requests
import ooi_classes as ooi
from ooicreds import UKEY, TOKE

# Disable Annoying HTTPS Warnings
requests.packages.urllib3.disable_warnings()

# Status, Verify, and Timeout Variables
SUCCESS_CODE = 200
VERIFY = False
TIMEOUT = 10

# M2M URLs
BASE_URL = 'https://ooinet.oceanobservatories.org/api/m2m/'
PRELOAD_URL = BASE_URL + '12575/stream/byname/'
U = BASE_URL + '/12576/sensor/inv/'

# Verbose? (boolean)
VERB = True

# Engineering Only or Science Only? (True=Eng,False=Sci)
ENG_ONLY = False

# Setup Nodes of Interest List
wanted_nodes = ['LJ01A', 'MJ01A', 'SF01A', 'PC01A', 'LJ01B', 'DP01A',
                'MJ01B', 'LJ01C', 'SF01B', 'PC01B', 'DP01B', 'MJ01C',
                'LJ01D', 'MJ03A', 'LJ03A', 'PC03A', 'SF03A', 'MJ03B',
                'MJ03E', 'MJ03F', 'DP03A', 'MJ03C', 'MJ03D']


# =============================================================================
# == BEGIN FUNCTION DEFINITIONS ===============================================
# =============================================================================

# == Define printV Helper Function ============================================
def printV(msg):
    """printV(msg [string]): Prints MSG if the global variable VERB=True."""
    if VERB:
        print(msg)


# == Define isScienceStream Helper Function ===================================
def getStreamType(stream_name):
    """Returns type of stream (science, engineering, etc.)."""
    return getData(PRELOAD_URL + stream_name)['stream_type']['value']


# == Define getData Helper Function ===========================================
def getData(url):
    """getData(url): Given a full URL, contacts the M2M server using Python's
    request.get() routine, supplying credentials using global variables UKEY,
    TOKE & timeout & verification flags using globals TIMEOUT & VERIFY.
    Checks the result against global SUCCESS_CODE variable (usually 200). If
    unsucessful, returns an empty array; if sucessful, returns the JSONified
    result of the requests.get() query."""
    try:
        raw_data = requests.get(url, auth=(UKEY, TOKE),
                                timeout=TIMEOUT, verify=VERIFY)
        if not raw_data.status_code == SUCCESS_CODE:
            print('WARNING: Request failed w/ error %i' % raw_data.status_code)
            printV('   Error message resonse:\n      %s' % raw_data.json())
            return []
        return raw_data.json()

    except Exception as err:
        print('Exception: %s' % str(err))
        return []


# == Define GetSites Helper Function ==========================================
def getSites():
    """getSites(): Returns a list of OOI site filtered to contain only Coastal
    Endurance and RSN site IDs."""
    # Request Site List from M2M
    res = getData(U)

    # Filter Sites to CE and RSN Only
    return [site for site in res if 'CE0' in site or 'RS0' in site]


# == Define getInstruments Helper Function ====================================
def getInstruments(site, node):
    """getInstruments(site, node): Returns a list of instruments for a given site-
    node pair, filtered for either sci or eng instruments based on the global
    ENG_ONLY flag. Requires global varoab;es U, UKEY, TOKE, TIMEOUT, VERIFY
    to be set."""
    # Request Data from M2M
    res = getData(U + site + '/' + node)

    # Filter Instrument List Based on Global ENG_ONLY Flag
    if ENG_ONLY:
        return [inst for inst in res if 'ENG' in inst or 'IP' in inst]
    else:
        return [inst for inst in res if 'ENG' not in inst
                and 'IP' not in inst
                and 'EP1' not in inst
                and 'OBS' not in inst
                and 'HYD' not in inst]


# == Define getStreams Helper Function ========================================
def getStreams(site, node, inst):
    """Gets a list of streams for a given site-node-inst combo."""
    # Print message if VERB, then request data
    printV('    Getting streams for %s' % inst)
    if node[0:1] == 'DP':
        method = '/telemetered'   # Change this to the right things!
    else:
        method = '/streamed'
    res = getData(U + site + '/' + node + '/' + inst + method)

    if not res:
        return []

    return res
# =============================================================================
# == END FUNCTION DEFINITIONS =================================================
# =============================================================================


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
        instIDs = getInstruments(siteID, nodeID)

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
