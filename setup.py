from distutils.core import setup
import py2exe, sys

sys.argv.append('py2exe')

setup(windows = [{'script': "main.py"}])