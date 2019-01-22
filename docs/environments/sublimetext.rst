********************************************************************************
Working in Sublime Text
********************************************************************************

* `Sublime Text Official Documentation <https://www.sublimetext.com/docs/3/>`_
* `Sublime Text Unofficial Documentation <http://docs.sublimetext.info/en/latest/index.html>`_


Install Packages
================

* Conda
* EditorConfig
* GitGutter
* LateXTools
* MarkdownPreview
* One Dark Color Scheme
* requirementstxt
* SideBarEnhancements
* SublimeLinter
* SublimeLinter-flake8
* Terminal

Settings
========

.. code-block:: json

    // Packages/User/Preferences.sublime-settings

    {
        "color_scheme": "Packages/One Dark Color Scheme/One Dark.tmTheme",
        "file_exclude_patterns":
        [
            "*.pyc",
            "*.pyo",
            "*.exe",
            "*.dll",
            "*.o",
            "*.a",
            "*.lib",
            "*.so",
            "*.dylib",
            "*.ncb",
            "*.sdf",
            "*.suo",
            "*.pdb",
            "*.idb",
            ".DS_Store",
            "*.class",
            "*.psd",
            "*.db",
            "*.sublime-workspace",
            "*.3dmbak",
            "*.rhl",
            "*.rui_bak"
        ],
        "rulers":
        [
            80
        ],
        "theme": "Adaptive.sublime-theme",
        "translate_tabs_to_spaces": true,
        "word_wrap": false
    }

.. code-block:: json

    // Packages/User/SublimeLinter.sublime-settings

    {
        "styles" :
        [
            {
                "mark_style": "none"
            }
        ],

        "linters" :
        {
            "flake8" :
            {
                "args" : ["--ignore=E221,E203,E309,E741", "--max-line-length=120"]

            }
        }
    }

Snippets
========

Builders
========

.. code-block:: json

    // Packages/User/Anaconda3 Python.sublime-build

    {
        "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
        "selector": "source.python",
        "shell_cmd": "\"python3\" -u \"$file\""
    }

Projects
========


