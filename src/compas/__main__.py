# -*- coding: utf-8 -*-
import platform

try:
    from importlib.metadata import distributions
except ImportError:
    distributions = None

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

    if distributions:
        names = {dist.metadata.get("Name") for dist in distributions()}
        compas_pkgs = [p for p in names if p and p.lower().startswith("compas") and p != "COMPAS"]

        if compas_pkgs:
            print("Extensions: {}".format(compas_pkgs))
