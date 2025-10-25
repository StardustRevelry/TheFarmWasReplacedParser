import ast

from ast import NodeTransformer

HAS_SCOPE = (
    ast.Module,
    ast.FunctionDef,
    ast.ClassDef,
    ast.With,
    ast.If,
    ast.For,
    ast.While,
    ast.Try,
    ast.TryStar,
    ast.match_case
)
# No plan for async support.
# AsyncFunctionDef, AsyncWith, AsyncFor

class LambdaTransformer(NodeTransformer):
    def __init__(self):
        self.counter = 0
        self.depth = 0
        self.prefix = "__lambda_"
        # Tracks the starting line number of orelse blocks at each depth to determine if a lambda is in an orelse section
        self.orelse_start_lineno = {}
        self.lambda_functions = {}
        self.ext = False

    def visit(self, node):
        visit_scope = isinstance(node, HAS_SCOPE)
        if visit_scope:
            if orelse_start_lineno := getattr(node, "orelse", None) and node.orelse[0].lineno:
                self.orelse_start_lineno[self.depth] = orelse_start_lineno
            self.depth += 1
        node = super().visit(node)

        if visit_scope:
            functions = []
            functions_in_orelse = []
            items = self.lambda_functions.pop(self.depth, None)
            if items is not None:
                for item in items.items():
                    name, (child_node, is_orelse) = item
                    if not is_orelse:
                        functions.append(self.__generate_function_from_lambda((name, child_node), node))
                    else:
                        functions_in_orelse.append(self.__generate_function_from_lambda((name, child_node), node))
            self.__insert_node(functions, node)
            self.__insert_node(functions_in_orelse, node, True)
            self.depth -= 1
            self.orelse_start_lineno.pop(self.depth, None)
        return node

    def visit_Lambda(self, node):
        name = f"{self.prefix}{self.counter}"
        self.counter += 1
        # Checks if the lambda is in the orelse part of the parent scope using line numbers
        is_orelse = (parent_depth := self.depth - 1) in self.orelse_start_lineno and node.lineno >= self.orelse_start_lineno[parent_depth]
        if self.depth not in self.lambda_functions:
            self.lambda_functions[self.depth] = {}
        self.lambda_functions[self.depth][name] = (node, is_orelse) # node, is_orelse
        return ast.Name(id=name, ctx=ast.Load())

    def __generate_function_from_lambda(self, node_tuple, scope):
        name, node = node_tuple
        new_node = ast.FunctionDef(
            name=name,
            args=node.args,
            body=[ast.Return(node.body)],
        )
        ast.copy_location(new_node, scope)
        if not hasattr(new_node, "lineno"):
            new_node.lineno = 1
        # Recursively visits the new function to handle any nested lambdas
        new_node = self.visit(new_node)
        return new_node

    def __insert_node(self, node, scope, is_orelse=False):
        if len(node) == 0:
            return
        if not isinstance(scope, ast.Module):
            for item in reversed(node):
                if is_orelse:
                    scope.orelse.insert(0, item)
                else:
                    scope.body.insert(0, item)
        else:
            pos_after_import = 0
            for i, item in enumerate(scope.body):
                if isinstance(item, (ast.Import, ast.ImportFrom)):
                    pos_after_import = i + 1
                else:
                    break
            for item in reversed(node):
                scope.body.insert(pos_after_import, item)