import pytest
import sys
import simpleconfig
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")

class TestSimpleConfig1C1():
    #def setUp(self):
    #    pass

    def test_basics1(self):
        theargs = ["--opt1", "val1", '--comp1.opt2', 'val2']
        topconfig = simpleconfig.SimpleConfig(component='')
        topconfig.add_argument("--opt1", type=str, default="optdefault")
        topconfig.parse_args(theargs)
        comp1config = simpleconfig.SimpleConfig(component='comp1')
        topconfig.add_config(comp1config)
        comp1config.add_argument("--opt2")
        comp1config.parse_args(theargs)
        valopt1 = topconfig.get('opt1')
        assert valopt1 == 'val1'
        valopt2 = comp1config.get('opt2')
        assert valopt2 == 'val2'
        valopt2a = topconfig.get('comp1.opt2')
        assert valopt2a == 'val2'

    def NOTATEST_basics1a(self):
        theargs = ['--foo', "333", "--comp1.help"]
        topconfig = simpleconfig.SimpleConfig()
        topconfig.parse_args(theargs)
        comp1config = simpleconfig.SimpleConfig(component='comp1')
        topconfig.add_config(comp1config)
        comp1config.add_argument("--bar")
        comp1config.parse_args(theargs)
        # logger.debug('ns={}'.format(topconfig.namespace))

    def test_basics2(self):
        cfgile1 = './tests/cfgfile1.yaml'
        theargs = ['--config_file', cfgile1]
        topconfig = simpleconfig.SimpleConfig()
        topconfig.add_argument("--key1", default="defaultforkey1")
        topconfig.parse_args(theargs)
        logger.debug('ns={}'.format(topconfig.namespace))

