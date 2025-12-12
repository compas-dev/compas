# type: ignore
import io
import os
import sys
import site
import subprocess
import importlib.util
import threading
import queue

# Ensure user site packages are in sys.path so we can find installed dependencies
# This is crucial because we install with --user
if site.USER_SITE not in sys.path:
    sys.path.append(site.USER_SITE)

# Check if dependencies are installed
try:
    import compas
except ImportError:
    compas = None

try:
    import bpy
except ImportError:
    bpy = None

try:
    import compas_blender.data
except ImportError:
    pass


__version__ = "2.15.0"


bl_info = {
    "name": "COMPAS",
    "author": "Tom Van Mele et al",
    "version": (2, 15, 0),
    "blender": (4, 2, 0),
    "location": "Console",
    "description": "The COMPAS framework for Blender",
    "warning": "",
    "doc_url": "https://compas.dev",
    "category": "Development",
}


INSTALLABLE_PACKAGES = ["compas", "compas_blender"]
SUPPORTED_VERSIONS = ["3.3", "3.6", "4.2"]
DEFAULT_VERSION = "4.2"

INSTALLATION_ARGUMENTS = None


__all__ = [
    "INSTALLABLE_PACKAGES",
    "SUPPORTED_VERSIONS",
    "DEFAULT_VERSION",
    "clear",
    "redraw",
]

__all_plugins__ = [
    "compas_blender.geometry.booleans",
    "compas_blender.install",
    "compas_blender.scene",
]

# =============================================================================
# =============================================================================
# =============================================================================
# General helpers
# =============================================================================
# =============================================================================
# =============================================================================


def clear(guids=None):
    """Clear all scene objects."""
    if guids is None:
        # delete all objects
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=True, confirm=False)
        # delete data
        compas_blender.data.delete_unused_data()
        # delete collections
        for collection in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.unlink(collection)
        for block in bpy.data.collections:
            objects = [o for o in block.objects if o.users]
            while objects:
                bpy.data.objects.remove(objects.pop())
            for collection in block.children:
                block.children.unlink(collection)
            if block.users == 0:
                bpy.data.collections.remove(block)
    else:
        for obj in guids:
            bpy.data.objects.remove(obj, do_unlink=True)


def redraw():
    """Trigger a redraw."""
    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)


def _check_blender_version(version):
    supported_versions = SUPPORTED_VERSIONS

    if not version:
        return DEFAULT_VERSION

    if version not in supported_versions:
        raise Exception("Unsupported Blender version: {}".format(version))

    return version


def _get_package_path(package):
    return os.path.abspath(os.path.dirname(package.__file__))


# =============================================================================
# =============================================================================
# =============================================================================
# Bootstrapper
# =============================================================================
# =============================================================================
# =============================================================================


def _get_bootstrapper_path(install_path):
    return os.path.join(install_path, "compas_bootstrapper.py")


def _get_bootstrapper_data(compas_bootstrapper):
    data = {}

    if not os.path.exists(compas_bootstrapper):
        return data

    content = io.open(compas_bootstrapper, encoding="utf8").read()
    exec(content, data)

    return data


def _try_remove_bootstrapper(path):
    """Try to remove bootstrapper.

    Returns
    -------
    bool: True if the operation did not cause errors, False otherwise.
    """

    bootstrapper = _get_bootstrapper_path(path)

    if os.path.exists(bootstrapper):
        try:
            os.remove(bootstrapper)
            return True
        except:  # noqa: E722
            return False
    return True


# =============================================================================
# =============================================================================
# =============================================================================
# Blender executable
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_blender_executable_path(version):
    version = _check_blender_version(version)

    if compas.OSX:
        path = _get_default_blender_executable_path_mac(version)
    elif compas.WINDOWS:
        path = _get_default_blender_executable_path_windows(version)
    elif compas.LINUX:
        path = _get_default_blender_executable_path_linux(version)
    else:
        raise Exception("Unsupported platform.")

    if not os.path.exists(path):
        raise Exception("The default installation folder for Blender doesn't exist.")

    return path


def _get_default_blender_executable_path_mac(version):
    return "/Applications/Blender.app/Contents/MacOS/Blender"


def _get_default_blender_executable_path_windows(version):
    return "C:\\Program Files\\Blender Foundation\\Blender {}".format(version)


def _get_default_blender_executable_path_linux(version):
    raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# Blender Python
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_blender_python_path(version):
    version = _check_blender_version(version)

    if compas.OSX:
        path = _get_default_blender_python_path_mac(version)
    elif compas.WINDOWS:
        path = _get_default_blender_python_path_windows(version)
    elif compas.LINUX:
        path = _get_default_blender_python_path_linux(version)
    else:
        raise Exception("Unsupported platform.")

    if not os.path.exists(path):
        raise Exception("The default installation folder for Blender {} doesn't exist.".format(version))

    return path


def _get_default_blender_python_path_mac(version):
    if version == "4.2":
        return "/Applications/Blender.app/Contents/Resources/{}/python/bin/python3.11".format(version)
    return "/Applications/Blender.app/Contents/Resources/{}/python/bin/python3.10".format(version)


