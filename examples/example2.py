from configsimple import topconfig, ConfigSimple, flag


class Component1:
    @staticmethod
    def configsimple(config=None, component="comp1"):
        myconf = config or topconfig.get_config(component=component)
        myconf.add_argument("--foo", default="22", type=int, help="The FOO setting!")
        myconf.add_argument("--bar", type=flag)
        return myconf

    def __init__(self):
        cfg = Component1.configsimple()
        topconfig.add_config(cfg)
        cfg.parse_args()
        print("Component1 foo is {}".format(cfg.get("foo")))


class Component2:
    @staticmethod
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
    #topconfig.add_config(Component1.configsimple())
    #topconfig.add_config(Component2.configsimple())
    topconfig.parse_args()
    print("Toplevel foo is {}".format(topconfig.get("foo")))
    compclass = [Component1, Component2][topconfig.get("comp")-1]
    comp = compclass()
    print("Get the global comp1.foo: {}".format(topconfig.get("comp1.foo")))
    print("Get the global comp2.foo: {}".format(topconfig.get("comp2.foo")))
    print("Get the global comp1.bar: {}".format(topconfig.get("comp1.bar")))
    print("Top positional parameter pos1: {}".format(topconfig.get("pos1")))


