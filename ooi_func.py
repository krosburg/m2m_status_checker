import requests
import datetime as dt
from time import sleep
from ooicreds import UKEY, TOKE
from ooi_globals import U, PRELOAD_URL, VERB, ENG_ONLY
"""Functions for the OOI package, to go with ooi_globals and ooi_classes."""

# == Define Important Variables ===============================================
# Disable Annoying HTTPS Warnings
requests.packages.urllib3.disable_warnings()

# Status, Verify, and Timeout Variables
SUCCESS_CODE = 200
VERIFY = False
TIMEOUT = 10

# =============================================================================
# == BEGIN FUNCTION DEFINITIONS ===============================================
# =============================================================================


# == Define printV Helper Function ============================================
def printV(msg):
    """Prints MSG if the global variable VERB=True."""
    if VERB:
        print(msg)


# == Define getStreamType Helper Function =====================================
def getStreamType(stream_name):
    """Returns type of stream (science, engineering, etc.)."""
    return getData(PRELOAD_URL + stream_name, 2)['stream_type']['value']


# == Define getData Helper Function ===========================================
def getData(url, pause=0):
    """getData(url): Given a full URL, contacts the M2M server using Python's
    request.get() routine, supplying credentials using global variables UKEY,
    TOKE & timeout & verification flags using globals TIMEOUT & VERIFY.
    Checks the result against global SUCCESS_CODE variable (usually 200). If
    unsucessful, returns an empty array; if sucessful, returns the JSONified
    result of the requests.get() query."""
    try:
        sleep(pause)
        raw_data = requests.get(url, auth=(UKEY, TOKE),
                                timeout=TIMEOUT, verify=VERIFY)
        if not raw_data.status_code == SUCCESS_CODE:
            print('WARNING: Request failed w/ error %i' % raw_data.status_code)
            printV('   Error message resonse:\n      %s' % raw_data.json())
            return []
        return raw_data.json()

    except Exception as err:
        print('Exception: %s' % str(err))
        quit()


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


# == Define lastSampleTime() Helper Function ==================================
def lastSampleTime(site, node, inst, stream):
    """Returns the UTC data & time of last M2M sample for the given
    site-node-inst-stream as a datetime element."""

    # Request timem metadata for the instrument
    res = getData(U + site + '/' + node + '/' + inst + '/metadata/times', 1)

    # Filter return based on the given stream name
    t_end = [time['endTime'] for time in res if time['stream'] == stream][0]

    # Convert to Datetime
    return dt.datetime.strptime(t_end, '%Y-%m-%dT%H:%M:%S.%fZ')
