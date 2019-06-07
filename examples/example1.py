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
    print("Get the global comp1.foo: {}".format(topconfig.get("comp1.foo")))
    print("Get the global comp2.foo: {}".format(topconfig.get("comp2.foo")))
    print("Get the global comp1.bar: {}".format(topconfig.get("comp1.bar")))
    print("Top positional parameter pos1: {}".format(topconfig.get("pos1")))


