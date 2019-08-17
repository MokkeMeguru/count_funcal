import ast
import collections
import argparse
import os
import json
import csv


def walktree(node):
    if isinstance(node, ast.FunctionDef):
        print(list(ast.walk(node)))
        for fields in ast.iter_fields(node):
            print(fields)
    for child in ast.iter_child_nodes(node):
        walktree(child)


def get_described_func(filename):
    with open(filename, 'r') as f:
        source = f.read()
        tree = ast.parse(source, filename)
        # walktree(tree)
        funcallList = [
            x.func.id for x in ast.walk(tree) if isinstance(x, ast.Call)
        ]
        c = collections.Counter(funcallList)
        print("filename: {}".format(filename))
        print("described func: {}".format(c.most_common()))
        return [filename, json.dumps(c.most_common())]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fname',
                        '-f',
                        type=str,
                        help="file name",
                        required=True)
    parser.add_argument('--type',
                        '-t',
                        type=str,
                        choices=['single-file', 'dir'],
                        help="file name",
                        required=True)
    parser.add_argument('--output',
                        '-o',
                        type=str,
                        help="output file name",
                        default='dumps.tsv')
    args = parser.parse_args()
    if (args.type == 'single-file'):
        get_described_func(args.fname)
    if (args.type == 'dir'):
        res = []
        for root, dirs, files in os.walk(args.fname):
            for f in files:
                if f.endswith('.py'):
                    res.append(get_described_func(os.path.join(root, f)))
    with open(args.output, 'w') as d:
        writer = csv.writer(d, delimiter='\t', quoting=csv.QUOTE_ALL)
        writer.writerows(res)
