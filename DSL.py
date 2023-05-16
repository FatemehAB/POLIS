import itertools
import math

class Node:
    def __init__(self):
        self.size = 0
        self.pcfg = False

    def get_size(self):
        return self.size

    def to_string(self):
        raise Exception('Unimplemented method: toString')

    def interpret(self):
        raise Exception('Unimplemented method: interpret')

    def set_ID(self):
        pass

    def grow(self, plist, new_plist):
        pass

    def __gt__(self, other):
        if self.size < other.get_size():
            return True
        return False

    @classmethod
    def name(cls):
        return cls.__name__


class Ite(Node):
    def __init__(self, condition, true_case, false_case):
        self.condition = condition
        self.true_case = true_case
        self.false_case = false_case
        self.size = condition.get_size() + true_case.get_size() + false_case.get_size()
        self.size += 1

    def to_string(self):
        return "(if " + self.condition.to_string() + " then " + self.true_case.to_string() + " else " + self.false_case.to_string() + ")"

    def interpret(self, env):
        if self.condition.interpret(env):
            return self.true_case.interpret(env)
        else:
            return self.false_case.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Ite:
            return False
        if self.condition == other.condition and self.true_case == other.true_case and self.false_case == other.false_case:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines the set of nodes accepted as conditions for an Ite
        accepted_condition_nodes = set([Lt.name(), Or.name(), Gt.name(), Observation.name(), And.name(), Equal.name(), Lt_Eq.name(), Gt_Eq.name()])
        # defines the set of nodes accepted as cases for an Ite
        accepted_case_nodes = set([AssignAction.name(), Ite.name()])

        combinations = list(itertools.product(range(1, size - 1), repeat=3))

        for c in combinations:

            c_size = c[0] + c[1] + c[2] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
            program_set3 = plist.get_programs(c[2])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted as a condition node for Ite
                if t1 not in accepted_condition_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t2 isn't a case node
                        if t2 not in accepted_case_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            for t3, programs3 in program_set3.items():
                                # skip if t3 isn't a case node
                                if t3 not in accepted_case_nodes:
                                    continue

                                # produces a new program with Ite, p1, p2, and p3
                                for p3 in programs3:
                                    if p2 == p3: continue
                                    ite = Ite(p1, p2, p3)
                                    new_programs.append(ite)

                                    yield ite
        return new_programs


class Lt(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " < " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) < self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Lt:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        left_accepted_nodes = set(
            [Observation.name(), Addition.name(), Multiplication.name(), Subtraction.name(), Abs.name(),
             Variable.name(), Sqrt.name(), Log.name(), Exp.name(), Division.name()])
        right_accepted_nodes = set([Num.name()])
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in left_accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in right_accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            lt = Lt(p1, p2)
                            new_programs.append(lt)

                            yield lt
        return new_programs


class Lt_Eq(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " <= " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) <= self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Lt_Eq:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        left_accepted_nodes = set(
            [Observation.name(), Addition.name(), Multiplication.name(), Subtraction.name(), Abs.name(),
             Variable.name(), Sqrt.name(), Log.name(), Exp.name(), Division.name()])
        right_accepted_nodes = set([Num.name()])
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in left_accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in right_accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            lt = Lt_Eq(p1, p2)
                            new_programs.append(lt)

                            yield lt
        return new_programs


class Gt(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " > " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) > self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Gt:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        left_accepted_nodes = set(
            [Observation.name(), Addition.name(), Multiplication.name(), Subtraction.name(), Abs.name(),
             Variable.name(), Sqrt.name(), Log.name(), Exp.name(), Division.name()])
        right_accepted_nodes = set([Num.name()])
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in left_accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in right_accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            gt = Gt(p1, p2)
                            new_programs.append(gt)

                            yield gt
        return new_programs


class Gt_Eq(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " >= " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) >= self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Gt_Eq:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        left_accepted_nodes = set(
            [Observation.name(), Addition.name(), Multiplication.name(), Subtraction.name(), Abs.name(),
             Variable.name(), Sqrt.name(), Log.name(), Exp.name(), Division.name()])
        right_accepted_nodes = set([Num.name()])
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in left_accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in right_accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            gt = Gt_Eq(p1, p2)
                            new_programs.append(gt)

                            yield gt
        return new_programs


