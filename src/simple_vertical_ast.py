"""
Simple Vertical AST Tree Visualizer for MiniLang compiler.
Creates top-down tree-like visual representation.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

from ast_nodes import *

class SimpleVerticalTreeVisualizer:
    """Simple vertical tree visualizer."""
    
    def __init__(self):
        self.output = []
        self.level = 0
    
    def _get_indent(self, level):
        """Get indentation for a given level."""
        return "    " * level
    
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
            return f"BINARY_OP({node.operator})"
        elif isinstance(node, UnaryOp):
            return f"UNARY_OP({node.operator})"
        elif isinstance(node, Identifier):
            return f"ID({node.name})"
        elif isinstance(node, IntegerLiteral):
            return f"INT({node.value})"
        elif isinstance(node, FloatLiteral):
            return f"FLOAT({node.value})"
        elif isinstance(node, BooleanLiteral):
            return f"BOOL({node.value})"
        else:
            return node.__class__.__name__
    
    def _draw_node(self, node, level=0):
        """Draw a single node with box."""
        indent = self._get_indent(level)
        name = self._get_node_name(node)
        
        # Create box
        box_width = max(len(name) + 4, 12)
        padding = (box_width - len(name) - 2) // 2
        
        top_line = indent + "┌" + "─" * (box_width - 2) + "┐"
        middle_line = indent + "│" + " " * padding + name + " " * (box_width - len(name) - padding - 2) + "│"
        bottom_line = indent + "└" + "─" * (box_width - 2) + "┘"
        
        self.output.append(top_line)
        self.output.append(middle_line)
        self.output.append(bottom_line)
        
        return box_width
    
    def _draw_connections(self, num_children, level, parent_width):
        """Draw connection lines to children."""
        if num_children == 0:
            return
        
        indent = self._get_indent(level)
        parent_center = parent_width // 2
        
        # Draw vertical line down from parent
        self.output.append(indent + " " * parent_center + "│")
        
        if num_children == 1:
            # Single child - straight down
            self.output.append(indent + " " * parent_center + "│")
        else:
            # Multiple children - spread horizontally
            line = indent + " " * parent_center
            
            # Calculate positions for children
            child_spacing = 15  # Space between children
            total_width = (num_children - 1) * child_spacing
            start_pos = parent_center - total_width // 2
            
            # Draw horizontal connector
            connector_line = [" "] * (start_pos + total_width + 10)
            
            for i in range(num_children):
                child_pos = start_pos + i * child_spacing
                if child_pos < parent_center:
                    for j in range(child_pos, parent_center + 1):
                        connector_line[j] = "─"
                    connector_line[child_pos] = "┌"
                elif child_pos > parent_center:
                    for j in range(parent_center, child_pos + 1):
                        connector_line[j] = "─"
                    connector_line[child_pos] = "┐"
                else:
                    connector_line[child_pos] = "┼"
            
            connector_line[parent_center] = "┼"
            self.output.append(indent + "".join(connector_line[:parent_center + total_width + 5]))
            
            # Draw vertical lines to children
            vertical_line = [" "] * (start_pos + total_width + 10)
            for i in range(num_children):
                child_pos = start_pos + i * child_spacing
                vertical_line[child_pos] = "│"
            
            self.output.append(indent + "".join(vertical_line[:parent_center + total_width + 5]))
    
    def print_tree(self, node, level=0):
        """Recursively print the tree."""
        # Draw current node
        node_width = self._draw_node(node, level)
        
        # Get children
        children = self._get_children(node)
        
        if children:
            # Draw connections
            self._draw_connections(len(children), level, node_width)
            
            # Draw children
            for child in children:
                self.output.append("")  # Empty line between levels
                self.print_tree(child, level + 1)
    
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
            # Create pseudo-nodes for then/else branches
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
    
    def visualize(self, ast):
        """Main method to visualize AST."""
        self.output = []
        self.level = 0
        
        print("\n" + "=" * 80)
        print("Abstract Syntax Tree (Vertical Layout)")
        print("=" * 80)
        
        self.print_tree(ast)
        
        for line in self.output:
            print(line)
        
        print("=" * 80)

def print_simple_vertical_ast(ast):
    """Print AST using simple vertical layout."""
    visualizer = SimpleVerticalTreeVisualizer()
    visualizer.visualize(ast)