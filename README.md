# OOI M2M Status Checker
Checks the science data status of all CE and RSN streamed instruments in the OOI Cabled Observatory.

## ooicreds
You will need to create your own ooicreds.py with the following variables:

<code>UKEY</code> Your OOI user login key

<code>TOKE</code> Your OOI login token

You can get these from http://ooinet.oceanobservatories.org.


## preloadInstruments.py
This script connects to the OOI M2M database, traverses the site-node-inst-stream tree, and generates a nested object structure to represent the science instruments in the Coastal Endurance and Cabled Array nodes. The structure is as folloes:
* Array
** Site
*** Node
**** Instrument
***** Stream

Hence a stream name for a given instrument can be accessed like so (assuming your Array object is called rsn):
rsn.site[0].nodes[0].instruments[0].streams[0].name (see ooi_classes.py for more info).

The structure is saved as a Pickle file (<code>rsn_streams.pkl</code<) for later use. The idea here is that this script can preload and save the information to make later traversals and information retrieval much faster.


## preloadEngInsts.py
This file is much the same as <code>preloadInstruments.py</code>, except that it filters for engineering data only. The class structure and Pickle file (<code>rsn_eng_streams.pkl</code<) structure are the same.


## checkInstStatusM2M.py
This script loads the <code>rsn_streams.pkl</code>, itterates through to the stream level, requests last sample timestamps from M2M, and compares this to the current time to assign a status flag for a given instrument. This will be implemented into Blue in the future.


## ooi_classes.py
This module builds a class structure for OOI elements:
#### Array:
This is the container for a set of sites objects.
##### Attributes:
<code>sites</code> (array of ooi_classes.Site objects)
##### Methods:
<code>addSite(siteObj):</code>