class Equal(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " == " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) == self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Equal:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        if self.right == other.left and self.left == other.right:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        left_accepted_nodes = set(
            [Observation.name(), Addition.name(), Multiplication.name(), Subtraction.name(), Abs.name(),
             Variable.name(), Sqrt.name(), Log.name(), Exp.name(), Division.name()])
        right_accepted_nodes = set(
            [Num.name(), Multiplication.name(), Division.name(), Log.name(), Sqrt.name(), Exp.name(), Variable.name(), Observation.name()])
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in left_accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in right_accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            if p1 == p2:
                                continue
                            eq = Equal(p1, p2)
                            new_programs.append(eq)

                            yield eq
        return new_programs


class NotEqual(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " != " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) != self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != NotEqual:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        if self.right == other.left and self.left == other.right:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        left_accepted_nodes = set(
            [Observation.name(), Addition.name(), Multiplication.name(), Subtraction.name(), Abs.name(),
             Variable.name(), Sqrt.name(), Log.name(), Exp.name(), Division.name()])
        right_accepted_nodes = set(
            [Num.name(), Multiplication.name(), Division.name(), Log.name(), Sqrt.name(), Exp.name(), Variable.name(), Observation.name()])
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in left_accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in right_accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            if p1 == p2:
                                continue
                            neq = NotEqual(p1, p2)
                            new_programs.append(neq)

                            yield neq
        return new_programs


class Or(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " or " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) or self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Or:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        if self.left == other.right and self.right == other.left:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        accepted_nodes = set([Observation.name(), Lt.name(), Gt.name(), Or.name(), Equal.name(), And.name(), Lt_Eq.name(), Gt_Eq.name()])

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if p1 == p2:
                                continue
                            o = Or(p1, p2)
                            new_programs.append(o)

                            yield o
        return new_programs


class And(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " and " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) and self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != And:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        if self.left == other.right and self.right == other.left:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        accepted_nodes = set([Observation.name(), Lt.name(), Gt.name(), Or.name(), And.name(), Equal.name(), Lt_Eq.name(), Gt_Eq.name()])

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a node accepted by Lt
                        if t2 not in accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if p1 == p2:
                                continue
                            o = And(p1, p2)
                            new_programs.append(o)

                            yield o
        return new_programs


class Addition(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1


    def to_string(self):
        return "(" + self.left.to_string() + " + " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) + self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Addition:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        if self.left == other.right and self.right == other.left:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        accepted_nodes = set(
            [Num.name(), Observation.name(), Abs.name(), Multiplication.name(), Addition.name(), Subtraction.name(),
             Variable.name(), Sqrt.name(), Log.name(), Exp.name(), Division.name()])

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))
        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a Node accepted by Lt
                if t1 not in accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a Node accepted
                        if t2 not in accepted_nodes:
                            continue
                        # skip if both sides are numbers
                        if (t1 == Num.name() and t2 == Num.name()):
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            st = Addition(p1, p2)
                            new_programs.append(st)

                            yield st
        return new_programs


class Subtraction(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " - " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) - self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Subtraction:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        accepted_nodes = set(
            [Num.name(), Observation.name(), Multiplication.name(), Addition.name(), Subtraction.name(), Abs.name(),
             Variable.name(), Sqrt.name(), Log.name(), Exp.name(), Division.name()])

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])
            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a Node accepted by Lt
                if t1 not in accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a Node accepted
                        if t2 not in accepted_nodes:
                            continue
                        #skip if both sides are numbers
                        if (t1 == Num.name() and t2 == Num.name()):
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if p1 == p2:
                                continue
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            if p1 == p2:
                                continue
                            st = Subtraction(p1, p2)
                            new_programs.append(st)

                            yield st

        return new_programs


