import os

# Only import if we are in the blender environment, this environment variable is set by the run.py script
if "INSIDE_OF_THE_INTERNAL_BLENDER_PYTHON_ENVIRONMENT" in os.environ:
    from .python.utility.SetupUtility import SetupUtility
    SetupUtility.setup([])
    from .api import loader
    from .api import utility
    from .api import sampler
    from .api import math
    from .python.utility.Initializer import init
    from .api import postprocessing
    from .api import writer
    from .api import material
    from .api import lighting
    from .api import camera
    from .api import renderer
    from .api import world
    from .api import constructor
    from .api import object
    from .api import types
    from .api import filter
