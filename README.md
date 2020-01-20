# configsimple

[![PyPi version](https://img.shields.io/pypi/v/configsimple.svg)](https://pypi.python.org/pypi/configsimple/)
[![Python compatibility](https://img.shields.io/pypi/pyversions/configsimple.svg)](https://pypi.python.org/pypi/configsimple/)



Configure a command and all the different components it uses via command line options, config files and environment variables.

One typical usage scenario: 
* you have some python program that takes arguments e.g. for which input and  output data to use
* depending on the input / output data format, the program may use different classes which require different parameters
* the program may perform different kinds of processing on the data and choose one of several classes for this.
  Each class again may require different configuration settings

With `configsimple` each of the configurable classes can define their own ConfigSimple object (which works much 
like ArgumentParser). The main program can then automatically process all the options for the different classes
and also show help information for them to the user. In addition, all the parameters for any of the components
can also be defined in a config file.


This builds on the [ConfigArgParse](https://github.com/bw2/ConfigArgParse) package, but instead of a replacement 
for the `ArgumentParser` class, provides its own class `ConfigSimple`
which can be used to define the possible settings using 
`add_argument` and after parsing the settings, to retrieve the 
setting values.

Each `ConfigSimple` instance represents either the "top level" settings
(similar to `ArgumentParser` usually for tools and programs) or a component
setting that belongs to a top level setting instance.

The `configsimple` package provides a default top level settings singleton, 
`configsimple.config`.  
  
Here is an example of how to define the settings
for the toplevel and two components, where the 
toplevel selects the component to get used:

example/example1.py:
```python
from configsimple import topconfig, ConfigSimple, flag


class Component1:
    def __init__(self):
        myconf = ConfigSimple(component="comp1")
        topconfig.add_config(myconf)
        myconf.add_argument("--foo", default="22", type=int, help="The FOO setting!")
        myconf.add_argument("--bar", type=flag)
        myconf.parse_args()
        print("Component1 foo is {}".format(myconf.get("foo")))


class Component2:
    def __init__(self):
        myconf = ConfigSimple(component="comp2")
        topconfig.add_config(myconf)
        myconf.add_argument("--foo", default="xyz", type=str, help="The FOO setting, but a different one!")
        myconf.parse_args()
        print("Component2 foo is {}".format(myconf.get("foo")))


if __name__ == "__main__":
    topconfig.add_argument("--bar", help="The BAR setting")
    topconfig.add_argument("--foo", help="The toplevel FOO setting")
    topconfig.add_argument("--comp", type=int, choices=[1, 2], required=True,  help="Component number")
    topconfig.add_argument("pos1")
    topconfig.parse_args()
    print("Toplevel foo is {}".format(topconfig.get("foo")))
    compclass = [Component1, Component2][topconfig.get("comp")-1]
    comp = compclass()
    print("We are using component class: ", compclass)
    print("Get the global comp1.foo: {}".format(topconfig.get("comp1.foo")))
    print("Get the global comp2.foo: {}".format(topconfig.get("comp2.foo")))
    print("Get the global comp1.bar: {}".format(topconfig.get("comp1.bar")))
    print("Top positional parameter pos1: {}".format(topconfig.get("pos1")))
```

One way to run this:
```
$ python examples/example1.py --comp 1 1 --comp1.foo 2
Toplevel foo is None
Component1 foo is 2
Get the global comp1.foo: 2
Get the global comp2.foo: None
Get the global comp1.bar: None
Top positional parameter pos1: 1
```

This selects component comp1 to get initialised which in turn will
set the comp1.foo parameter. Note that the positional parameter
"pos1" MUST be specified before any component arguments!

In order to get usage information for the component comp1 settings,
we cann run:
```
$ python examples/example1.py --comp 1 x --comp1.help
Toplevel foo is None
usage: example1.py [--comp1.help] [--comp1.config_file COMP1.CONFIG_FILE]
                   [--comp1.save_config_file CONFIG_OUTPUT_PATH]
                   [--comp1.foo COMP1.FOO] [--comp1.bar COMP1.BAR]

optional arguments:
  --comp1.help          Show help for the 'comp1' component
  --comp1.config_file COMP1.CONFIG_FILE
                        Specify a file from which to load settings for
                        component 'comp1'
  --comp1.save_config_file CONFIG_OUTPUT_PATH
                        Specify a file to which to save specified settings.
  --comp1.foo COMP1.FOO
                        The FOO setting!
  --comp1.bar COMP1.BAR
```
This shows the help information as soon as the parameters are getting
parsed in component comp1. For this to work, the required
top level arguments have to be provided. 

Another and maybe better way to do this, especially when all possible
components are known in advance is similar to this:

```python
from configsimple import topconfig, flag


class Component1:
    @staticmethod
    def configsimple(config=None, component="comp1"):
        myconf = config or topconfig.get_config(component=component)
        myconf.add_argument("--sub1.sub2.foo", default="22", type=int, help="The FOO setting!")
        myconf.add_argument("--sub1.sub3.sub4.bar", type=flag)
        return myconf

    def __init__(self):
        cfg = Component1.configsimple()
        topconfig.add_config(cfg)
        cfg.parse_args()
        print("Component1 sub1.sub2.foo is {}".format(cfg.get("sub1.sub2.foo")))

class Component2:
    def configsimple(config=None, component="comp2"):
        myconf = config or topconfig.get_config(component=component)
        myconf.add_argument("--foo", default="xyz", type=str, help="The FOO setting, but a different one!")
        return myconf

    def __init__(self):
        myconf = Component2.configsimple()
        topconfig.add_config(myconf)
        myconf.parse_args()
        print("Component2 foo is {}".format(myconf.get("foo")))


if __name__ == "__main__":
    topconfig.add_argument("--bar", help="The BAR setting")
    topconfig.add_argument("--foo", help="The toplevel FOO setting")
    topconfig.add_argument("--comp", type=int, choices=[1, 2], required=True,  help="Component number")
    topconfig.add_argument("pos1")
    topconfig.add_config(Component1.configsimple())
    topconfig.add_config(Component2.configsimple())
    topconfig.parse_args()
    print("Toplevel foo is {}".format(topconfig.get("foo")))
    compclass = [Component1, Component2][topconfig.get("comp")-1]
    comp = compclass()
    print("Get the global comp1.foo: {}".format(topconfig.get("comp1.foo")))
    print("Get the global comp2.foo: {}".format(topconfig.get("comp2.foo")))
    print("Get the global comp1.bar: {}".format(topconfig.get("comp1.bar")))
    print("Get the global comp1.sub1.sub2.foo: {}".format(topconfig.get("comp1.sub1.sub2.foo")))
    print("Top positional parameter pos1: {}".format(topconfig.get("pos1")))
``` 

Here each component has a static function that returns a component 
config with all arguments added. These configs can be added in the 
top-level code and "--help" will then show the help for the top level
and all added configs. 




## NOTE

This package is meant to build on and depend on [ConfigArgParse](https://github.com/bw2/ConfigArgParse) package,
but because of a problem in that code, a slightly modified version of
configargparse.py is currently directly included.  
