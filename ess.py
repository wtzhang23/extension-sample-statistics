#!/usr/bin/python3
import importlib
import os
import sys
import argparse
import traceback

def main():

    if importlib.util.find_spec('matplotlib') is None:
        print('[import error] matplotlib not found, did you install it?')
        exit(1)
    
    if importlib.util.find_spec('matplotlib.pyplot') is None:
        print('[import error] matplotlib.pyplot not found, did you install it?')
        exit(1)

    if importlib.util.find_spec('numpy') is None:
        print('[import error] numpy not found, did you install it?')
        exit(1)

    # imports
    matplotlib = importlib.import_module('matplotlib')
    np = importlib.import_module('numpy')

    graph_types = ('NONE', 'HISTOGRAM', 'BOXBLOT', 'N', 'H', 'B')

    parser = argparse.ArgumentParser(description='Get sample statistics for file reads with a certain extension. The files must only consist of one number.')
    parser._actions[0].help = 'Show this message and exit.'
    parser.add_argument('extension', action='store', metavar='E', type=str, help='the file extension')
    parser.add_argument('-f', '--force', action='store_true', help='Forces the program to continue executing instead of prompting.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show all error messages.')
    parser.add_argument('-p', '--plot-type',
            dest='type',
            action='store',
            metavar='P',
            type=str.upper,
            default='NONE', 
            choices=('NONE', 'HISTOGRAM', 'BOXBLOT', 'N', 'H', 'B'),
            help=f'The type of graph to plot. The supported graphs are histograms and boxplots. Valid arguments: {graph_types}.')
    parser.add_argument('-o', '--output-path',
            dest='filename',
            action='store',
            metavar='F',
            default='x.png',
            help='The file name of the plot.')
    parser.add_argument('-t', '--title',
            dest='title',
            action='store',
            metavar='T',
            default='distribution',
            help='The title of the plot.')
    parser.add_argument('-x', '--x-label',
            dest='xlabel',
            action='store',
            metavar='X',
            default='values',
            help='The x-axis label.')
    parser.add_argument('-y', '--y-label',
            dest='ylabel',
            action='store',
            metavar='Y',
            default=None,
            help='The y-axis label.')
    parser.add_argument('-b', '--backend',
            dest='backend',
            metavar='B',
            action='store',
            default=matplotlib.get_backend(),
            help=f'The backend to be used by matplotlib for plot generation. By default, {matplotlib.get_backend()} is used.')
    args = parser.parse_args()

    matplotlib.use(args.backend)
    plt = importlib.import_module('matplotlib.pyplot')

    ext = args.extension[1:] if args.extension[0] == '.' else args.extension
    if args.verbose:
        print(f'[status] sampling from files with the extension .{ext}.')
    def f(fp) :
        idx = fp.find(ext)
        return idx == len(fp) - len(ext) and idx > 0 and fp[idx - 1] == '.'

    data = []
    for file_path in filter(f, os.listdir('.')):
        with open(file_path, 'r') as read:
            s = ' '.join(read.readlines()).strip() # space added to give warning if file contains anything other than a lone number
            try:
                data.append(float(s))
                if args.verbose:
                    print(f'[read] read {data[-1]} from {file_path}.')
            except ValueError:
                if args.verbose:
                    print(f'[invalid file] skipped {file_path} as contents are not a parsable number.')

    if len(data) == 0:
        print(f'[error] no files found with extension .{ext}.')
        exit(64)

    arr = np.array(data)
    mean, std = np.mean(arr), np.std(arr)
    fq, med, sq = np.percentile(arr, [25, 50, 75])
    iqr = sq - fq

    if args.verbose:
        print('[status] computing sample statistics.')
    print(f'mean: {mean:.3f}', f'std: {std:.3f}')
    print(f'median: {med:.3f}', f'1st quartile: {fq:.3f}', f'2nd quartile: {sq:.3f}', f'iqr: {iqr:.3f}')

    if args.type[0] != 'N':
        try:
            if args.type[0] == 'H':
                plt.hist(arr)
            elif args.type[0] == 'B':
                plt.boxplot(arr, vert = False)
            plt.title(args.title)
            plt.xlabel(args.xlabel)
            if args.ylabel is not None:
                plt.ylabel(args.ylabel)
        except Exception as e:
            print(f'[error] {e}')
            exit(1)
        
        save_file = True
        if os.path.isfile(args.filename) and not args.force:
            while True:
                ipt = input(f"[prompt] override {os.path.abspath(args.filename)}? [y/n]")
                if ipt in ('y', 'n', 'Y', 'n'):
                    break
            if ipt == 'n' or ipt == 'N':
                save_file = False
        if save_file:
            try:
                plt.savefig(args.filename)
                if args.verbose:
                    print(f'[status] saved plot at {os.path.abspath(args.filename)}.')
            except IOError as io:
                print(f'[error] {io}.')
                exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        idx = 0
        path = f'fp{idx}.log'
        while os.path.isfile(path):
            idx = idx + 1
            path = f'fp{idx}.log'
        print(f'[error] dumped unhandled error into {os.path.abspath(path)}.')
        with open(path, 'w') as f:
            f.write(e)
            f.write(traceback.format_exc())
        exit(1)
        
