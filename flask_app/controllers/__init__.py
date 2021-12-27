from os.path import dirname, basename, isfile, join
import inspect
import pdb

import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and f.endswith('_controller.py')]

from . import *

def to_camel_case(name):
    return ''.join(word.title() for word in name.split('_'))

controllers =[]
def start(sio):
    for module in __all__:
        class_name = to_camel_case(module)
        instruction = f"{module}.{class_name}(sio)"

        controller = eval(instruction)
        controllers.append(controller)

        # if module=='test_controller':pdb.set_trace()

