import os
import argparse


def main(target_file):
    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            print(os.path.join(root, f))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_file',
                        dest='target_file',
                        default=None,
                        type=str,
                        help='please enter the target_file name')
    args = parser.parse_args()
    main(args.target_file)