def _get_default_blender_python_path_windows(version):
    return "C:\\Program Files\\Blender Foundation\\Blender {}\\{}\\python\\bin\\python.exe".format(version, version)


def _get_default_blender_python_path_linux(version):
    raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# Blender Python site-packages
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_blender_sitepackages_path(version):
    version = _check_blender_version(version)

    if compas.OSX:
        path = _get_default_blender_sitepackages_path_mac(version)
    elif compas.WINDOWS:
        path = _get_default_blender_sitepackages_path_windows(version)
    elif compas.LINUX:
        path = _get_default_blender_sitepackages_path_linux(version)
    else:
        raise Exception("Unsupported platform.")

    if not os.path.exists(path):
        raise Exception("The default installation folder for Blender {} doesn't exist.".format(version))

    return path


def _get_default_blender_sitepackages_path_mac(version):
    return "/Applications/Blender.app/Contents/Resources/{}/python/lib/python3.10/site-packages".format(version)


def _get_default_blender_sitepackages_path_windows(version):
    return "C:\\Program Files\\Blender Foundation\\Blender {}\\{}\\python\\lib\\site-packages".format(version, version)


def _get_default_blender_sitepackages_path_linux(version):
    raise NotImplementedError


def _get_python_exe():
    # Determine python executable
    python_exe = sys.executable
    
    # If sys.executable is Blender, we need to find the python binary
    if os.path.basename(sys.executable).lower().startswith("blender"):
        if sys.platform == "darwin":
            # macOS: Resources/X.X/python/bin/python3.X
            # sys.prefix usually points to Resources/X.X/python
            python_dir = os.path.join(sys.prefix, "bin")
            # Find the python executable
            found = False
            if os.path.exists(python_dir):
                for name in os.listdir(python_dir):
                    if name.startswith("python3") and not name.endswith("config"):
                        python_exe = os.path.join(python_dir, name)
                        found = True
                        break
            if not found:
                print("COMPAS: Could not locate python executable in {}".format(python_dir))
        elif sys.platform == "win32":
            # Windows: python/bin/python.exe
            python_exe = os.path.join(sys.prefix, "bin", "python.exe")
            if not os.path.exists(python_exe):
                 python_exe = os.path.join(sys.prefix, "python.exe")
    return python_exe


def _run_command(cmd, env=None, log_func=None):
    try:
        # Create a startupinfo object to hide the console window on Windows
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
        # Prepare environment
        process_env = os.environ.copy()
        if env:
            process_env.update(env)

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            startupinfo=startupinfo,
            env=process_env,
            bufsize=1,
            universal_newlines=True
        )
        
        output_lines = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                line = line.rstrip()
                output_lines.append(line)
                if log_func:
                    log_func(line)
        
        stdout = "\n".join(output_lines)
        
        if process.returncode != 0:
            return False, stdout
        return True, stdout
    except Exception as e:
        return False, str(e)


def _log_to_text_block(message):
    log_name = "COMPAS_INSTALL_LOG"
    if log_name not in bpy.data.texts:
        bpy.data.texts.new(log_name)
    log = bpy.data.texts[log_name]
    log.write(message + "\n")
    # Try to switch an area to text editor to show log? No, that's too intrusive.


def _install_dependencies(log_func=None, progress_func=None):
    if log_func is None:
        log_func = _log_to_text_block
    
    def update_progress(val):
        if progress_func:
            progress_func(val)

    update_progress(0)
    print("COMPAS: Installing dependencies...")
    log_func("--- Starting Installation ---")
    
    python_exe = _get_python_exe()
    log_func("Using python executable: {}".format(python_exe))
    
    # We install to the user site packages to avoid permission issues (especially on Windows)
    # and to avoid modifying the Blender installation itself.
    log_func("Installing to user site packages (requires no admin rights).")
    
    wheels_dir = os.path.join(os.path.dirname(__file__), "wheels")
    
    # Ensure pip is installed
    update_progress(10)
    log_func("Checking for pip...")
    # Check if pip is already available
    pip_check, _ = _run_command([python_exe, "-m", "pip", "--version"])
    
    if not pip_check:
        log_func("pip not found. Attempting to install pip via ensurepip...")
        # Try ensurepip. We try with --user to avoid permission errors if possible.
        success, output = _run_command([python_exe, "-m", "ensurepip", "--upgrade", "--user"], log_func=log_func)
        if not success:
             # Fallback: try without --user (maybe we are admin?)
             log_func("ensurepip --user failed. Trying default ensurepip...")
             success, output = _run_command([python_exe, "-m", "ensurepip", "--upgrade"], log_func=log_func)
             if not success:
                return False, "Failed to install pip. See COMPAS_INSTALL_LOG for details."
    else:
        log_func("pip is already installed.")

    update_progress(30)

    # Install wheels
    if os.path.exists(wheels_dir):
        # Find the compas wheel
        compas_wheels = [f for f in os.listdir(wheels_dir) if f.startswith("compas-") and f.endswith(".whl")]
        if not compas_wheels:
             return False, "Could not find compas wheel in {}".format(wheels_dir)
        
        compas_wheel_path = os.path.join(wheels_dir, compas_wheels[0])
        log_func("Installing compas from {}".format(compas_wheel_path))
        
        # Install with --user
        # We use --upgrade to ensure we get the latest compatible dependencies.
        # We do NOT use --force-reinstall to avoid forcing a reinstall of numpy if it's in system.
        success, output = _run_command([
            python_exe, "-m", "pip", "install", 
            compas_wheel_path,
            "--upgrade",
            "--user"
        ], log_func=log_func)
        if not success:
            return False, "Failed to install compas. See COMPAS_INSTALL_LOG for details."
    
    update_progress(100)
    log_func("Dependencies installed successfully.")
    
    # Ensure user site is in sys.path immediately
    if site.USER_SITE not in sys.path:
        sys.path.append(site.USER_SITE)
        
    return True, "Success"


