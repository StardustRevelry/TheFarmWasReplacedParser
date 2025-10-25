import ast

from ast import NodeTransformer

class DecoratorTransformer(NodeTransformer):
    def __init__(self):
        self.counter = 0
        self.prefix = "__temp_"
        self.func_names = set()

    def get_temp_func_name(self, name: str):
        if name in self.func_names:
            suffix = str(self.counter)
            self.counter += 1
            return self.prefix + name + suffix
        else:
            self.func_names.add(name)
            return self.prefix + name

    def visit_FunctionDef(self, node):
        if node.decorator_list:
            inner_counter = len(node.decorator_list) - 1
            origin_func_name = node.name
            func_name = self.get_temp_func_name(node.name)
            new_node = ast.FunctionDef(
                name=func_name,
                args=node.args,
                body=node.body,
                decorator_list=[],
                returns=node.returns
            )
            ast.copy_location(new_node, node)

            # apply decorator to the inner function
            call_expr = ast.Name(id=func_name, ctx=ast.Load())
            for decorator in reversed(node.decorator_list.copy()):
                call_expr = ast.Call(
                    func=decorator,
                    args=[call_expr],
                    keywords=[]
                )

            # assign the result to the original function name
            assign_func = ast.Assign(
                targets=[ast.Name(id=origin_func_name, ctx=ast.Store())],
                value=call_expr
            )
            ast.copy_location(assign_func, node)

            return [new_node, assign_func]
        else:
            return node
