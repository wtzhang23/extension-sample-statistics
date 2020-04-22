#!/usr/bin/python3
import importlib
import os
import sys
import argparse
import traceback

def main():
    assert importlib.util.find_spec('matplotlib') is not None, '[import error] matplotlib not found, did you install it?'
    assert importlib.util.find_spec('matplotlib.pyplot') is not None, '[import error] matplotlib.pyplot not found, did you install it?'
    assert importlib.util.find_spec('numpy') is not None, '[import error] numpy not found, did you install it?'

    # imports
    matplotlib = importlib.import_module('matplotlib')
    np = importlib.import_module('numpy')

    parser = argparse.ArgumentParser(description='Get sample statistics for file reads with a certain extension. The files must only consist of one number.')
    parser.add_argument('extension', action='store', metavar='E', type=str, help='the file extension')
    parser.add_argument('--force', '-f', action='store_true', help='Forces the program to continue executing instead of prompting.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show all error messages.')
    parser.add_argument('--plot-type', '-p',
            dest='type',
            action='store',
            default='none', 
            choices=('none', 'histogram', 'boxplot', 'n', 'h', 'b'),
            help='The type of graph to plot.')
    parser.add_argument('--output-path', '-o',
            dest='filename',
            action='store',
            default='x.png',
            help='The file name of the plot.')
    parser.add_argument('--title', '-t',
            dest='title',
            action='store',
            default='distribution',
            help='The title of the plot.')
    parser.add_argument('--x-label', '-x',
            dest='xlabel',
            action='store',
            default='values',
            help='The x-axis label.')
    parser.add_argument('--y-label', '-y',
            dest='ylabel',
            action='store',
            default=None,
            help='The y-axis label.')
    parser.add_argument('--backend', '-b',
            dest='backend',
            action='store',
            default=matplotlib.get_backend(),
            help=f'The backend to be used by matplotlib. By default, {matplotlib.get_backend()}.')
    args = parser.parse_args()

    matplotlib.use(args.backend)
    plt = importlib.import_module('matplotlib.pyplot')

    ext = args.extension[1:] if args.extension[0] == '.' else args.extension
    if args.verbose:
        print(f'[status] sampling from files with the extension .{ext}.')
    def f(fp) :
        idx = fp.find(ext)
        return idx == len(fp) - len(ext) and idx > 1 and fp[idx - 1] == '.' # idx > 1 to ensure file has a name and is not a hidden file

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

    arr = np.array(data)
    mean, std = np.mean(arr), np.std(arr)
    fq, med, sq = np.percentile(arr, [25, 50, 75])
    iqr = sq - fq

    if args.verbose:
        print('[status] computing sample statistics.')
    print(f'mean: {mean:.3f}', f'std: {std:.3f}')
    print(f'median: {med:.3f}', f'1st quartile: {fq:.3f}', f'2nd quartile: {sq:.3f}', f'iqr: {iqr:.3f}')

    if args.type[0] != 'n':
        if args.type[0] == 'h':
            plt.hist(arr)
        elif args.type[0] == 'b':
            plt.boxplot(arr, vert = False)
        plt.title(args.title)
        plt.xlabel(args.xlabel)
        if args.ylabel is not None:
            plt.ylabel(args.ylabel)
        
        save_file = True
        if os.path.isfile(args.filename) and not args.force:
            while True:
                ipt = input(f"[prompt] override {os.path.abspath(args.filename)}? [y/n]")
                if ipt in ('y', 'n', 'Y', 'n'):
                    break
            if ipt == 'n' or ipt == 'N':
                save_file = False
        if save_file:
            plt.savefig(args.filename)
            if args.verbose:
                print(f'[status] saved plot at {os.path.abspath(args.filename)}.')

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
            f.write(str(e))
            f.write(traceback.format_exc())
        
