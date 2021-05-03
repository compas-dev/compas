import json
import os
import compas


def compas_api():
    with open(compas_api_filename(), 'r') as f:
        return json.load(f)


def compas_api_filename():
    if compas.IPY:
        filename = 'compas_api_ipy.json'
    else:
        filename = 'compas_api.json'
    return os.path.join(os.path.dirname(__file__), filename)


def compas_stubs():
    HERE = os.path.dirname(__file__)
    STUBS = os.path.join(HERE, '../../docs/api/generated')
    _, _, filenames = next(os.walk(STUBS))
    stubs = {}
    for name in filenames:
        parts = name.split('.')
        if len(parts) != 4:
            continue
        package = parts[0]
        module = parts[1]
        item = parts[2]
        if package == 'compas':
            packmod = "{}.{}".format(package, module)
            if packmod not in stubs:
                stubs[packmod] = []
            stubs[packmod].append(item)
    return stubs


def check_compas_stubs(api, stubs):
    for packmod in api['modules']:
        parts = packmod.split('.')
        if len(parts) != 2:
            continue
        assert packmod in stubs
        for name in api['modules'][packmod]:
            if name not in stubs[packmod]:
                print(packmod, name)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    check_compas_stubs(compas_api(), compas_stubs())
