from configsimple import topconfig, flag

# Follow convention that each component adds the arguments in the class body and adds itself to topconfig.
# Here the config gets added to topconfig when the class is defined, but parsed only when the class is initialized
# This also illustrates how we can define hierarchical settings in a component
# NOTE: all instances of a component class will share the settings 
# In order to initialize different instances of the same class differently, these approaches are possible:
# * if each instance serves a different purpose, have a separate wrapper class for each of those
# * use code to auto-generate the configs for each instance and generate component names for them, e.g. 
#   mycomp01 to mycomp09 ... then tell the class which component to use at init time (__init__(self, comp=...))

class Component1:
    cfg = topconfig.get_config(component="comp1")
    cfg.add_argument("--sub1.sub2.foo", default="22", type=int, help="The FOO setting!")
    cfg.add_argument("--sub1.sub3.sub4.bar", type=flag)

    def __init__(self):
        print("Component1 parms: ", Component1.cfg.parms())
        Component1.cfg.parse_args()
        print("Config for component1: ", Component1.cfg)
        print("Component1 sub1.sub2.foo is {}".format(Component1.cfg.get("sub1.sub2.foo")))
        print("Component1 parsed args():", Component1.cfg.args())


class Component2:
    cfg = topconfig.get_config(component="comp2")
    cfg.add_argument("--foo", default="xyz", type=str, help="The FOO setting, but a different one!")

    def __init__(self):
        Component2.cfg.parse_args()
        print("Component2 foo is {}".format(Component2.cfg.get("foo")))





if __name__ == "__main__":
    topconfig.add_argument("--bar", help="The BAR setting")
    topconfig.add_argument("--foo", help="The toplevel FOO setting")
    topconfig.add_argument("--comp", type=int, choices=[1, 2], required=True,  help="Component number")
    topconfig.add_argument("pos1")
    print("Toplevel parms:", topconfig.parms())

    topconfig.parse_args()
    print("Toplevel parsed args:", topconfig.args())
    print("Toplevel foo is {}".format(topconfig.get("foo")))
    print("Toplevel args is {}".format(topconfig.args()))
    compclass = [Component1, Component2][topconfig.get("comp")-1]
    comp = compclass()
    comp1another = Component1()
    print("Get the global comp1.foo: {}".format(topconfig.get("comp1.foo")))
    print("Get the global comp2.foo: {}".format(topconfig.get("comp2.foo")))
    print("Get the global comp1.bar: {}".format(topconfig.get("comp1.bar")))
    print("Get the global comp1.sub1.sub2.foo: {}".format(topconfig["comp1.sub1.sub2.foo"]))
    print("Get local config comp1 sub1.sub2.foo: {}".format(topconfig.get_config(component="comp1")["sub1.sub2.foo"]))
    print("Get instance sub1.sub2.foo: {}".format(comp1another.cfg["sub1.sub2.foo"]))
    print("Top positional parameter pos1: {}".format(topconfig.get("pos1")))
    #print("All config keys: {}".format(topconfig.keys()))
    #print("All config items: {}".format(topconfig.items()))
    #print("The top config as string:", topconfig)
    #print("The top config repr:", repr(topconfig))
    # set a config value that should percolate down to a component setting
    topconfig["comp1.sub1.sub2.foo"] = 123456
    #print("Top config now:", topconfig)
    #print("Comp1 config now:", topconfig.get_config(component="comp1"))
    print("After changing, global comp1.sub1.sub2.foo: {}".format(topconfig["comp1.sub1.sub2.foo"]))
    print("After changing, local comp1 sub1.sub2.foo: {}".format(topconfig.get_config("comp1")["sub1.sub2.foo"]))
    print("After changing, instance comp1another sub1.sub2.foo: {}".format(comp1another.cfg["sub1.sub2.foo"]))
