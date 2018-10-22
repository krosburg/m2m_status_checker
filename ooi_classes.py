
class Stream:
    def __init__(self, name, method, stream_type, parSite, parNode, parInst):
        self.name = name
        self.method = method
        self.streamType = stream_type
        self.parentSite = parSite
        self.parentNode = parNode
        self.parentInst = parInst


class Inst:
    def __init__(self, name, instID, parSite, parNode):
        self.name = name
        self.id = instID
        self.parentSite = parSite
        self.parentNode = parNode
        self.streams = []

    def addStream(self, name, method, stream_type, parSite, parNode, parInst):
        self.streams.append(Stream(name,
                                   method,
                                   stream_type,
                                   parSite,
                                   parNode,
                                   parInst))


class Node:
    def __init__(self, name, nodeID, parSite):
        self.name = name
        self.id = nodeID
        self.parentSite = parSite
        self.instruments = []

    def addInst(self, instObj):
        self.instruments.append(instObj)


class Site:
    def __init__(self, name, siteID):
        self.name = name
        self.id = siteID
        self.nodes = []

    def addNode(self, nodeObj):
        self.nodes.append(nodeObj)


class Array:
    def __init__(self):
        self.sites = []

    def addSite(self, siteObj):
        self.sites.append(siteObj)

    def traversePrint(self):
        for site in self.sites:
            print(site.id)
            for node in site.nodes:
                print('  ' + node.id)
                for inst in node.instruments:
                    print('    ' + inst.id)
                    for stream in inst.streams:
                        print('      %s : %s' % (stream.name,
                                                 stream.streamType))
            print('')
