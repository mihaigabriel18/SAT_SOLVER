import numpy as nm

interpretation_result = [None]


class Node:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.value = val


def parse_expression(fnc_formula):
    clauze = fnc_formula.split("^")
    clauze_lungime = len(clauze)

    literali_all = {}  # dictionary with literals
    literal_num = 0  # every literal has a index associated, unique
    matrix_lit = nm.zeros((clauze_lungime, 0))
    # iterate over "clauze"
    for index_cl in range(0, len(clauze)):  # for every clause
        clauza = clauze[index_cl][1:-1]
        literali = clauza.split("V")

        for index_lit in range(0, len(literali)):  # for every literal in clause
            literal = literali[index_lit]
            if literal[0] == '~':

                if literal[1:] not in literali_all:
                    # if not in literali column to matrix and mark in dictionary
                    matrix_lit = nm.hstack((matrix_lit, nm.zeros((clauze_lungime, 1))))
                    literali_all[literal[1:]] = literal_num
                    literal_num += 1  # future new literal will have next index number

                matrix_lit[index_cl, literali_all[literal[1:]]] = -1
            else:

                if literal not in literali_all:
                    # if not in literali column to matrix and mark in dictionary
                    matrix_lit = nm.hstack((matrix_lit, nm.zeros((clauze_lungime, 1))))
                    literali_all[literal] = literal_num
                    literal_num += 1  # future new literal will have next index number

                matrix_lit[index_cl, literali_all[literal]] = 1

    inv_literali_all = {v: k for k, v in literali_all.items()}
    return matrix_lit, inv_literali_all


def fnc_sat_backtracking(step, n, unchecked_lit, interpretation, matrix_lit):
    """
    :param unchecked_lit: starting index of unchecked literals
    :param step:
    :param n: number of literals
    :param interpretation:
    :param matrix_lit:
    :return:
    """
    if step == n:
        for line in range(0, len(matrix_lit)):
            # storing the result of the "line"-th clause using given interpretation
            result_clause = interpretation * matrix_lit[line]
            # if a line doesn't have a single '1', then the whole expression is false
            if 1 not in result_clause:
                return False
        # All clauses have been checked for '1'-s, and all of them have at least a one
        global interpretation_result
        interpretation_result = interpretation.copy()
        return True

    for literal in range(unchecked_lit, n):
        for true_or_false in [-1, 1]:
            interpretation_new = list(interpretation)
            interpretation_new.append(true_or_false)

            # move to the next step with the new interpretation and another value for unchecked_lit
            if fnc_sat_backtracking(step + 1, n, unchecked_lit + 1, interpretation_new, matrix_lit):
                return True

    # All literals were checked, none satisfy the expression
    return False


def fnc_sat(matrix_lit):
    """

    :param matrix_lit:
    :return:
    """
    interpretation = []
    fnc_sat_backtracking(0, len(matrix_lit[0]), 0, interpretation, matrix_lit)


def simplify_expresion(expresion):
    expresion = str(expresion)
    clauses = expresion.split("^")
    for i in range(0, len(clauses)):
        # if a clause is false, the whole expression is false
        if clauses[i] == "(False)" or clauses[i] == "False":
            return "False"
        # if a literal in a clause is True, the whole clause is true
        if "True" in clauses[i]:
            clauses[i] = "True"
        # every roaming "False" is useless to the clause, unless is the only thing there
        clauses[i] = clauses[i].replace("False", "")

    # if the clause end or starts with a "V" remove it
    for i in range(0, len(clauses)):
        if clauses[i][1] == "V":
            clauses[i] = "(" + clauses[i][2:]  # remove first character
        if clauses[i][len(clauses[i]) - 2] == "V":
            clauses[i] = clauses[i][:-2] + ")"  # remove last character

    # every roaming "True" is useless to the expression
    clauses = [i for i in clauses if i != "True"]  # remove all occurrences of "True"
    # if the expression is the empty string, the expression evaluates to true
    if len(clauses) == 0:
        return "True"

    # in the end return a string made up from all the modified clauses from above
    separator = "^"
    return separator.join(clauses)


def build_tree(expr, literals):
    queue = []

    root = Node(expr)
    queue.append((root, 0))
    while True:
        currTuple = queue.pop(0)
        currNode = currTuple[0]
        level = currTuple[1]
        # reached a leaf node, tree is complete
        if level == len(literals):
            queue.insert(0, currTuple)
            break

        # built left child for negative case
        expression_left = str(currNode.value)
        expression_left = expression_left.replace(literals[level], "False")
        expression_left = expression_left.replace("~False", "True")
        expression_left = simplify_expresion(expression_left)
        print("Left " + expression_left)

        # built right child for negative case
        expression_right = str(currNode.value)
        expression_right = expression_right.replace(literals[level], "True")
        expression_right = expression_right.replace("~True", "False")
        expression_right = simplify_expresion(expression_right)
        print("Right " + expression_right)

        # create left and right nodes
        node_l = Node(expression_left)
        node_r = Node(expression_right)
        # add left and right child
        currNode.left = node_l
        currNode.right = node_r
        # adding nodes to queue
        queue.append((node_l, level + 1))
        queue.append((node_r, level + 1))

    return root


def bdd_sat(expr, literals):

    root = build_tree(expr, literals)


if __name__ == '__main__':
    expression = input()
    matrix_input, all_literali = parse_expression(expression)
    fnc_sat(matrix_input)
    print(interpretation_result)
    bdd_sat(expression, all_literali)
