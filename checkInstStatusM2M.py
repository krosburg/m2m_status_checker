import requests
from ooicreds import UKEY, TOKE
import datetime as dt

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

# Color Time Cutoffs (hours)
YEL_CUTOFF = 12
GRN_CUTOFF = 1

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


# == Define printSites Helper Function ========================================
def printSites(siteIDs, results):
    """printSites(siteIDs, results): Takes a filtered JSON list of OOI Site IDs &
    the raw result of the requests.get().json() query that got the list. Prints
    the number of filtered and raw results, then prints the site list on a new
    line. Note: Results are only printed if global VERB=True."""
    printV('Of %i sites, found %i matching CE or RSN:\n  %s\n'
           % (len(results), len(siteIDs), siteIDs))


# == Define printNodes Helper Function ========================================
def printNodes(nodeIDs, results):
    """printNodes(nodeIDs, results): Takes a filtered JSON list of OOI Node IDs &
    the raw result of the requests.get().json() query that got the list. Prints
    the number of filtered and raw results, then prints the node list on a new
    line. Note: Results are only printed if global VERB=True."""
    printV('  Of %i nodes, found %i of interest:\n    %s\n'
           % (len(results), len(nodeIDs), nodeIDs))


# == Define printInsts Helper Function ========================================
def printInstruments(instIDs, results, node):
    """printInstruments(instIDs, results, node): Takes a filtered JSON list of OOI
    instrument ID, the raw result of the requests.get().json() query that got
    the list, and the node in question. Prints the number of filtered & raw
    results, then prints the inst list on a new line. Note: Results are only
    printed if global VERB=True."""
    if ENG_ONLY:
        inst_type = 'eng'
    else:
        inst_type = 'sci'
    printV('    Found %i %s inst (of %i total) for %s:\n      %s\n'
           % (len(instIDs), inst_type, len(results), instIDs, node))


# == Define isScienceStream Helper Function ===================================
def isScienceStream(stream_name):
    """isScienceSteam(stream_name) Returns TRUE if STREAM_NAME (string) is a
    Science stream. Note gloabls PRELOAD_URL, UKEY, and TOKE must be set."""
    stream_type = getData(PRELOAD_URL + stream_name)
    return stream_type['stream_type']['value'] == 'Science'


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


# == Define getSciStreams Helper Function =====================================
def getSciStreams(site, node, inst):
    """getSciStreams(site, node, inst): Get List of Science-Only streams for
    a given reference designator site, node, inst combo."""
    # Print message if VERB, then request data
    printV('    Getting streams for %s' % inst)
    res = getData(U + site + '/' + node + '/' + inst + '/streamed')

    # Skip If Empty
    if not res:
        return

    # Filter Out Non-Science Streams With Manual Exclusions
    printV('      Pre-Filtering %s-%s-%s streams to sci only'
           % (site, node, inst))
    streams = [stream for stream in res if 'config' not in stream
               and 'eng' not in stream
               and 'status' not in stream
               and 'parse' not in stream
               and 'cal' not in stream
               and 'hardware' not in stream
               and 'header' not in stream
               and 'system' not in stream
               and 'dev' not in stream
               and 'message' not in stream]

    # Skip If Empty
    if not res:
        return

    # Filter Out Non-Science Streams by Checking STREAM_TYPE Attribute
    if len(streams) > 1:
        printV('      Filtering %s-%s-%s streams to sci only'
               % (site, node, inst))
        streams = [s for s in streams if isScienceStream(s)]

    # Give Back Results
    return streams


# == Define lastSampleTime() Helper Function ==================================
def lastSampleTime(site, node, inst, stream):
    """lastSampleTime(site, node, isnt, stream): Returns a string continaing the
    UTC data & time of last M2M sample for the given site-node-inst-stream."""

    # Request timem metadata for the instrument
    res = getData(U + site + '/' + node + '/' + inst + '/metadata/times')

    # Filter return based on the given stream name
    t_end = [time['endTime'] for time in res if time['stream'] == stream][0]

    # Convert to Datetime
    return dt.datetime.strptime(t_end, '%Y-%m-%dT%H:%M:%S.%fZ')


# == Define timeDiff() Helper Function ========================================
def checkTimeDiff(t_end):
    """checkTimeDiff(t_end): Given a last samp time, t_end [datetime], calcualtes
    the time difference [timedelta] between now & the last sample in hours. If
    the difference is greater than YEL_CUTOFF, returns the time diff & the flag
    `red`, if less than red cutoff & greater than green cutoff the time diff &
    `yellow` flag are returned, if below the green cuttoff, `green` is returned
    with the time_diff. Cuttoffs are global YEL_CUTOFF,GRN_CUTOFF variables."""
    # Calcualte the time difference
    time_diff = (dt.datetime.utcnow() - t_end).total_seconds()/3600.0

    if time_diff > YEL_CUTOFF:
        tcolor = 'red'
    elif time_diff > GRN_CUTOFF:
        tcolor = 'yellow'
    else:
        tcolor = 'green'

    return time_diff, tcolor
# =============================================================================
# == END FUNCTION DEFINITIONS =================================================
# =============================================================================


# Loop on Sites
for siteID in getSites():

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

        # Request Instruments at Given Node
        printV('  Getting instruments for %s' % nodeID)
        instIDs = getInstruments(siteID, nodeID)

        # Skip if No Instruments
        if not instIDs:
            continue

        # Loop on Instruments for the Given Node
        for instID in instIDs:
            # Get and Filter Streams for Instrument
            streams = getSciStreams(siteID, nodeID, instID)

            # Skip if no Streams
            if not streams:
                continue

            # Print Stream List
            printV('        Found: %s' % streams)

            # Get Final Sample Time
            t_end = lastSampleTime(siteID, nodeID, instID, streams[0])
            printV('          End Time: %s' % t_end)

            # Get/Set Color Flag
            t_diff, tclr = checkTimeDiff(t_end)

            printV('            %s (%2.1f hr)' % (tclr, t_diff))

    printV(' ')
