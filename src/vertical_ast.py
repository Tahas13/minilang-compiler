"""
Vertical AST Tree Visualizer for MiniLang compiler.
Creates vertical tree-like visual representation similar to parse trees.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

from ast_nodes import *
from typing import List, Tuple

class VerticalTreeVisualizer(ASTVisitor):
    """Visitor that creates a vertical tree-like visual representation of the AST."""
    
    def __init__(self):
        self.lines = []
        self.node_width = 12  # Width of each node box
        self.level_height = 3  # Height between levels
    
    def _create_node_box(self, text: str, width: int = None) -> List[str]:
        """Create a visual box for a node."""
        if width is None:
            width = max(self.node_width, len(text) + 2)
        
        # Ensure text fits in box
        if len(text) > width - 2:
            text = text[:width-5] + "..."
        
        padding = (width - len(text)) // 2
        
        top = "┌" + "─" * (width - 2) + "┐"
        middle = "│" + " " * padding + text + " " * (width - len(text) - padding - 2) + "│"
        bottom = "└" + "─" * (width - 2) + "┘"
        
        return [top, middle, bottom]
    
    def _get_node_info(self, node: ASTNode) -> str:
        """Get display text for a node."""
        if isinstance(node, Program):
            return "PROGRAM"
        elif isinstance(node, VarDeclaration):
            return f"{node.var_type} {node.name}"
        elif isinstance(node, Assignment):
            return f"= {node.name}"
        elif isinstance(node, PrintStatement):
            return "PRINT"
        elif isinstance(node, IfStatement):
            return "IF"
        elif isinstance(node, WhileStatement):
            return "WHILE"
        elif isinstance(node, Block):
            return "BLOCK"
        elif isinstance(node, BinaryOp):
            return f"OP({node.operator})"
        elif isinstance(node, UnaryOp):
            return f"UN({node.operator})"
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
    
    def _draw_connections(self, parent_x: int, children_positions: List[int], level: int) -> List[str]:
        """Draw connection lines from parent to children."""
        if not children_positions:
            return []
        
        lines = []
        
        # Calculate the span
        leftmost = min(children_positions)
        rightmost = max(children_positions)
        
        # Draw vertical line down from parent
        line1 = " " * parent_x + "│"
        lines.append(line1)
        
        if len(children_positions) == 1:
            # Single child - straight line
            child_x = children_positions[0]
            if child_x == parent_x:
                line2 = " " * parent_x + "│"
            elif child_x < parent_x:
                line2 = " " * child_x + "┌" + "─" * (parent_x - child_x - 1) + "┘"
            else:
                line2 = " " * parent_x + "└" + "─" * (child_x - parent_x - 1) + "┐"
            lines.append(line2)
        else:
            # Multiple children - horizontal line with branches
            horizontal_line = [" "] * (rightmost + 1)
            horizontal_line[parent_x] = "┼"
            
            for i, child_x in enumerate(children_positions):
                if child_x < parent_x:
                    for j in range(child_x, parent_x):
                        if horizontal_line[j] == " ":
                            horizontal_line[j] = "─"
                    horizontal_line[child_x] = "┌"
                elif child_x > parent_x:
                    for j in range(parent_x + 1, child_x + 1):
                        if horizontal_line[j] == " ":
                            horizontal_line[j] = "─"
                    horizontal_line[child_x] = "┐"
                else:
                    horizontal_line[child_x] = "┼"
            
            lines.append("".join(horizontal_line))
            
            # Draw vertical lines to children
            vertical_line = [" "] * (rightmost + 1)
            for child_x in children_positions:
                vertical_line[child_x] = "│"
            lines.append("".join(vertical_line))
        
        return lines
    
    def _layout_nodes(self, node: ASTNode, x_offset: int = 0) -> Tuple[List[str], int, List[int]]:
        """Layout nodes and return (lines, width, child_positions)."""
        node_text = self._get_node_info(node)
        node_box = self._create_node_box(node_text)
        node_width = len(node_box[0])
        
        # Get children
        children = self._get_children(node)
        
        if not children:
            # Leaf node
            positioned_box = []
            for line in node_box:
                positioned_box.append(" " * x_offset + line)
            return positioned_box, x_offset + node_width, [x_offset + node_width // 2]
        
        # Layout children
        child_layouts = []
        child_positions = []
        current_x = x_offset
        total_width = 0
        
        for child in children:
            child_lines, child_width, child_pos = self._layout_nodes(child, current_x)
            child_layouts.append(child_lines)
            child_positions.extend(child_pos)
            current_x = child_width + 2  # 2 spaces between children
            total_width = current_x
        
        # Position parent node centered above children
        children_span = child_positions[-1] - child_positions[0] if child_positions else 0
        parent_x = child_positions[0] + children_span // 2 - node_width // 2
        parent_center = parent_x + node_width // 2
        
        # Create final layout
        result_lines = []
        
        # Add parent node
        for line in node_box:
            result_lines.append(" " * parent_x + line)
        
        # Add connection lines
        connections = self._draw_connections(parent_center, child_positions, 0)
        result_lines.extend(connections)
        
        # Add children (find max height)
        max_child_height = max(len(layout) for layout in child_layouts) if child_layouts else 0
        
        for i in range(max_child_height):
            line = ""
            for layout in child_layouts:
                if i < len(layout):
                    # Pad line to maintain alignment
                    current_len = len(line)
                    needed_padding = layout[i].find(layout[i].lstrip()) - current_len
                    if needed_padding > 0:
                        line += " " * needed_padding
                    line += layout[i].lstrip()
                else:
                    # Child layout doesn't have this line
                    pass
            result_lines.append(line)
        
        return result_lines, total_width, [parent_center]
    
    def _get_children(self, node: ASTNode) -> List[ASTNode]:
        """Get child nodes for a given node."""
        children = []
        
        if isinstance(node, Program):
            return node.statements
        elif isinstance(node, VarDeclaration):
            if node.value:
                children.append(node.value)
        elif isinstance(node, Assignment):
            children.append(node.value)
        elif isinstance(node, PrintStatement):
            children.append(node.expression)
        elif isinstance(node, IfStatement):
            children.append(node.condition)
            if node.then_statements:
                for stmt in node.then_statements:
                    children.append(stmt)
            if node.else_statements:
                for stmt in node.else_statements:
                    children.append(stmt)
        elif isinstance(node, WhileStatement):
            children.append(node.condition)
            for stmt in node.body:
                children.append(stmt)
        elif isinstance(node, Block):
            return node.statements
        elif isinstance(node, BinaryOp):
            children.extend([node.left, node.right])
        elif isinstance(node, UnaryOp):
            children.append(node.operand)
        
        return children
    
    def print_tree(self, ast: Program):
        """Print the AST as a vertical tree."""
        lines, width, positions = self._layout_nodes(ast)
        
        print("\n" + "=" * 60)
        print("Abstract Syntax Tree (Vertical Layout)")
        print("=" * 60)
        
        for line in lines:
            print(line)
        
        print("=" * 60)
    
    # Implement required visitor methods (not used in this implementation)
    def visit_program(self, node: Program): pass
    def visit_var_declaration(self, node: VarDeclaration): pass
    def visit_assignment(self, node: Assignment): pass
    def visit_print_statement(self, node: PrintStatement): pass
    def visit_if_statement(self, node: IfStatement): pass
    def visit_while_statement(self, node: WhileStatement): pass
    def visit_block(self, node: Block): pass
    def visit_binary_op(self, node: BinaryOp): pass
    def visit_unary_op(self, node: UnaryOp): pass
    def visit_identifier(self, node: Identifier): pass
    def visit_integer_literal(self, node: IntegerLiteral): pass
    def visit_float_literal(self, node: FloatLiteral): pass
    def visit_boolean_literal(self, node: BooleanLiteral): pass
    def visit(self, node: ASTNode): pass

def print_vertical_ast_tree(ast: Program):
    """Print the AST as a vertical tree structure."""
    visualizer = VerticalTreeVisualizer()
    visualizer.print_tree(ast)

# Test the vertical visualizer
if __name__ == "__main__":
    from scanner import Scanner
    from parser import Parser
    
    test_code = '''
    int x = 5;
    x = x + 1;
    print(x);
    '''
    
    scanner = Scanner(test_code)
    tokens = scanner.tokenize()
    
    if tokens:
        parser = Parser(tokens)
        ast = parser.parse()
        
        if ast:
            print_vertical_ast_tree(ast)