
class Stream:
    def __init__(self, name, method, stream_type, parSite, parNode, parInst):
        self.name = str(name)
        self.method = method
        self.streamType = stream_type
        self.parentSite = parSite
        self.parentNode = parNode
        self.parentInst = parInst

    def isScience(self):
        if self.streamType == 'Science':
            return True
        else:
            return False

    def isScienceData(self):
        if (self.isScience()
           and 'config' not in self.name
           and 'eng' not in self.name
           and 'status' not in self.name
           and 'parse' not in self.name
           and 'cal' not in self.name
           and 'hardware' not in self.name
           and 'header' not in self.name
           and 'system' not in self.name
           and 'dev' not in self.name
           and 'message' not in self.name
           and 'dark' not in self.name):
            return True
        else:
            return False


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

    def dropInst(self, inst):
        self.instruments.remove(inst)

    def filtIPOnly(self):
        for inst in self.instruments:
            if 'IP' not in inst.id:
                self.dropInst(inst)


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
