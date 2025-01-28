import os
import sys

__all__ = [
    "DevTools",
]


class DevTools(object):
    """Tools for working with Python code in development mode, unloading, and reloading code."""

    def __init__(self):
        """Initializes a new instance of the DevTools class."""
        self.watcher = None

    @staticmethod
    def unload_modules(top_level_module_name):
        """Unloads all modules named starting with the specified string.

        This function eases the development workflow when editing a library that is
        used from Rhino/Grasshopper.

        Parameters
        ----------
        top_level_module_name : :obj:`str`
            Name of the top-level module to unload.

        Returns
        -------
        list
            List of unloaded module names.
        """
        to_remove = [name for name in sys.modules if name.startswith(top_level_module_name)]

        for module in to_remove:
            sys.modules.pop(module)

        return to_remove

    @classmethod
    def enable_reloader(cls):
        """Enables the code reload on the current folder.

        The file must have been saved already in order for this to work."""
        cls._manage_reloader(enable=True)

    @classmethod
    def disable_reloader(cls):
        """Disables the code reload on the current folder.

        The file must have been saved already in order for this to work."""
        cls._manage_reloader(enable=False)

    @classmethod
    def _manage_reloader(cls, enable):
        import scriptcontext

        doc_id = scriptcontext.doc.Component.OnPingDocument().DocumentID.ToString()
        key = "__compas_devtools_{}__".format(doc_id)
        if key in scriptcontext.sticky:
            reloader = scriptcontext.sticky[key]
            reloader.stop_watcher()
            reloader = None
            del reloader

        if enable:
            reloader = DevTools()
            reloader.start_watcher()
            scriptcontext.sticky[key] = reloader

    @staticmethod
    def ensure_path():
        """Ensures the current folder is in the system path."""
        # Not sure why we need to import sys inside this method but GH complains otherwise
        import scriptcontext

        # First ensure the current folder is in the system path
        filepath = scriptcontext.doc.Component.OnPingDocument().FilePath

        if not filepath:
            raise Exception("It seems this file is not saved, cannot reload files without knowning where to search for them!")

        dirname = os.path.dirname(filepath)
        if dirname not in sys.path:
            sys.path.append(dirname)

        return dirname

    def start_watcher(self):
        try:
            from System.IO import FileSystemWatcher  # noqa : F401
            from System.IO import NotifyFilters  # noqa : F401
        except ImportError:
            raise Exception("This component requires the System.IO.FileSystemWatcher class to work")

        dirname = self.ensure_path()

        # Disable previous watchers if any
        if self.watcher:
            self.disable()

        # Setup file system watcher on python files
        self.watcher = FileSystemWatcher()
        self.watcher.Path = dirname
        self.watcher.NotifyFilter = NotifyFilters.LastWrite
        self.watcher.IncludeSubdirectories = False
        self.watcher.Filter = "*.py"
        self.watcher.Changed += self.on_changed
        self.watcher.EnableRaisingEvents = True

    def on_changed(self, sender, args):
        try:
            # Get module name from full path
            filename = os.path.basename(args.FullPath)
            if filename.lower().endswith(".py"):
                module_name = filename.split(".")[0]

                # Unload the modified module
                self.unload_modules(module_name)
        except Exception:
            print("Something failed during unload, this message will not be printed anywhere thou, deal with it")

    def stop_watcher(self):
        try:
            if self.watcher:
                self.watcher.Changed
                self.watcher.Dispose()
                del self.watcher
        except:  # noqa : E722
            pass
        self.watcher = None


unload_modules = DevTools.unload_modules
