from os.path import isfile

def writeNavHeader(fname,title_str):
    f = open(fname, 'w+')
    f.write('<!-- PAGE CREATED BY OOI_WEB.PY -->\n')
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('\t<meta http-equiv="refresh" content="3600" />\n')
    f.write('\t<title>Links</title>\n</head>\n\n')
    f.write('<ul>\n')
    f.write('\t<script src="../topNavLinks.js"></script>\n')
    f.write('\t<b>%s</b>\n\n' % title_str)
    f.close()

def writePlotSummary(fname):
    # If file doesn't exist, create it and write header
    if isfile(fname):
        f = open(fname, 'a')
    else:
        writeHeader(fname)

    # Setup Node URL and Window Lit
    url_base = 'index.php?view=main&window='
    t_list = ['day', 'week', 'month', 'year']

    # Begin List and Write Node Link
    f.write('\t<br><br>\n')
    f.write('\t<li>\n')
    f.write('\t\t<a href="%sday" target="content">Summary</a>\n' % (url_base))

    # Write (d), (m), etc Links
    for twin in t_list:
        url = url_base + twin
        f.write('\t\t<a href="%s" target="content">(%s)</a>\n' % (url, twin[0]))
    f.write('\t</li>\n\n')
    f.write('\t<br>\n')

    # Close File
    f.close()


def writeEngNavNodeLI(fname, node):
    # If file doesn't exist, create it and write header
    if isfile(fname):
        f = open(fname, 'a')
    else:
        writeHeader(fname)
    
    # Setup Node URL and Window Lit
    url_base = 'plotDisplay.php?node=' + node + '&window='
    t_list = ['day', 'week', 'month', 'year']

    # Begin List and Write Node Link
    f.write('\t<li>\n')
    f.write('\t\t<a href="%sday" target="content">%s</a>\n' % (url_base, node))

    # Write (d), (m), etc Links
    for twin in t_list:
        url = url_base + twin
        f.write('\t\t<a href="%s" target="content">(%s)</a>\n' % (url, twin[0]))
    f.write('\t</li>\n\n')

    # Close File
    f.close()


def writePlotNodeLI(fname, node):
    # If file doesn't exist, create it and write header
    if isfile(fname):
        f = open(fname, 'a')
    else:
        writeHeader(fname)

    # Start the new UL and print node name
    f.write('\t<li>%s\n' % node)
    f.write('\t\t<ul>\n')
    
    # Close file
    f.close()


def writePlotNodeEnd(fname):
    # Open File
    f = open(fname, 'a')
    f.write('\t\t</ul>\n')
    f.write('\t</li>\n')
    f.close()


def writePlotNavInstLI(fname, node, inst):
    # Open file for writing
    f = open(fname, 'a')

    # Massage Inst Variable (remove port number)
    inst = inst.split('-')[1]

    # Setup Node URL and Window List
    url_base = 'index.php?inst=' + inst + '&labels=no&org=2&size=450'
    url_base += '&warn=no&window='
    t_list = ['day', 'week', 'month', 'year']

    # Begin List and Write Node Link
    f.write('\t\t\t<li>\n')
    f.write('\t\t\t\t<a href="%sday" target="content">%s</a>\n' % (url_base, inst))

    # Write (d), (m), etc Links
    for twin in t_list:
        url = url_base + twin
        f.write('\t\t\t\t<a href="%s" target="content">(%s)</a>\n' % (url, twin[0]))
    f.write('\t\t\t</li>\n\n')

    # Close File
    f.close()
    

def writeNavFooter(fname):
    if isfile(fname):
        f = open(fname, 'a')
        f.write('</ul>\n\n</html>\n')
        f.close()
    else:
        raise Exception('HTML File Not Found!')
