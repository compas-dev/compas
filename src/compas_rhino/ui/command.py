from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino


__all__ = ['CommandMenu']


class CommandMenu(object):

    def __init__(self, menu):
        self.menu = menu

    def select_action(self):
        def select(message, options):
            if not options:
                return
            names = [option["name"] for option in options]
            name = compas_rhino.rs.GetString(message, names[0], names)
            if not name:
                return
            if name not in names:
                raise Exception("This option is not valid: {}".format(name))
            for option in options:
                if option["name"] == name:
                    break
            if "action" in option:
                return option.get("action")
            message = option["message"]
            options = option.get("options")
            return select(message, options)
        return select(self.menu["message"], self.menu["options"])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
