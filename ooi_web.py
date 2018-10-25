from os.path import isfile

def writeNavHeader(fname):
    f = open(fname, 'w+')
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('\t<meta http-equiv="refresh" content="3600" />\n')
    f.write('\t<title>Links</title>\n</head>\n\n')
    f.write('<ul>\n')
    f.close()


def writeNavNodeLI(fname, node):
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


def writeNavFooter(fname):
    if isfile(fname):
        f = open(fname, 'a')
        f.write('</ul>\n\n</html>\n')
        f.close()
    else:
        raise Exception('HTML File Not Found!')
