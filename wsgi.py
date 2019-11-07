
import sys
import os

path = '/home/gabiz/EN_VT_2019_US'
if path not in sys.path:
    sys.path.append(path)

from flask_receiver import app as application  # noqa
