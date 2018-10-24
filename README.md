# OOI M2M Status Checker
Checks the science data status of all CE and RSN streamed instruments in the OOI Cabled Observatory.

## ooicreds.py (You Must Create Locally)
You will need to create your own ooicreds.py with the following variables:

<code>UKEY</code> Your OOI user login key

<code>TOKE</code> Your OOI login token

You can get these from http://ooinet.oceanobservatories.org.


## preloadInstruments.py
This script connects to the OOI M2M database, traverses the site-node-inst-stream tree, and generates a nested object structure to represent the science instruments in the Coastal Endurance and Cabled Array nodes. The structure is as folloes:
* Array
  * Site
    * Node
      * Instrument
        * Stream

Hence a stream name for a given instrument can be accessed like so (assuming your Array object is called rsn):
rsn.site[0].nodes[0].instruments[0].streams[0].name (see ooi_classes.py for more info).

The structure is saved as a Pickle file (<code>rsn_streams.pkl</code<) for later use. The idea here is that this script can preload and save the information to make later traversals and information retrieval much faster.


## preloadEngInsts.py
This file is much the same as <code>preloadInstruments.py</code>, except that it filters for engineering data only. The class structure and Pickle file (<code>rsn_eng_streams.pkl</code<) structure are the same.


## checkInstStatusM2M.py
This script loads the <code>rsn_streams.pkl</code>, itterates through to the stream level, requests last sample timestamps from M2M, and compares this to the current time to assign a status flag for a given instrument. This will be implemented into Blue in the future.


## ooi_classes.py
This module builds a class structure for OOI elements:


### Array:
This is the container or array (think CE, RSN, etc.) for a set of sites objects.


#### Attributes:
* <code>sites</code> (array of <code>ooi_classes.Site</code> objects)


#### Methods:
* <code>addSite(siteObj):</code> -- Adds a <code>Site</code> object to the <code>Array.sites[]</code> list.
* <code>traversePrint()</code> -- Traverses the <code>Array</code> object and prints out IDs to the stream level.

### Site:
Represents OOI sites. Contains site info and a list of attached nodes.


#### Attributes:
* <code>name</code> (string: name of the site)
* <code>id</code> (string: site ID portion of reference designator)
* <code>nodes</code> (array of <code>ooi_classes.Node</code> objects)


#### Methods:
* <code>addNode(nodeObj)</code> -- Adds a <code>Node</code> object to the <code>Site.nodes[]</code> list.

### Node:
Represents OOI nodes. Contains node info, parent site ID, and a list of attached instruments.

#### Attributes:
* <code>name</code> (string: name of the node).
* <code>id</code> (string: node ID portion of reference designator).
* <code>parentSite</code> (string: site ID of parent site).
* <code>instruments</code> (array of <code>ooi_classes.Inst</code> objects).


#### Methods:
* <code>addInst(instObj)</code> -- Adds an <code>Inst</code> object to the <code>Node.instruments[]</code> list.
* <code>dropInst(instObj)</code> -- Removes an <code>Inst</code> object from the <code>Node.instruments[]</code> list.
* <code>filtIPOnly()</code> -- Drops all non-Instrument_Port (IP) instruments from the <code>Node.instruments[]</code> list.


### Inst:
Represents OOI instruments. Contains instrument info, parent site and node IDs, and a list of associated streams.


#### Attributes:
* <code>name</code> (string: name of the instrument)
* <code>id</code> (string: instrument ID portion of reference designator)
* <code>parentSite</code> (string: site ID of parent site)
* <code>parentNode</code> (string: node ID of parent node)
* <code>streams</code> (array of <code>ooi_classes.Stream</code> objects)


#### Methods:
* <code>addStream(name, method, stream_type, parSite, parNode, parInst)</code> -- Given a stream name <code>name [string]</name>, <code>method [string]</code> (e.g. "streamed"), <code>stream_type [string]</code> (e.g. "Science"), parent site|node|instrument ID <code>par|Site|Node|Inst</code>, adds a <code>ooi_classes.Stream</code> object to the <code>Inst.streams[]</code> list.


### Stream:
Represents OOI streams. Contains stream info, parent site, node, and instrument IDs.

#### Attributes:
* <code>name</code> (string: Name of the M2M stream)
* <code>method</code> (string: Stream delivery method (e.g. "streamed", "telemetered", etc.)
* <code>steamType</code> (string: Stream content type (e.g. "Science", "Engineering", etc.)
* <code>parentSite</code> (string: site ID of parent site)
* <code>parentNode</code> (string: node ID of parent node)
* <code>parentInst</code> (string: instrument ID of parent instrument)

#### Methods:
* <code>isScience()</code> -- Returns true if the <code>stream_type</code> is "Science".
* <code>isScienceData()</code> -- Returns true if the stream contains scientific data parameters.
