from .configsimple import ConfigSimple
import argparse
__version__ = '0.3'


def flag(val):
    val = str(val)
    if val.lower() in ["yes", "true", "y", "t", "1"]:
        return True
    elif val.lower() in ["no", "false", "n", "f", "0"]:
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected, not %s" % (val,))


topconfig = ConfigSimple(component='')
