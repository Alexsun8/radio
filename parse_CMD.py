import argparse


def parse_cmd():
    parser = argparse.ArgumentParser(description='Compare 2 audio files')

    parser.add_argument('path1', type=str,
                        help='Base file')

    parser.add_argument('path2', type=str,
                        help='File for checking')

    parser.add_argument('--config', '-c', dest='confPath',
                        help='Config files with params')

    parser.add_argument('--plot', '-p', dest='plotPath',
                        help='pathForSavingPlot')


    args = parser.parse_args()
    return args.path1, args.path2, args.confPath, args.plotPath


