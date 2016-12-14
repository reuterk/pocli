"""
"""


from . import lib


def parse_args():
    import argparse
    from . import lib
    # ---
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Commands')
    # ---
    parser_put = subparsers.add_parser(
        'put', help='upload file(s)')
    # parser_put.add_argument('--input', type=str, help='input parameter file')
    parser_put.set_defaults(func=lib.put)
    parser_put.add_argument('--destination', '-d', type=str, help='remote destination directory')
    parser_put.add_argument('files', nargs=argparse.REMAINDER, help='file(s)')
    # ---
    parser_get = subparsers.add_parser(
        'get', help='download file')
    parser_get.set_defaults(func=lib.get)
    # ---
    parser_ls = subparsers.add_parser(
        'ls', help='list remote directory')
    parser_ls.set_defaults(func=lib.ls)
    parser_ls.add_argument('dir', nargs=argparse.REMAINDER, help='directory')
    # ---
    parser_mkdir = subparsers.add_parser(
        'mkdir', help='create remote directory')
    parser_mkdir.set_defaults(func=lib.mkdir)
    parser_mkdir.add_argument('dir', nargs=argparse.REMAINDER, help='directory')
    # ---
    parser_check = subparsers.add_parser(
        'check', help='check if current OwnCloud configuration works')
    parser_check.set_defaults(func=lib.check)
    # ---
    parser_init = subparsers.add_parser(
        'init', help='initialize .pocrc config file')
    parser_init.set_defaults(func=lib.init)
    # ---
    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
