from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
from xml.etree import ElementTree as ET

import compas


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


def install(version='5.0'):
    compaspath = os.path.abspath(os.path.join(compas.HERE, '../'))
    appdata = os.getenv('APPDATA')
    filename = 'settings.xml'

    # temp = appdata.split(os.path.sep)
    # if 'Roaming' in temp:
    #     temp.remove('Roaming')
    #     appdata = os.path.join(temp[0], os.path.sep, *temp[1:])
    #     # if temp[0].endswith(':'):
    #     #     appdata = os.path.join(temp[0], os.path.sep, *temp[1:])
    #     # else:
    #     #     appdata = os.path.join(*temp)

    if version not in ('5.0', '6.0'):
        version = '5.0'

    if version == '6.0':
        filename = 'settings-Scheme__Default.xml'

    xmlpath = os.path.abspath(os.path.join(appdata,
                                           'McNeel',
                                           'Rhinoceros',
                                           '{}'.format(version),
                                           'Plug-ins',
                                           'IronPython (814d908a-e25c-493d-97e9-ee3861957f49)',
                                           'settings',
                                           filename))

    if not os.path.exists(xmlpath):
        raise Exception("The settings file does not exist in this location: {}".format(xmlpath))

    if not os.path.isfile(xmlpath):
        raise Exception("The settings file is not a file :)")
        
    if not os.access(xmlpath, os.W_OK):
        raise Exception("The settings file is not wrtieable.")
       
    tree = ET.parse(xmlpath)
    root = tree.getroot()

    entries = root.findall(".//entry[@key='SearchPaths']")

    try:
        searchpathsentry = entries[0]
    except IndexError:
        raise Exception("The settings file has no entry 'SearchPaths'.")

    searchpaths = searchpathsentry.text.split(';')
    searchpaths[:] = [os.path.abspath(path) for path in searchpaths]
        
    if compaspath not in searchpaths:
        searchpaths.append(compaspath)

    searchpathsentry.text = ";".join(searchpaths)
    tree.write(xmlpath)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import sys

    try:
        version = sys.argv[1]
    except IndexError:
        version = '5.0'
    else:
        try:
            version = str(version)
        except Exception:
            version = '5.0'

    install(version=version)
