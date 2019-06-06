# see issue #1

def with_configargparse():
    import configargparse
    # print("Version:", configargparse.__version__)
    p = configargparse.ArgParser(
        add_config_file_help=False,
        add_env_var_help=False,
        auto_env_var_prefix="ENV",
        ignore_unknown_config_file_keys=False,
        default_config_files=[],
        description=None,
        usage=None,
        add_help=False,
        allow_abbrev=False,
        prefix_chars='-')
    # p.add("--comp1.cfile")
    p.add("--comp1.cfile", is_config_file_arg=True)
    args = ["--comp", "2"]
    ns, unkn = p.parse_known_args(args)
    print("NS=",ns,"UNKN=",unkn)


if __name__ == "__main__":
    with_configargparse()
