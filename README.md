# PythonInjector
A simple python GUI Injector source, it is in 3.5 so it can be compiled into a .exe with ease using the most common tools.

You don't need to modify it for it to work, just select a DLL, select a process, and inject.

I know of 2 issues I don't care to fix at the moment.  If your process opens after you open the injector, there isn't a refresh method, although it could really easily be added.
An error #22 has come up, but that is most likely due to an outdated .dll was being injected during the process, although it still worked.

Py2exe doesn't work with this build, so I have used PyInstaller which works perfectly with this build.
