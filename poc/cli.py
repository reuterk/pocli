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
        'put',
        help='upload file')
    # parser_put.add_argument('--input', type=str, help='input parameter file')
    parser_put.set_defaults(func=lib.put)
    # ---
    parser_get = subparsers.add_parser(
        'get',
        help='download file')
    parser_get.set_defaults(func=lib.get)
    # ---
    parser_ls = subparsers.add_parser(
        'ls',
        help='list remote directory')
    parser_ls.set_defaults(func=lib.ls)
    # ---
    parser_mkdir = subparsers.add_parser(
        'mkdir',
        help='create remote directory')
    parser_mkdir.set_defaults(func=lib.mkdir)
    # ---
    parser_check = subparsers.add_parser(
        'check',
        help='check if current OwnCloud configuration works')
    parser_check.set_defaults(func=lib.check)
    # ---
    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