# Global queue for thread communication
install_queue = queue.Queue()

def _log_to_queue(message):
    install_queue.put(("LOG", message))

def _progress_to_queue(value):
    install_queue.put(("PROGRESS", value))

def _install_thread_target():
    try:
        success, msg = _install_dependencies(log_func=_log_to_queue, progress_func=_progress_to_queue)
        install_queue.put(("RESULT", (success, msg)))
    except Exception as e:
        install_queue.put(("RESULT", (False, str(e))))

if bpy is not None:
    class COMPAS_OT_install_dependencies(bpy.types.Operator):
        bl_idname = "compas.install_dependencies"
        bl_label = "Install Dependencies"
        bl_description = "Install COMPAS and required dependencies (scipy, etc.)"

        _timer = None
        _thread = None

        def modal(self, context, event):
            if event.type == 'TIMER':
                while not install_queue.empty():
                    try:
                        msg_type, data = install_queue.get_nowait()
                    except queue.Empty:
                        break

                    if msg_type == "LOG":
                        _log_to_text_block(data)
                        context.workspace.status_text_set(data)
                    elif msg_type == "RESULT":
                        success, msg = data
                        
                        # Clear status text
                        context.workspace.status_text_set(None)
                        
                        if success:
                            self.report({'INFO'}, "COMPAS dependencies installed. Please restart Blender.")
                            # Invalidate import caches so find_spec works immediately
                            importlib.invalidate_caches()
                        else:
                            self.report({'ERROR'}, msg)
                            self.report({'WARNING'}, "Check the 'COMPAS_INSTALL_LOG' in the Text Editor for details.")
                        
                        context.window_manager.event_timer_remove(self._timer)
                        
                        # Force redraw of the preferences area if possible
                        if context.area:
                            context.area.tag_redraw()
                            
                        return {'FINISHED'}
            
            return {'PASS_THROUGH'}

        def execute(self, context):
            self.report({'INFO'}, "Installation started. Check COMPAS_INSTALL_LOG for progress...")
            
            # Start thread
            self._thread = threading.Thread(target=_install_thread_target)
            self._thread.start()
            
            self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}

    class COMPAS_PT_preferences(bpy.types.AddonPreferences):
        bl_idname = __package__

        def draw(self, context):
            layout = self.layout

            compas_spec = importlib.util.find_spec("compas")

            if compas_spec:
                if compas:
                    layout.label(text="COMPAS {} is installed.".format(compas.__version__), icon='CHECKMARK')
                else:
                    layout.label(text="COMPAS is installed (Restart Blender to load).", icon='CHECKMARK')
                layout.operator("compas.install_dependencies", text="Reinstall / Update Dependencies")
            else:
                layout.label(text="COMPAS is NOT installed.", icon='ERROR')
                layout.operator("compas.install_dependencies", text="Install Dependencies")

            if importlib.util.find_spec("scipy"):
                layout.label(text="Dependencies are installed.", icon='CHECKMARK')
            else:
                layout.label(text="Dependencies are NOT installed.", icon='ERROR')


    def register():
        if "bpy" in sys.modules:
            print("COMPAS: Registering classes...")
            try:
                bpy.utils.register_class(COMPAS_OT_install_dependencies)
                bpy.utils.register_class(COMPAS_PT_preferences)
                print("COMPAS: Classes registered.")
            except Exception as e:
                print("COMPAS: Failed to register classes: {}".format(e))
                import traceback
                traceback.print_exc()
            
            # Auto-install is disabled to prevent UI blocking/crashing.
            # User should use the button in Preferences.
            if compas is None or importlib.util.find_spec("scipy") is None:
                print("COMPAS: Dependencies missing. Please use the 'Install Dependencies' button in the COMPAS preferences.")


    def unregister():
        if "bpy" in sys.modules:
            bpy.utils.unregister_class(COMPAS_OT_install_dependencies)
            bpy.utils.unregister_class(COMPAS_PT_preferences)
