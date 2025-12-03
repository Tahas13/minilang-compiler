"""
Web-optimized AST Tree Visualizer for MiniLang compiler.
Creates clean, properly formatted vertical trees for web display.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

from ast_nodes import *

class WebTreeVisualizer:
    """Clean tree visualizer optimized for web display."""
    
    def __init__(self):
        self.lines = []
    
    def _get_node_name(self, node):
        """Get display name for a node."""
        if isinstance(node, Program):
            return "PROGRAM"
        elif isinstance(node, VarDeclaration):
            return f"VAR_DECL({node.var_type} {node.name})"
        elif isinstance(node, Assignment):
            return f"ASSIGN({node.name})"
        elif isinstance(node, PrintStatement):
            return "PRINT"
        elif isinstance(node, IfStatement):
            return "IF"
        elif isinstance(node, WhileStatement):
            return "WHILE" 
        elif isinstance(node, Block):
            return "BLOCK"
        elif isinstance(node, BinaryOp):
            return f"EXPR({node.operator})"
        elif isinstance(node, UnaryOp):
            return f"UNARY({node.operator})"
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, IntegerLiteral):
            return str(node.value)
        elif isinstance(node, FloatLiteral):
            return str(node.value)
        elif isinstance(node, BooleanLiteral):
            return str(node.value)
        else:
            return node.__class__.__name__
    
    def _build_tree(self, node, level=0, is_last=True, prefix=""):
        """Build tree recursively."""
        name = self._get_node_name(node)
        
        # Create the line for this node
        if level == 0:
            # Root node
            line = name
        else:
            # Child nodes
            connector = "└── " if is_last else "├── "
            line = prefix + connector + name
        
        self.lines.append(line)
        
        # Get children
        children = self._get_children(node)
        
        if children:
            # Calculate new prefix for children
            if level == 0:
                new_prefix = ""
            else:
                new_prefix = prefix + ("    " if is_last else "│   ")
            
            # Process each child
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                self._build_tree(child, level + 1, is_last_child, new_prefix)
    
    def _get_children(self, node):
        """Get child nodes."""
        if isinstance(node, Program):
            return node.statements
        elif isinstance(node, VarDeclaration):
            return [node.value] if node.value else []
        elif isinstance(node, Assignment):
            return [node.value]
        elif isinstance(node, PrintStatement):
            return [node.expression]
        elif isinstance(node, IfStatement):
            children = [node.condition]
            if node.then_statements:
                children.extend(node.then_statements)
            if node.else_statements:
                children.extend(node.else_statements)
            return children
        elif isinstance(node, WhileStatement):
            children = [node.condition]
            children.extend(node.body)
            return children
        elif isinstance(node, Block):
            return node.statements
        elif isinstance(node, BinaryOp):
            return [node.left, node.right]
        elif isinstance(node, UnaryOp):
            return [node.operand]
        else:
            return []
    
    def get_tree_string(self, ast):
        """Get the tree as a clean string."""
        self.lines = []
        self._build_tree(ast)
        return "\n".join(self.lines)

def get_web_ast_string(ast):
    """Get AST as clean string for web display."""
    visualizer = WebTreeVisualizer()
    return visualizer.get_tree_string(ast)