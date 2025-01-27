"""
Remote Procedure Call: to invoke Python functions outside of Rhino, in the context of the CPython interpreter.
"""

# r: compas==2.8.1
import Grasshopper

from compas.rpc import Proxy


class CompasRemoteProcedureCall(Grasshopper.Kernel.GH_ScriptInstance):
    def RunScript(self, module, function, parameters, path, restart):
        if not (module and function):
            return

        if restart:
            proxy = Proxy(max_conn_attempts=1)
            proxy.stop_server()

        proxy = Proxy(module, path=path)
        fn = getattr(proxy, function)
        parameters = parameters or []

        result = fn(*parameters)

        return result
