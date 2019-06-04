#
import configargparse
import re
import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="DEBUG")

PAT_OPTION = re.compile(r'(--?)([^.\s]+)')


class SimpleConfig:

    @staticmethod
    def fullname(component, option):
        """
        Returns the full option name, given a component and an option name. This is simply the two parts
        joined by a dot, or if component is the empty string, just option.
        If the option starts with one or two dashes, those dashes are moved in front.
        :param component: component name, or an empty string
        :param option: option name
        :return: full name
        """
        if component.strip() == "":
            return option
        else:
            if len(option) > 2 and option.startswith('--'):
                return '--' + component + '.' + option[2:]
            elif len(option) > 1 and option.startswith('-'):
                return '-' + component + '.' + option[1:]
            else:
                return component + "." + option

    def __init__(self, description=None, usage=None, component=None, config_files=None):
        if component is None:
            raise Exception("SimpleConfig component must be specified as empty string or a name")
        self.component = component
        if config_files is None:
            config_files = []
        elif not isinstance(config_files, list):
            config_files = [config_files]
        self.argparser = configargparse.ArgumentParser(
            default_config_files=config_files,
            description=description,
            usage=usage,
            add_help=False,
            allow_abbrev=False,
            prefix_chars='-')
        # always add the standard options: component.help, component.config_file
        self.argparser.add(SimpleConfig.fullname(self.component, "--help"), action="store_true",
                           help="Show help for the '{}' component".format(self.component))
        self.argparser.add(SimpleConfig.fullname(self.component, "--config_file"),
                           is_config_file_arg=True,
                           help="Specify a file from which to load settings for component '{}'".
                           format(self.component))
        self.namespace = None
        self.defaults = {}   # dictionary dest->value
        self.added_configs = []
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
        self.merge_namespace(config.namespace)

    def add_argument(self, *args, **kwargs):
        # intercept all the args and use componentame.optionname instead
        options_new = []
        for option_string in args:
            m = PAT_OPTION.match(option_string)
            if m is None:
                raise Exception("Not a valid option string: {}".format(option_string))
            prefixchars, optionname = m.groups()
            options_new.append(prefixchars + SimpleConfig.fullname(self.component, optionname))
        # intercept the dest keyword
        kwargs.setdefault('dest', None)
        dest = kwargs.pop("dest")
        if dest is None:
            dest = optionname
        if dest is not None:
            if "." in dest:
                raise Exception("dest must not contain a dot")
            dest = SimpleConfig.fullname(self.component, dest)
            kwargs["dest"] = dest
        # intercept the default value, we do not allow argparse to handle this
        kwargs.setdefault("default", None)
        default = kwargs.pop("default")
        self.defaults[dest] = default
        logger.debug("Defaults for {} are now {}".format(self.component, self.defaults))
        self.argparser.add_argument(*options_new, **kwargs)

    def parse_args(self, args=None):
        self.namespace, unknown = self.argparser.parse_known_args(args)
        logger.debug("Namespace for {} after parse: {}".format(self.component, vars(self.namespace)))
        # first of all, check if we have a help request:
        if self.get("help"):
            raise Exception("SHOULD BE SHOWING HELP HERE")
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
                else:
                    nameshortened = optionname
                if "." in nameshortened:
                    raise Exception("Option {} not defined for component {}".format(nameshortened, self.component))
        # now process any config file settings and environment settings
        # configargparse alreadt handles local files and environment vars, we handle inheritance
        # and falling back to the specified default here
        if self.parent is not None:
            # TODO: set from parent settings what is still not set
            # This would be anything that was set from a file loaded in the parent for this namespace!
            pass
        # set what is still not set from the local defaults
        for k, v in self.defaults.items():
            if getattr(self.namespace, k) is None:
                setattr(self.namespace, k, v)
        # now that we have all the settings, merge them into the global settings in
        # the parent (which will bubble up to its parent and so on)
        if self.parent is not None:
            self.parent.merge_namespace(self.namespace)

    def get(self, option, default=None, exception_if_missing=False):
        """
        Get the setting for 'option' for this component. 'option' is just the name of the
        option, without the component name which is added automatically. However, the options
        :param option: the name of the option for which to retrieve the value
        :param default: a default value if the current value of the option is None
        :param exception_if_missing: instead of returning the default value, throw an exception
        :return: the value of the option or the specified default value unless an exception is thrown
        """
        name = SimpleConfig.fullname(self.component, option)
        d = vars(self.namespace)
        if exception_if_missing and name not in d:
            raise Exception("Setting {} not found for component '{}'".format(option, self.component))
        return d.get(name, default)

    def set(self, parm, value):
        name = SimpleConfig.fullname(self.component, parm)
        self.namespace.setattr(name, value)
        if self.parent is not None:
            self.parent.set(name, value)

    def merge_namespace(self, ns):
        """
        Merge the given namespace into our own namespace.
        :param ns: namespace to merge into our own
        :return:
        """
        logger.debug("Merging from NS: {}".format(ns))
        for k, v in vars(ns).items():
            logger.debug("Merging into {}: {} <= {}".format(self.namespace, k, v))
            setattr(self.namespace, k, v)
        logger.debug("NS IS NOW: {}".format(self.namespace))