class Multiplication(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " * " + self.right.to_string() + ")"

    def interpret(self, env):
        return self.left.interpret(env) * self.right.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Multiplication:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        if self.left == other.right and self.right == other.left:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        left_accepted_nodes = set(
            [Observation.name(), Addition.name(), Multiplication.name(), Subtraction.name(), Abs.name(),
             Variable.name(), Neg.name(), Sqrt.name(), Log.name(), Exp.name(), Division.name()])
        right_accepted_nodes = set([Num.name()])
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a Node accepted by Lt
                if t1 not in left_accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a Node accepted
                        if t2 not in right_accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            mp = Multiplication(p1, p2)
                            new_programs.append(mp)

                            yield mp
        return new_programs


class Division(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " / " + self.right.to_string() + ")"

    def interpret(self, env):
        try:
            return self.left.interpret(env) / self.right.interpret(env)
        except:
            return None

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Division:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        left_accepted_nodes = set([Variable.name(), Observation.name(), Num.name(), Sqrt.name(), Log.name()])
        right_accepted_nodes = set(
            [Observation.name(), Addition.name(), Multiplication.name(), Subtraction.name(), Abs.name(),
             Variable.name(), Neg.name(), Num.name(), Sqrt.name(), Log.name(), Exp.name()])
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a Node accepted by Lt
                if t1 not in left_accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a Node accepted
                        if t2 not in right_accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            # skip if the solution is 1
                            if p1 == p2:
                                continue
                            dv = Division(p1, p2)
                            new_programs.append(dv)

                            yield dv
        return new_programs


class Exp(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.size = left.get_size() + right.get_size()
        self.size += 1

    def to_string(self):
        return "(" + self.left.to_string() + " ** " + self.right.to_string() + ")"

    def interpret(self, env):
        return pow(self.left.interpret(env), int(self.right.interpret(env)))

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Exp:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        return False

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        left_accepted_nodes = set(
            [Observation.name(), Variable.name()])
        right_accepted_nodes = set([Num.name(), Variable.name()])
        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size - 1), repeat=2))

        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + c[1] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])
            program_set2 = plist.get_programs(c[1])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a Node accepted by Lt
                if t1 not in left_accepted_nodes:
                    continue

                for p1 in programs1:
                    for t2, programs2 in program_set2.items():
                        # skip if t1 isn't a Node accepted
                        if t2 not in right_accepted_nodes:
                            continue

                        # p1 and all programs in programs2 satisfy constraints; grow the list
                        for p2 in programs2:
                            if t1 == Num.name():
                                p1 = Num(p1.value)
                            elif t2 == Num.name():
                                p2 = Num(p2.value)
                            xp = Exp(p1, p2)
                            new_programs.append(xp)

                            yield xp
        return new_programs


class Abs(Node):
    def __init__(self, expr):
        self.expr = expr
        self.size = expr.get_size() + 1

    def to_string(self):
        return "abs(" + self.expr.to_string() + ")"

    def interpret(self, env):
        a = self.expr.interpret(env)
        if a > 0:
            return a
        return -a

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Abs:
            return False
        return self.expr == other.expr

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        accepted_nodes = set([Observation.name(), Variable.name()])

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size), repeat=1))
        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in accepted_nodes:
                    continue

                for p1 in programs1:
                    abs = Abs(p1)
                    new_programs.append(abs)

                    yield abs
        return new_programs


class Neg(Node):
    def __init__(self, expr):
        self.expr = expr
        self.size = expr.get_size() + 1

    def to_string(self):
        return "-(" + self.expr.to_string() + ")"

    def interpret(self, env):
        return -self.expr.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Neg:
            return False
        return self.expr == other.expr

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        accepted_nodes = set([Observation.name(), Variable.name()])

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size), repeat=1))
        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in accepted_nodes:
                    continue

                for p1 in programs1:
                    ng = Neg(p1)
                    new_programs.append(ng)

                    yield ng
        return new_programs


