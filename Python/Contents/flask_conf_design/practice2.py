from argparse import ArgumentParser

args_parser = ArgumentParser(description="test")


def t_or_f(arg):
    ua = str(arg).upper()
    if 'TRUE'.startswith(ua):
        return True
    elif 'FALSE'.startswith(ua):
        return False
    else:
        pass


args_parser.add_argument("--flush", dest="hello", type=t_or_f, default="True")
args_parser.add_argument("--type", type=str, default="T")

args = args_parser.parse_args()
print(args)

