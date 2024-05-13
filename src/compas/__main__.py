# -*- coding: utf-8 -*-
import platform

try:
    import pkg_resources
except ImportError:
    pkg_resources = None

import compas

if __name__ == "__main__":
    # c = 'DCDHDCACDHDCAEDEACDHDCAEDEACDHDCAEDCDEACDHDCADCACDEADHDCAEDADEACDHDADADADHDCACDCAEDEACDCACDHDCAEDEACDCAEDEACDCAEDBACDHDAEDEACDADADCAEDBADHDAGDEACDADEADCAEDEADHDBADEDCAEDEACDEDAGDHDADCAEDACDCADADADHDAGDADEACAEDADBADHDAGDCADEAEDEACDBADHDAGDCAEDADEACDBADHDBADADADADAGDHDAGDCADEDADBADHDBADADAGDHDEADEAEDEAEDADHDEADEDADEDADHDEACDADCAEDHDACDADCADHDEACDADCAEDHDEACDADCAEDHDEACDADCAEDHDEAFCDADCAEDHDEAEDHDEDH'  # noqa: E501
    # r = 'fGfB]DSD]BYBHEIEHCXBUCFBYBFCUBSBEBOEOBEBSBQBEPBGBPBEQBOBDBRIRBDBOBNEUGUENBLBECRBCBCBCBRCEBLBKBDBBBDBNBCBEBCBNBDBBBDBKBKDBFCDBIDIDIBDCFBDKBJDBKCCCDDKBCDCCCKBDJBIBDPCBBCBMBCBBCPDBIBIERBCBBBCGCBCDREIBIDBQDEBDCDBEDQBDIBIDBOBDIBCBIBCBOBDIBIDBNBCBKCKBCBNBDIBIBDMDMCMDMDBIBJDBHBFNCNGHBDJBJBDGkGDBJBKBDFBGB[BGBFEKBLBDHCPCPCHELBMBDBWCWBDBMBOEBUCUBEOBPBEBSCSBEBPBRBEBQCQBEBRBUBECMCMCECTBXBFBDGCGDGCWB[DXC[BbObB'  # noqa: E501
    # maps = ' !-X_`|\n' if compas.IPY or compas.WINDOWS else ' ▌▀█▄`▐\n'

    # for n, o in zip(r, c):
    #     print((ord(n) - 65) * maps[ord(o) - 65], end='')

    print()
    print("Yay! COMPAS is installed correctly!")
    print()
    print("COMPAS: {}".format(compas.__version__))
    print("Python: {} ({})".format(platform.python_version(), platform.python_implementation()))

    if pkg_resources:
        working_set = pkg_resources.working_set
        packages = set([p.project_name for p in working_set]) - set(["COMPAS"])
        compas_pkgs = [p for p in packages if p.lower().startswith("compas")]

        if compas_pkgs:
            print("Extensions: {}".format([p for p in compas_pkgs]))