class Sqrt(Node):
    def __init__(self, expr):
        self.expr = expr
        self.size = expr.get_size() + 1

    def to_string(self):
        return "sqrt(" + self.expr.to_string() + ")"

    def interpret(self, env):
        return math.sqrt(self.expr.interpret(env))

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Sqrt:
            return False
        return self.expr == other.expr

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        accepted_nodes = set([Observation.name(), Variable.name()])

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size), repeat=1))
        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in accepted_nodes:
                    continue

                for p1 in programs1:
                    sq = Sqrt(p1)
                    new_programs.append(sq)

                    yield sq
        return new_programs


class Log(Node):
    def __init__(self, expr):
        self.expr = expr
        self.size = expr.get_size() + 1

    def to_string(self):
        return "log(" + self.expr.to_string() + ")"

    def interpret(self, env):
        try:
            return math.log(self.expr.interpret(env))
        except:
            return None

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Log:
            return False
        return self.expr == other.expr

    def grow(plist, size):
        new_programs = []
        # defines which nodes are accepted in the AST
        accepted_nodes = set([Observation.name(), Variable.name()])

        # generates all combinations of cost of size 2 varying from 1 to size - 1
        combinations = list(itertools.product(range(1, size), repeat=1))
        for c in combinations:
            # skip if the cost combination exceeds the limit
            c_size = c[0] + 1
            if c_size != size:
                continue

            # retrive bank of programs with costs c[0] and c[1]
            program_set1 = plist.get_programs(c[0])

            for t1, programs1 in program_set1.items():
                # skip if t1 isn't a node accepted by Lt
                if t1 not in accepted_nodes:
                    continue

                for p1 in programs1:
                    lg = Log(p1)
                    new_programs.append(lg)

                    yield lg
        return new_programs


class Num(Node):
    def __init__(self, value):
        self.value = value
        self.size = 1
        self.id = None

    def to_string(self):
        return str(self.value)

    def interpret(self, env):
        return self.value

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        return type(other) == Num and self.value == other.value and self.id == other.id

    def __str__(self):
        return 'ID: {}, Value: {}'.format(self.id, self.value)


class AssignAction(Node):
    def __init__(self, value):
        self.value = value
        self.size = 1

    def to_string(self):
        return 'act = ' + str(self.value)

    def interpret(self, env):
        env['act'] = self.value

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != AssignAction:
            return False
        if self.value == other.value:
            return True
        return False


class Observation(Node):
    def __init__(self, index):
        self.index = index
        self.size = 1

    def to_string(self):
        return 's[' + str(self.index) + ']'

    def interpret(self, env):
        return env['s'][self.index]

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Observation:
            return False
        if self.index == other.index:
            return True
        return False


class Variable(Node):
    def __init__(self, var):
        self.var = var
        self.size = 1

    def to_string(self):
        return self.var

    def interpret(self, env):
        return env[self.var]

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Variable:
            return False
        if self.var == other.var:
            return True
        return False


class Att_Var(Node):
    def __init__(self, name, p):
        self.var = name
        self.program = p
        self.size = p.size

    def to_string(self):
        return self.var + " = " + self.program.to_string()

    def interpret(self, env):
        env[self.var] = self.program.interpret(env)

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Att_Var:
            return False
        if self.var == other.var and self.program == other.program:
            return True
        return False


class Att_Ite(Node):
    def __init__(self, condition, true_case, false_case):
        self.condition = condition
        self.true_case = true_case
        self.false_case = false_case
        self.size = len(true_case) + len(false_case)


    def to_string(self):
        s =  "(if " + self.condition.to_string() + " then\n"
        for i in range(len(self.true_case)):
            s += "  " + self.true_case[i].to_string() + "\n"
        s+= " else\n "
        for i in range(len(self.false_case)):
            s += "  " + self.false_case[i].to_string() + "\n"
        s+=")"
        return s

    def interpret(self, env):
        interpret_list = []
        if self.condition.interpret(env):
            for l in self.true_case:
                interpret_list.append(l.interpret(env))
        else:
            for l in self.false_case:
                interpret_list.append(l.interpret(env))
        return interpret_list

    def set_ID(self, id):
        self.id = id

    def __eq__(self, other):
        if type(other) != Att_Ite:
            return False
        if self.condition == other.condition and self.true_case == other.true_case and self.false_case == other.false_case:
            return True
        return False

