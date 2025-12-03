"""
AST Tree Visualizer for MiniLang compiler.
Creates tree-like visual representation of the Abstract Syntax Tree.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

from ast_nodes import *

class TreeVisualizer(ASTVisitor):
    """Visitor that creates a tree-like visual representation of the AST."""
    
    def __init__(self):
        self.tree_lines = []
        self.current_depth = 0
    
    def _get_prefix(self, is_last=False, depth=None):
        """Get the prefix for the current line based on depth and position."""
        if depth is None:
            depth = self.current_depth
        
        if depth == 0:
            return ""
        
        prefix = ""
        for i in range(depth - 1):
            prefix += "    "  # 4 spaces for each level
        
        if is_last:
            prefix += "└── "
        else:
            prefix += "├── "
        
        return prefix
    
    def _add_line(self, text, is_last=False):
        """Add a line to the tree output."""
        prefix = self._get_prefix(is_last)
        self.tree_lines.append(prefix + text)
    
    def _visit_children(self, children, labels=None):
        """Visit a list of child nodes."""
        if not children:
            return
        
        self.current_depth += 1
        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)
            
            if labels and i < len(labels):
                # Add a label before the child
                label_prefix = self._get_prefix(False if child else is_last)
                self.tree_lines.append(label_prefix + labels[i] + ":")
                self.current_depth += 1
                if child:
                    self.visit(child)
                self.current_depth -= 1
            else:
                if child:
                    self.visit(child)
        self.current_depth -= 1
    
    def get_tree_string(self):
        """Get the complete tree as a string."""
        return "\n".join(self.tree_lines)
    
    def visit_program(self, node: Program):
        self._add_line("PROGRAM")
        self._visit_children(node.statements)
    
    def visit_var_declaration(self, node: VarDeclaration):
        self._add_line(f"VAR_DECL({node.var_type} {node.name})")
        if node.value:
            self._visit_children([node.value], ["value"])
    
    def visit_assignment(self, node: Assignment):
        self._add_line(f"ASSIGN({node.name})")
        self._visit_children([node.value], ["value"])
    
    def visit_print_statement(self, node: PrintStatement):
        self._add_line("PRINT")
        self._visit_children([node.expression], ["expr"])
    
    def visit_if_statement(self, node: IfStatement):
        self._add_line("IF")
        
        # Add condition
        self.current_depth += 1
        condition_prefix = self._get_prefix(False)
        self.tree_lines.append(condition_prefix + "condition:")
        self.current_depth += 1
        self.visit(node.condition)
        self.current_depth -= 1
        
        # Add then branch
        then_prefix = self._get_prefix(node.else_statements is None)
        self.tree_lines.append(then_prefix + "then:")
        self.current_depth += 1
        for i, stmt in enumerate(node.then_statements):
            self.visit(stmt)
        self.current_depth -= 1
        
        # Add else branch if present
        if node.else_statements:
            else_prefix = self._get_prefix(True)
            self.tree_lines.append(else_prefix + "else:")
            self.current_depth += 1
            for stmt in node.else_statements:
                self.visit(stmt)
            self.current_depth -= 1
        
        self.current_depth -= 1
    
    def visit_while_statement(self, node: WhileStatement):
        self._add_line("WHILE")
        
        # Add condition
        self.current_depth += 1
        condition_prefix = self._get_prefix(False)
        self.tree_lines.append(condition_prefix + "condition:")
        self.current_depth += 1
        self.visit(node.condition)
        self.current_depth -= 1
        
        # Add body
        body_prefix = self._get_prefix(True)
        self.tree_lines.append(body_prefix + "body:")
        self.current_depth += 1
        for stmt in node.body:
            self.visit(stmt)
        self.current_depth -= 1
        
        self.current_depth -= 1
    
    def visit_block(self, node: Block):
        self._add_line("BLOCK")
        self._visit_children(node.statements)
    
    def visit_binary_op(self, node: BinaryOp):
        self._add_line(f"BINARY_OP({node.operator})")
        self._visit_children([node.left, node.right], ["left", "right"])
    
    def visit_unary_op(self, node: UnaryOp):
        self._add_line(f"UNARY_OP({node.operator})")
        self._visit_children([node.operand], ["operand"])
    
    def visit_identifier(self, node: Identifier):
        self._add_line(f"IDENTIFIER({node.name})")
    
    def visit_integer_literal(self, node: IntegerLiteral):
        self._add_line(f"INT({node.value})")
    
    def visit_float_literal(self, node: FloatLiteral):
        self._add_line(f"FLOAT({node.value})")
    
    def visit_boolean_literal(self, node: BooleanLiteral):
        self._add_line(f"BOOL({node.value})")
    
    def visit(self, node: ASTNode):
        """Generic visit method that dispatches to specific visit methods."""
        method_name = f"visit_{node.__class__.__name__.lower()}"
        method_name = method_name.replace('literal', '_literal')
        method_name = method_name.replace('statement', '_statement')
        method_name = method_name.replace('declaration', '_declaration')
        method_name = method_name.replace('binaryop', 'binary_op')
        method_name = method_name.replace('unaryop', 'unary_op')
        
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            raise Exception(f"No visit method for {node.__class__.__name__}")

def print_ast_tree(ast: Program):
    """Print the AST as a tree structure."""
    visualizer = TreeVisualizer()
    visualizer.visit(ast)
    print(visualizer.get_tree_string())

# Test the visualizer
if __name__ == "__main__":
    from scanner import Scanner
    from parser import Parser
    
    test_code = '''
    int a = 10;
    if (a > 5) {
        print(a);
    }
    '''
    
    scanner = Scanner(test_code)
    tokens = scanner.tokenize()
    
    if tokens:
        parser = Parser(tokens)
        ast = parser.parse()
        
        if ast:
            print("AST Tree Structure:")
            print("=" * 50)
            print_ast_tree(ast)