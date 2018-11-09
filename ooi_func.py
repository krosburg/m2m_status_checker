import requests, sys
import pandas as pd
import numpy as np
import datetime as dt
from time import sleep
from ooicreds import UKEY, TOKE
from ooi_globals import U, PRELOAD_URL, VERB, LIMIT
"""Functions for the OOI package, to go with ooi_globals and ooi_classes."""

# == Define Important Variables ===============================================
# Disable Annoying HTTPS Warnings
try:
    requests.packages.urllib3.disable_warnings()
except ModuleNotFoundError:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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


#== Define getArgs Helper Function ============================================
def getTimeWinArg():
    """Retrieves commandline argument for time-window for ploting"""
    if len(sys.argv) < 2:
        print('No time windows supplied, using day.')
        return 'day'
    else:
        t_win = str(sys.argv[1]).lower()
        if t_win not in ['day', 'week', 'month', 'year']:
            raise Exception('Invalid time window, using day')
            return 'day'
        return t_win


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
            if raw_data.status_code == 404:
                printV('WARN: M2M Returned no data (404).')
            else:
                printV('WARN: Request failed w/ error %i' % raw_data.status_code)
                printV('   Error message resonse:\n      %s' % raw_data.json())
            return []
        return raw_data.json()

    except Exception as err:
        print('Exception: %s' % str(err))
        #quit()
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
def getInstruments(site, node, ENG_ONLY):
    """getInstruments(site, node): Returns a list of instruments for a given site-
    node pair, filtered for either sci or eng instruments based on the ENG_ONLY
    flag. Requires global variables U, UKEY, TOKE, TIMEOUT, VERIFY to be
    set."""
    # Request Data from M2M
    res = getData(U + site + '/' + node)

    # Filter Instrument List Based on Global ENG_ONLY Flag
    if ENG_ONLY:
        return [inst for inst in res
                if 'ENG' in inst or 'IP' in inst or 'EP' in inst]
    else:
        return [inst for inst in res if 'ENG' not in inst
                and 'IP' not in inst
                and 'EP1' not in inst
                and 'OBS' not in inst
                and 'HYD' not in inst]


# == Define getInstruments Helper Function ====================================
def getOBSInstruments(site, node):
    """getInstruments(site, node): Returns a list of OBS SEIS instruments.
    Requires global variables U, UKEY, TOKE, TIMEOUT, VERIFY to be set."""
    # Request Data from M2M
    res = getData(U + site + '/' + node)

    # Filter Instrument List Based on OBS
    return [inst for inst in res if 'OBS' in inst]


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


# == Define getOffset Helper Function =========================================
def getOffset(time_window):
    # Case statement that returns the time offset given a time_window string.
    if time_window == 'day':
        return 1
    elif time_window == 'week':
        return 7
    elif time_window == 'month':
        return 30
    elif time_window == 'year':
        return 365
    else:
        raise Exception('Interval time not specified')


# == Define epoch2dt Helper Function ==========================================
def epoch2dt(t):
    # Setup Offsets
    offset = dt.datetime(1970, 1, 1, 0, 0, 0)-dt.datetime(1900, 1, 1, 0, 0, 0)
    off_sec = dt.timedelta.total_seconds(offset)

    # Convert using offsets
    t_datetime = []
    for tt in t:
        t_sec = tt - off_sec
        t_datetime.append(dt.datetime.utcfromtimestamp(t_sec))

    return t_datetime


# == Define startEndTimes(time_window) ========================================
def startEndTimes(time_window):
    t_end = dt.datetime.utcnow().isoformat() + 'Z'
    dt_end = dt.datetime.strptime(t_end, '%Y-%m-%dT%H:%M:%S.%fZ')
    dt_start = dt_end - dt.timedelta(days=getOffset(time_window))
    t_start = dt_start.isoformat() + 'Z'
    return t_start, t_end


# == Define getIPData Helper Function =========================================
def getIPData(inst_obj, time_window):
    # Parameter Names List
    params = ['sn_port_output_current', 'sn_port_unit_temperature',
              'sn_port_gfd_high', 'sn_port_gfd_low']
    # Get Start/End Times from time_window
    t_start, t_end = startEndTimes(time_window)

    # Fix Some Issues w/ LV Nodes
    if 'LV' in inst_obj.parentNode or len(inst_obj.streams) > 1:
        inst_obj.streams[0].name = 'secondary_node_port_eng_data'

    # Assemble URL
    url = U + inst_obj.parentSite + '/' + inst_obj.parentNode + '/'  \
            + inst_obj.id + '/streamed/' + inst_obj.streams[0].name  \
            + '?beginDT=' + t_start + '&endDT=' + t_end + '&limit='  \
            + LIMIT + '&parameters=PD7100,PD7102,PD7103,PD7104,PD7'  \
            + '&require_deployment=False'

    # Send Request
    raw_data = getData(url, 1)
    if not raw_data:
        return [], t_start, t_end
    data = pd.DataFrame.from_records(raw_data)

    # Assign Data
    inst_obj.ipData = []
    inst_obj.time = epoch2dt(data['time'])
    for pname in params:
        x = np.array(data[pname], dtype=np.float)
        x[x <= -9.9e5] = float('NaN')
        inst_obj.ipData.append(list(x))
    return inst_obj, t_start, t_end


# == Define getPDData Helper Function =========================================
def getPDData(inst_obj, time_window):
    # Parameter names List
    params = ['dp_dock_ambient_temperature',
              'dp_dock_heat_sink_temperature',
              'dp_dock_relative_humidity',
              'dp_dock_12_v_current']

    # Get Start/End Times from time_window
    t_start, t_end = startEndTimes(time_window)

    # Assemble URL
    url = U + inst_obj.parentSite + '/' + inst_obj.parentNode + '/'  \
            + inst_obj.id + '/streamed/' + inst_obj.streams[0].name  \
            + '?beginDT=' + t_start + '&endDT=' + t_end + '&limit='  \
            + LIMIT + '&parameters=PD7201,PD7202,PD7204,PD7200,PD7'  \
            + '&require_deployment=False'

    # Send Request
    raw_data = getData(url, 1)
    if not raw_data:
        return [], t_start, t_end
    data = pd.DataFrame.from_records(raw_data)

    # Assign Data
    inst_obj.data = []
    inst_obj.time = epoch2dt(data['time'])
    for pname in params:
        x = np.array(data[pname], dtype=np.float)
        x[x <= -9.9e5] = float('NaN')
        inst_obj.data.append(list(x))
    return inst_obj, t_start, t_end
