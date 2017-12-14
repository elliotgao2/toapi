### Manual Installation

In order to manually install Toapi you'll need [Python] installed on your
system, as well as the Python package manager, [pip]. You can check if you have
these already installed from the command line:

```text
$ python --version
Python 3.5.2
$ pip --version
pip 9.0.1
```

Toapi supports Python3.5+.

#### Installing Python

Install [Python] by downloading an installer appropriate for your system from
[python.org] and running it.

!!! Note

    If you are installing Python on Windows, be sure to check the box to have
    Python added to your PATH if the installer offers such an option (it's
    normally off by default).

[python.org]: https://www.python.org/downloads/

#### Installing pip

If you're using a recent version of Python, the Python package manager, [pip],
is most likely installed by default. However, you may need to upgrade pip to the
lasted version:

```text
pip install --upgrade pip
```

If you need to install [pip] for the first time, download [get-pip.py].
Then run the following command to install it:

```text
python get-pip.py
```

#### Installing Toapi

Install the `toapi` package using pip:

```text
pip install toapi
```

You should now have the `toapi` command installed on your system. Run `toapi
--version` to check that everything worked okay.

```text
$ toapi --version
toapi, version 1.0.0
```

!!! Note
    If you are using Windows, some of the above commands may not work
    out-of-the-box.

    A quick solution may be to preface every Python command with `python -m`
    like this:

        python -m pip install toapi
        python -m api

    For a more permanent solution, you may need to edit your `PATH` environment
    variable to include the `Scripts` directory of your Python installation.
    Recent versions of Python include a script to do this for you. Navigate to
    your Python installation directory (for example `C:\Python34\`), open the
    `Tools`, then `Scripts` folder, and run the `win_add2path.py` file by double
    clicking on it. Alternatively, you can [download][a2p] the script and run it
    (`python win_add2path.py`).

[a2p]: https://svn.python.org/projects/python/trunk/Tools/scripts/win_add2path.py

---

[pip]: http://pip.readthedocs.io/en/stable/installing/
[Python]: https://www.python.org/
