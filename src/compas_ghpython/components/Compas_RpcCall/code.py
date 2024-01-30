"""
Remote Procedure Call: to invoke Python functions outside of Rhino, in the context of the CPython interpreter.
"""

from ghpythonlib.componentbase import executingcomponent as component

from compas.rpc import Proxy


class CompasRpcCall(component):
    def RunScript(self, module, function, parameters, path, restart):
        if not (module and function):
            return

        if restart:
            proxy = Proxy(max_conn_attempts=1)
            proxy.stop_server()

        proxy = Proxy(module, path=path)
        fn = getattr(proxy, function)
        parameters = parameters or []

        try:
            result = fn(*parameters)
        except Exception:
            self.Message = "Error! Check details in stacktrace"
            raise

        self.Message = ""

        return result
