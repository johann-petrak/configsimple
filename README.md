# simpleconfig

Configure a command/tall and its components via command line options, config files and environment variables.

This builds on the [ConfigArgParse](https://github.com/bw2/ConfigArgParse) package, but instead of a replacement 
for the `ArgumentParser` class, provides its own class `SimpleConfig`
which can be used to define the possible settings using 
`add_argument` and after parsing the settings, to retrieve the 
setting values.

Each `SimpleConfig` instance represents either the "top level" settings
(similar to `ArgumentParser` usually for tools and programs) or a component
setting that belongs to a top level setting instance.

The `simpleconfig` package provides a default top level settings singleton, 
`simpleconfig.config`.  
  
Here is an example of how to define the settings
for the toplevel and two components, where the 
toplevel selects the component to get used:

example1.py:
```python
from simpleconfig import config


```
