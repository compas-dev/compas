import os
import sys

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from compas.rpc import Dispatcher


class FileWatcherService(Dispatcher):
    def __init__(self):
        super(FileWatcherService, self).__init__()
        self.current_module = None
        self.current_observer = None

    def on_module_imported(self, module, newly_loaded_modules):
        module_spec = module.__spec__
        module_dir = os.path.dirname(module_spec.origin)

        # Stop existing observer, if any
        if self.current_module != module and self.current_observer:
            self.current_observer.stop()

        self.current_module = module
        reload_event_handler = ModuleReloader(newly_loaded_modules)

        print("Watching on {}".format(module_dir))
        self.current_observer = Observer()
        self.current_observer.schedule(reload_event_handler, module_dir, recursive=True)
        self.current_observer.start()


class ModuleReloader(PatternMatchingEventHandler):
    def __init__(self, module_names):
        super(ModuleReloader, self).__init__(ignore_patterns=["__pycache__"])
        self.module_names = module_names

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            # Unload modules so that they are reloaded on the next invocation
            for module in self.module_names:
                if module in sys.modules:
                    sys.modules.pop(module)
