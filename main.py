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

    return matrix_lit


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


def fnc_sat(expression_literals):
    """

    :param expression_literals:
    :return:
    """
    matrix_lit = parse_expression(expression_literals)
    interpretation = []
    fnc_sat_backtracking(0, len(matrix_lit[0]), 0, interpretation, matrix_lit)


if __name__ == '__main__':
    expression = input()
    fnc_sat(expression)
    print(interpretation_result)
