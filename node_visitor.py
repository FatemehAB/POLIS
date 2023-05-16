from ast import *
from _ast import If, IfExp
from typing import Any
import DSL
import BUS

FILENAME = 'pilot2-versions/pilot2_h_5.py'


class AnalysisNodeVisitor(NodeVisitor):

    def visit_Module(self, node: Module) -> Any:
        body = node.body
        v = self.generic_visit(node)
        for i in range(len(body)):
            if isinstance(body[i], FunctionDef) and body[i].name == "heuristic":
                print(v[i])
                return v[i]
        raise Exception("There is no heuristic function in this file")

    def visit_If(self, node: If) -> Any:
        print('If')
        #print(condition.toString())
        if_else = self.generic_visit(node)
        condition = if_else.pop(0)
        true_cases = if_else[:len(node.body)]
        false_cases = if_else[-len(node.orelse):]
        if len(node.orelse) == 0:
            raise Exception("Please include else.")
        return DSL_PCFG.Att_Ite(condition, true_cases, false_cases)

    def visit_Return(self, node: Return) -> Any:
        r = self.generic_visit(node)
        if len(r) != 1:
            raise Exception("Please return action variable.")
        if r[0] != 'action':
            raise Exception("Please return action variable.")

    def visit_IfExp(self, node: IfExp) -> Any:
        print('IfExp')
        self.generic_visit(node)

    def visit_Assign(self, node):
        print('Node type: Assign and fields: ', node._fields)
        v = self.generic_visit(node)
        #print(v)
        if len(v) > 2:
            raise Exception("Please define one var per each line")
        if v[0] == "action":
            return DSL_PCFG.AssignAction(v[1])
        if isinstance(v[1], DSL_PCFG.Node):
            prog = v[1]
        else:
            if isinstance(v[1], str):
                prog = DSL_PCFG.Variable(v[1])
            elif isinstance(v[1], (int, float)):
                prog = DSL_PCFG.Num(v[1])
            else:
                raise Exception("Please assign a valid expression to the variable")
        return DSL_PCFG.Att_Var(v[0], prog)



    def visit_BoolOp(self, node: BoolOp) -> Any:
        print('Node type: BoolOp and fields: ', node._fields)
        values = self.generic_visit(node)[1:]
        print(node.op)
        left = values.pop(0)
        while len(values) != 0:
            right = values.pop(0)
            if isinstance(node.op, Or):
                left = DSL_PCFG.Or(left, right)
            elif isinstance(node.op, And):
                left = DSL_PCFG.And(left, right)
            else:
                raise Exception("Please use valid Boolean operations")
        return left
        #self.generic_visit(node)

    def visit_BinOp(self, node: BinOp) -> Any:
        print('Node type: BinOp and fields: ', node._fields)
        v = self.generic_visit(node)
        if isinstance(v[0], DSL_PCFG.Node):
            left = v[0]
        else:
            if isinstance(v[0], str):
                left = DSL_PCFG.Variable(v[0])
            else:
                left = DSL_PCFG.Num(v[0])

        if isinstance(v[2], DSL_PCFG.Node):
            right = v[2]
        else:
            if isinstance(v[2], str):
                right = DSL_PCFG.Variable(v[2])
            else:
                right = DSL_PCFG.Num(v[2])

        if isinstance(node.op, Add):
            prog = DSL_PCFG.Addition(left, right)
        elif isinstance(node.op, Sub):
            prog = DSL_PCFG.Subtraction(left, right)
        elif isinstance(node.op, Mult):
            prog = DSL_PCFG.Multiplication(left, right)
        elif isinstance(node.op, Div):
            prog = DSL_PCFG.Division(left, right)
        elif isinstance(node.op, Pow):
            prog = DSL_PCFG.Exp(left, right)
        else:
            raise Exception("Invalid Binary Operation")
        return prog

    def visit_UnaryOp(self, node: UnaryOp) -> Any:
        v = self.generic_visit(node)
        if isinstance(node.op, USub):
            if isinstance(v[1], DSL_PCFG.Node):
                return DSL_PCFG.Neg(v[1])
            else:
                if isinstance(v[1], str):
                    return DSL_PCFG.Neg(DSL_PCFG.Variable(v[1]))
                else:
                    return DSL_PCFG.Neg(DSL_PCFG.Num(v[1]))
        raise Exception("Invalid Unary operation")

    def visit_Compare(self, node: Compare) -> Any:
        print('Node type: Compare and fields: ', node._fields)
        if len(node.ops) !=1 :
            raise Exception("Please use binary comparator")
        v = self.generic_visit(node)
        if isinstance(v[0], DSL_PCFG.Node):
            left = v[0]
        else:
            if isinstance(v[0], str):
                left = DSL_PCFG.Variable(v[0])
            else:
                left = DSL_PCFG.Num(v[0])
        if isinstance(v[2], DSL_PCFG.Node):
            right = v[2]
        else:
            if isinstance(v[2], str):
                right = DSL_PCFG.Variable(v[2])
            else:
                right = DSL_PCFG.Num(v[2])
        op = node.ops[0]
        if isinstance(op, Gt):
            prog = DSL_PCFG.Gt(left, right)
        elif isinstance(op,Lt):
            prog = DSL_PCFG.Lt(left, right)
        elif isinstance(op, Eq):
            prog = DSL_PCFG.Equal(left, right)
        elif isinstance(op, LtE):
            prog = DSL_PCFG.Lt_Eq(left, right)
        elif isinstance(op, GtE):
            prog = DSL_PCFG.Gt_Eq(left, right)
        elif isinstance(op, NotEq):
            prog = DSL_PCFG.NotEqual(left, right)
        else:
            raise Exception("Invalid Compare")
        return prog

    def visit_Call(self, node: Call) -> Any:
        print('Node type: Call and fields: ', node._fields)
        v = self.generic_visit(node)
        if isinstance(v[1], DSL_PCFG.Node):
            param = v[1]
        else:
            if isinstance(v[1], str):
                param = DSL_PCFG.Variable(v[1])
            else:
                param = DSL_PCFG.Num(v[1])
        if v[0] == "abs":
            prog = DSL_PCFG.Abs(param)
        elif v[0] == "neg":
            prog = DSL_PCFG.Neg(param)
        elif v[0] == "sqrt":
            prog = DSL_PCFG.Sqrt(param)
        elif v[0]== "log":
            prog = DSL_PCFG.Log(param)
        else:
            raise Exception("Please use valid function")
        return prog

    def visit_Subscript(self, node: Subscript) -> Any:
        v = self.generic_visit(node)
        if v[0] == 's':
            if isinstance(v[1][0], int):
                obs = DSL_PCFG.Observation(v[1][0])
                return obs
            else:
                raise Exception("Invalid index.")
        else:
            raise Exception("Do not define any lists other than 's'.")

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        list_return = []
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        list_return.append(self.visit(item))
            elif isinstance(value, AST):
                list_return.append(self.visit(value))
        return list_return

    # def generic_visit(self, node):
    #   print(type(node).__name__)
    #   super(AnalysisNodeVisitor, self).generic_visit(node)
    #
    # def visit_BinOp(self, node):
    #   print('Node type: BinOp and fields: ', node._fields)
    #   self.generic_visit(node)
    #
    # def visit_Expr(self, node):
    #   print('Node type: Expr and fields: ', node._fields)
    #   self.generic_visit(node)
    #
    def visit_Num(self, node):
        #print('Node type: Num and fields: ', node._fields)
        return node.n

    def visit_Name(self, node):
        #print('Node type: Name and fields: ', node._fields)
        return node.id

    def visit_Index(self, node: Index) -> Any:
        #print('Node type: Index and fields: ', node._fields)
        i = self.generic_visit(node)
        return i

    def visit_Str(self, node):
        #print('Node type: Str and fields: ', node._fields)
        return node


def main():
    with open(FILENAME) as f:
        tree = parse(f.read())
    v = AnalysisNodeVisitor()
    program = v.visit(tree)
    atts = []
    for p in program:
        if isinstance(p, DSL_PCFG.Node):
            atts.append(p)
    heu = BUS.Function(atts, [], [])
    print(heu.to_string())
    print(heu.evaluate(1, env_name="highway-fast-v0"))
    #print(program)


if __name__ == '__main__':
    main()
