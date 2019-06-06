# configsimple

Configure a command/tall and its components via command line options, config files and environment variables.

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
from configsimple import config, ConfigSimple, flag


class Component1:
    def __init__(self):
        myconf = ConfigSimple(component="comp1")
        config.add_config(myconf)  # always immediately add to top config!
        myconf.add_argument("--foo", default="22", type=int, help="The FOO setting!")
        myconf.add_argument("--bar", type=flag)
        myconf.parse_args()
        foo = myconf.get("foo")


class Component2:
    def __init__(self):
        myconf = ConfigSimple(component="comp2")
        config.add_config(myconf)
        myconf.add_argument("--foo", default="xyz", type=str, help="The FOO setting, but a different one!")
        myconf.parse_args()
        foo = myconf.get("foo")


if __name__ == "__main__":
    config.add_argument("--bar", help="The BAR setting")
    config.add_argument("--foo", help="The toplevel FOO setting")
    config.add_argument("--comp", type=int, choices=[1, 2], required=True,  help="Component number")
    config.parse_args()
    print("Toplevel foo is {}".format(config.get("foo")))
    compclass = [Component1, Component2][config.get("comp")-1]
    comp = compclass()
    print("Get the global comp1.foo: {}".format(config.get("comp1.foo")))
    print("Get the global comp2.foo: {}".format(config.get("comp2.foo")))
    print("Get the global comp1.bar: {}".format(config.get("comp1.bar")))
```




## NOTE

This package is meant to build on and depend on [ConfigArgParse](https://github.com/bw2/ConfigArgParse) package,
but because of a problem in that code, a slightly modified version of
configargparse.py is currently directly included.  
