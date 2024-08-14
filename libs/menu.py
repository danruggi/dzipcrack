import argparse

def menu():
    parser = argparse.ArgumentParser(description="ZIP Password Cracker")
    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=52)

    parser.add_argument('-z', action='store_true', help="Dummy flag to demonstrate flag usage")
    parser.add_argument('-t', action='store_true', help="Another dummy flag to demonstrate flag usage")
    parser.add_argument('-B', action='store_true', help="Bruteforce")
    parser.add_argument('--min_len', type=int, default=0, help="Password Length MIN")
    parser.add_argument('--max_len', type=int, default=32, help="Password Length MAX")
    parser.add_argument('--starts', type=str, required=False, default="", help="Start part of the password")
    parser.add_argument('--middle', type=str, required=False, default="", help="Middle part of the password")
    parser.add_argument('--ends', type=str, required=False, default="", help="End part of the password")
    parser.add_argument('--charset', type=str, required=False, default="aA1!", help="End part of the password")

    parser.add_argument('zipfile', help="Path to the password-protected ZIP file")

    args = parser.parse_args()

    tconf = {
        'FILE': args.zipfile,
        'STARTS': args.starts,
        'ENDS': args.ends,
        'MIDDLE': args.middle,
        'Z': args.z,
        'T': args.t,
        'B': args.B,
        'LMAX': args.max_len,
        'LMIN': args.min_len,
        'CHARSET': args.charset,
    }

    return tconf
