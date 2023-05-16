from bayes_opt import BayesianOptimization, UtilityFunction
import numpy as np
from DSL import *


def create_interval(value, delta):
    interval = (value - delta, value + delta)
    return interval

class ParameterFinder():
    def __init__(self, inputs, actions, id, function):
        self.inputs = inputs
        self.actions = actions
        self.att_id = id
        self.function = function

    def set_IDs(self):
        q = []
        i = 1
        q.append(self.tree)
        while len(q) != 0:
            node = q.pop(0)
            node.set_ID(i)
            i+=1
            if isinstance(node, (Addition, Multiplication, Subtraction, Division, Exp, Lt, Or, Gt, And, Equal, NotEqual, Lt_Eq, Gt_Eq)):
                q.append(node.left)
                q.append(node.right)
            elif isinstance(node, (Abs, Neg, Sqrt, Log)):
                q.append(node.expr)
            elif isinstance(node, (Att_Ite)):
                q.append(node.condition)
                for t in node.true_case:
                    q.append(t)
                for f in node.false_case:
                    q.append(f)
            elif isinstance(node, Ite):
                q.append(node.condition)
                q.append(node.true_case)
                q.append(node.false_case)

    def print_IDs(self):
        q = []
        q.append(self.tree)
        while len(q) != 0:
            node = q.pop(0)
            print(node.id)
            print(node.to_string())
            if isinstance(node, (Addition, Multiplication, Subtraction, Division, Exp, Lt, Or, Gt, And, Equal, NotEqual, Lt_Eq, Gt_Eq)):
                q.append(node.left)
                q.append(node.right)
            elif isinstance(node, (Abs, Neg, Sqrt, Log)):
                q.append(node.expr)
            elif isinstance(node, (Att_Ite)):
                q.append(node.condition)
                for t in node.true_case:
                    q.append(t)
                for f in node.false_case:
                    q.append(f)
            elif isinstance(node, Ite):
                q.append(node.condition)
                q.append(node.true_case)
                q.append(node.false_case)


    def get_Num_range(self):
        dict_ranges = {}
        originals = []
        # BFS
        q = []
        q.append(self.tree)
        while len(q) != 0:
            node = q.pop(0)
            if isinstance(node, (Num)):
                name = 'Num{}'.format(node.id)
                originals.append(node.value)
                interval = create_interval(node.value, 20)
                dict_ranges[name] = interval
            elif isinstance(node, (Abs, Neg, Log, Sqrt)):
                q.append(node.expr)
            elif isinstance(node, (Addition, Multiplication, Subtraction, Division, Exp, Lt, Or, Gt, And, Equal, NotEqual, Lt_Eq, Gt_Eq)):
                q.append(node.left)
                q.append(node.right)
            elif isinstance(node, (Att_Ite)):
                q.append(node.condition)
                for t in node.true_case:
                    q.append(t)
                for f in node.false_case:
                    q.append(f)
            elif isinstance(node, Ite):
                q.append(node.condition)
                q.append(node.true_case)
                q.append(node.false_case)

        return dict_ranges, originals

    def set_Num_value(self, values):
        # BFS
        q = []
        q.append(self.tree)
        while len(q) != 0:
            node = q.pop(0)
            if isinstance(node, (Num)):
                name = "Num"+str(node.id)
                if type(values) is not list:
                    node.value = values[name]
                else:
                    node.value = values.pop(0)
                    #print(self.tree.toString())
            elif isinstance(node, (Abs, Neg, Log, Sqrt)):
                q.append(node.expr)
            elif isinstance(node, (Addition, Multiplication, Subtraction, Division, Exp, Lt, Or, Gt, And, Equal, NotEqual, Lt_Eq, Gt_Eq)):
                q.append(node.left)
                q.append(node.right)
            elif isinstance(node, (Att_Ite)):
                q.append(node.condition)
                for t in node.true_case:
                    q.append(t)
                for f in node.false_case:
                    q.append(f)
            elif isinstance(node, Ite):
                q.append(node.condition)
                q.append(node.true_case)
                q.append(node.false_case)
        return

    def find_distance(self, **kwargs):
        numNodes = np.fromiter(kwargs.values(), dtype=float)
        self.set_Num_value(numNodes.tolist())

        actions = self.function.get_action(self.att_id, self.tree)
        diff = 0
        for i in range(len(self.actions)):
            if actions[i] != self.actions[i]:
                diff += 1

        return -diff/float(len(self.actions))

    def optimize(self, tree):
        self.tree = tree
        self.set_IDs()
        gp_params = {"alpha": 1e-3, "n_restarts_optimizer": 10}  # Optimizer configuration
        list_Nums_range, originals = self.get_Num_range()
        if len(list_Nums_range) == 0:
            return originals
        bayesOpt = BayesianOptimization(self.find_distance,
                                        pbounds=list_Nums_range, verbose=0)
        try:
            bayesOpt.maximize(init_points=10, n_iter=20, acq="ucb", kappa=5, **gp_params)
            self.set_Num_value(bayesOpt.max['params'])
        except Exception as e:
            self.set_Num_value(originals)
