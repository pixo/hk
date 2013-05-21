import sys

__all__ = ['QtCore', 'QtGui', 'QtNetwork', 'QtOpenGL', 'QtSql', 'QtSvg', 'QtTest', 'QtWebKit', 'QtScript']

if sys.version_info[0] < 3:
    import private

__version__         = "1.0.9"
__version_info__    = (1, 0, 9, "final", 1)
