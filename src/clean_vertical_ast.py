"""
Clean Vertical AST Tree Visualizer for MiniLang compiler.
Creates clean top-down tree-like visual representation like parse trees.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

from ast_nodes import *

class CleanVerticalTreeVisualizer:
    """Clean vertical tree visualizer similar to parse trees."""
    
    def __init__(self):
        self.output = []
    
    def _get_node_name(self, node):
        """Get display name for a node."""
        if isinstance(node, Program):
            return "PROGRAM"
        elif isinstance(node, VarDeclaration):
            return f"VAR_DECL"
        elif isinstance(node, Assignment):
            return f"ASSIGN"
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
    
    def _get_node_details(self, node):
        """Get additional details for a node."""
        if isinstance(node, VarDeclaration):
            return f"({node.var_type} {node.name})"
        elif isinstance(node, Assignment):
            return f"({node.name})"
        else:
            return ""
    
    def _create_simple_tree(self, node, level=0, is_last=True, prefix=""):
        """Create a clean vertical tree representation."""
        # Get node display info
        name = self._get_node_name(node)
        details = self._get_node_details(node)
        full_name = name + details
        
        # Create the line for this node with proper alignment
        if level == 0:
            # Root node - center it
            line = full_name
        else:
            # Child nodes - use tree connectors
            if is_last:
                connector = "└── "
                child_prefix_addition = "    "
            else:
                connector = "├── "
                child_prefix_addition = "│   "
            line = prefix + connector + full_name
        
        self.output.append(line)
        
        # Get children
        children = self._get_children(node)
        
        if children:
            # Prepare prefix for children
            if level == 0:
                child_prefix = ""
            else:
                child_prefix = prefix + child_prefix_addition
            
            # Process children
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                self._create_simple_tree(child, level + 1, is_last_child, child_prefix)
    
    def _create_boxed_tree(self, node, level=0):
        """Create a boxed tree representation."""
        indent = "    " * level
        name = self._get_node_name(node)
        details = self._get_node_details(node)
        full_name = name + details
        
        # Create box
        box_width = max(len(full_name) + 4, 12)
        padding = (box_width - len(full_name) - 2) // 2
        
        top_line = indent + "┌" + "─" * (box_width - 2) + "┐"
        middle_line = indent + "│" + " " * padding + full_name + " " * (box_width - len(full_name) - padding - 2) + "│"
        bottom_line = indent + "└" + "─" * (box_width - 2) + "┘"
        
        self.output.append(top_line)
        self.output.append(middle_line) 
        self.output.append(bottom_line)
        
        # Get children
        children = self._get_children(node)
        
        if children:
            # Add vertical connector
            connector_pos = box_width // 2
            self.output.append(indent + " " * connector_pos + "│")
            
            # Add horizontal line if multiple children
            if len(children) > 1:
                # Calculate positions
                total_children_width = sum(max(len(self._get_node_name(child) + self._get_node_details(child)) + 4, 12) for child in children)
                spacing = max(4, (80 - total_children_width) // len(children))
                
                horizontal_line = indent + " " * connector_pos + "┼"
                for i in range(len(children) - 1):
                    horizontal_line += "─" * spacing + "┬"
                
                self.output.append(horizontal_line)
                self.output.append(indent + " " * connector_pos + "│" + "│" * (len(horizontal_line) - len(indent) - connector_pos - 1))
            else:
                self.output.append(indent + " " * connector_pos + "│")
            
            # Process children
            for child in children:
                self.output.append("")  # Add spacing
                self._create_boxed_tree(child, level + 1)
    
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
    
    def visualize_simple(self, ast):
        """Create simple tree visualization."""
        self.output = []
        
        print("\n" + "=" * 60)
        print("Abstract Syntax Tree")
        print("=" * 60)
        print()
        
        self._create_simple_tree(ast)
        
        for line in self.output:
            print(line)
        
        print("\n" + "=" * 60)
    
    def visualize_boxed(self, ast):
        """Create boxed tree visualization."""
        self.output = []
        
        print("\n" + "=" * 60)
        print("Abstract Syntax Tree (Boxed Tree)")
        print("=" * 60)
        
        self._create_boxed_tree(ast)
        
        for line in self.output:
            print(line)
        
        print("=" * 60)

def print_clean_vertical_ast(ast, style="simple"):
    """Print AST using clean vertical layout."""
    visualizer = CleanVerticalTreeVisualizer()
    
    if style == "boxed":
        visualizer.visualize_boxed(ast)
    else:
        visualizer.visualize_simple(ast)