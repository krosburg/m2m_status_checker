
import cPickle as pickle
import datetime as dt
from ooi_func import printV, lastSampleTime

# Define RSN Streams Object File
in_file = 'rsn_streams.pkl'


def checkTimeDiff(t_end):
    """Given a last samp time, t_end [datetime], calcualtes the time difference
    [timedelta] between now & the last sample in hours. If the difference is
    greater than YEL_CUTOFF, returns the time diff & the flag `red`, if less
    than red cutoff & greater than green cutoff the time diff & `yellow` flag
    are returned, if below the green cuttoff, `green` is returned with the
    time_diff. Cuttoffs are global YEL_CUTOFF,GRN_CUTOFF variables."""
    # Calcualte the time difference
    time_diff = (dt.datetime.utcnow() - t_end).total_seconds()/3600.0

    if time_diff > YEL_CUTOFF:
        tcolor = 'red'
    elif time_diff > GRN_CUTOFF:
        tcolor = 'yellow'
    else:
        tcolor = 'green'

    return time_diff, tcolor


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

            # Isolate Single Stream
            streams = streams[0]

            # Request the last sameple time & Check Difference
            t_end = lastSampleTime(site.id, node.id, inst.id, streams.name)
            t_diff, tcolor = checkTimeDiff(t_end)

            # Print Results
            printV('%s-%s-%s:' % (site.id, node.id, inst.id))
            printV('  %s - %s' % (streams.name, streams.streamType))
            printV('    %s\n      %s (%2.1f hr)' % (t_end, tcolor, t_diff))
