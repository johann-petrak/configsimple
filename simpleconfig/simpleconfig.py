#
import argparse
import re

PAT_OPTION = re.compile(r'(--?)([^.\s]+)')


class SimpleConfig:

    @staticmethod
    def fullname(component, option):
        """
        Returns the full option name, given a component and an option name. This is simply the two parts
        joined by a dot, or if component is the empty string, just option
        :param component: component name, or an empty string
        :param option: option name
        :return: full name
        """
        if component.strip() == "":
            return option
        else:
            return component + "." + option

    def __init__(self, description=None, usage=None, component=None, config_file=None):
        if component is None:
            raise Exception("SimpleConfig component must be specified as empty string or a name")
        self.component = component
        self.argparser = argparse.ArgumentParser(
            description=description, usage=usage, add_help=True, allow_abbrev=False, prefix_chars='-')
        # always add the standard options: component.help, component.config_file
        self.argparser.add_argument("--"+SimpleConfig.fullname(self.component, "help"), action="store_true",
                                    help="Show help for the '{}' component".format(self.component))
        self.argparser.add_argument("--"+SimpleConfig.fullname(self.component, "config_file", type=str),
                                    help="Specify a file from which to load settings for component '{}'".format(self.component))
        self.namespace = None
        self.defaults = {}   # dictionary dest->value
        self.added_configs = []
        self.config_file = config_file
        self.parent = None  # this will be set if this config gets added to another config

    def add_config(self, config):
        """
        Add the given SimpleConfig to this instance. This is usually used to add a component-wise config to the
        global config. This should happen as soon as it is created and all arguments have been added, but BEFORE
        the local config parses the arguments
        :param config: the other local config to add
        :return:
        """
        # before we add, check that the component name is not already added!
        if config.component == self.component:
            raise Exception("Cannot add config, component name {} already there added".format(config.component))
        for cfg in self.added_configs:
            if cfg.component == config.component:
                raise Exception("Cannot add config, component name {} already there added".format(config.component))
        self.added_configs.append(config)
        config.parent = self

    def add_argument(self, *args, **kwargs):
        # intercept all the args and use componentame.optionname instead
        options_new = []
        for option_string in args:
            m = PAT_OPTION.match(option_string)
            if m is None:
                raise Exception("Not a valid option string: {}".format(option_string))
            prefixchars, optionname = m.groups()
            options_new = prefixchars + SimpleConfig.fullname(self.component, optionname)
        # intercept the dest keyword
        dest = kwargs.pop("dest")
        if dest is not None:
            if "." in dest:
                raise Exception("dest must not contain a dot")
            dest = SimpleConfig.fullname(self.component, dest)
            kwargs["dest"] = dest
        # intercept the default value, we do not allow argparse to handle this
        default = kwargs.pop("default")
        self.defaults[default] = default
        self.argparser.add_argument(*options_new, **kwargs)

    def parse_args(self, args=None):
        ns, unknown = self.argparser.parse_known_args()
        for val in unknown:
            if val.startswith("-"):
                m = PAT_OPTION.match(val)
                if m is None:
                    raise Exception("Odd unknown option name for component {}: {}".format(self.component, val))
                prefixchars, optionname = m.groups()
                # if the optionname starts with the component name, remove the component name and
                # check if the remainder contains a dot. If not, it is meant to refer to this component so it is
                # unknown and invalid
                if self.component == "":
                    nameshortened = optionname
                elif optionname.startswith(self.component+"."):
                    nameshortened = optionname[len(self.component)+1:]
                if "." not in nameshortened:
                    raise Exception("Option {} not defined for component {}".format(nameshortened, self.component))
        # now process any config file settings and environment settings
        # we do this in decreasing order of priority:
        # * config file specified on the command line for this component
        # * config file specified when we initialised this component config
        # * setting from the parent (from some config file) but not from the merged settings in the parent
        # * default specified in the add_argument call
        if ns.config_file is not None:
            # TODO: set from there what is not set through command line!
            pass
        if self.config_file is not None:
            # TODO: set from there what is still not set
            pass
        if self.parent is not None:
            # TODO: set from parent settings what is still not set
            pass
        # set what is still not set from the local defaults
        for k, v in self.defaults:
            if getattr(ns, k) is None:
                setattr(ns, k, v)
        self.namespace = ns

    def get(self, parm, default=None, exception_if_missing=False):
        name = SimpleConfig.fullname(self.component, parm)
        d = self.namespace.__dict__
        if exception_if_missing and name not in d:
            raise Exception("Setting {} not found for component '{}'".format(parm, self.component))
        return d.get(name, default)

    def set(self, parm, value):
        name = SimpleConfig.fullname(self.component, parm)
        self.namespace.setattr(name, value)
        if self.parent is not None:
            self.parent.set(name, value)
