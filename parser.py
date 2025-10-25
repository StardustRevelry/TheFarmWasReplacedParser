import os
import ast
from ast import NodeTransformer, NodeVisitor

from package.ast_transformer import *

def parse_all_files(path):
    """
    Parse all python files in the given path and return a dict of nodes.
    """

    nodes: dict[str, ast.AST] = {}

    # read all python files in the given path
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    code = f.read()
                    try:
                        node = ast.parse(code)
                        rel_path = os.path.relpath(root, path)
                        rel_path_file = os.path.join(rel_path, file)
                        nodes[rel_path_file] = node
                    except SyntaxError as e:
                        print(f"Error parsing {file}: {e}")

    # init all transformers
    dec_trans = DecoratorTransformer()
    lbd_trans = LambdaTransformer()

    # apply all transformers influencing single node-tree
    for file, node in nodes.items():
        dec_trans.visit(node)
        lbd_trans.visit(node)

    return nodes

def save_nodes(nodes, path):
    """
    Save all nodes to the given path.
    """

    for file, node in nodes.items():
        with open(os.path.join(path, file), 'w') as f:
            f.write(ast.unparse(node))

