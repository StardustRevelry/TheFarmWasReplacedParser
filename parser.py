import os
import ast
from ast import NodeTransformer, NodeVisitor

from package.ast_transformer import *

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.realpath(__file__))
    scripts_dir = os.path.join(current_dir, 'demo')
    test_feature = "lambda"
    test_file = os.path.join(scripts_dir, f"{test_feature}_demo.py")
    build_name = os.path.join(scripts_dir, f"{test_feature}_parsed.py")

    with open(test_file, 'r', encoding="utf-8") as f:
        code = f.read()

    node_tree = ast.parse(code)

    save_file = os.path.join(scripts_dir, f'{test_feature}.ast')
    with open(save_file, 'w', encoding="utf-8") as f:
        f.write(ast.dump(node_tree, indent=4))

    transformers = [
        LambdaTransformer()
    ]
    transformed_tree = node_tree
    for transformer in transformers:
        transformed_tree = transformer.visit(transformed_tree)

    save_file = os.path.join(scripts_dir, build_name)
    with open(save_file, 'w', encoding="utf-8") as f:
        f.write(ast.unparse(transformed_tree))

    print("Parsing Done")

    print("Try generated file")
    os.system(f"python {save_file}")