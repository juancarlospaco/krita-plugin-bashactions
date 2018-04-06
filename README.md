# krita-plugin-bashactions

Plugin to execute Bash commands and programs as Actions on your current Images from Krita.

![screenshot](krita_plugin0.png)


![screenshot](krita_plugin1.png)


# Install

- Copy all files to `~/.local/share/krita/pykrita/` and restart Krita.
- Go to `Settings → Configure Krita → Python Plugin Manager → BashActions`, Enable it and restart Krita.
- Go to `Tools → Scripts → BashActions`.

**Uninstall:**

- Go to `Settings → Configure Krita → Python Plugin Manager → BashActions`, Disable it and restart Krita.
- Delete all files from `~/.local/share/krita/pykrita/bashactions/`.


# Requisites

- Python 3.6+.
- Qt 5+.
- Krita 4+.
- Linux or OsX.


# Description

<details>
    The GUI has on top your current opened image files on Krita with its full path,<br>
    then on Commands Template you can type or paste Bash commands to execute,<br>
    1 per line, you can repeat lines to repeat the operation,<br>
    the words "FILE1" in uppercase will be replaced with your first selected image file,<br>
    the words "FILE2" in uppercase will be replaced with your second selected image file,<br>
    the words "FILE3" in uppercase will be replaced with your third selected image file,<br>
    and so on, you can repeat those words, you can put as many as you want or none,<br>
    that way you can format commands quickly without having to type long complicated
    full paths of your current opened images on Krita,<br>
    it will automatically add Quotes if the filename or path contains white spaces,<br>
    to avoid errors on Bash commands, it can also repeat the whole commands again,<br>
    as many as you want or once, also you can set a wait Delay, with a Backoff multiplier,<br>
    and a Timeout on seconds, the commands run once with no wait by default,<br>
    the commands are automatically saved to cache txt on execution,<br>
    the commands can be Loaded from disk as bash or txt files,<br>
    you can run the commands on low smooth CPU priority if is too resource hog,<br>
    you can also Minimize the window during commands execution,<br>
    you can also Close the window after commands execution,<br>
    theres a Preview that shows you how the commands look like before execution,<br>
    theres a Log that shows you Standard Output, Standard Error,<br>
    some useful extra Info from the commands after execution.<br><br>
    It has a Mode selector with "Full" (advanced) and "Simple" (basic),<br>
    following the idea of <i>Simple but Powerful When Needed</i>.<br><br>
    Theres a Help button that opens the Plugins GitHub with Source, Docs, etc.
</details>
