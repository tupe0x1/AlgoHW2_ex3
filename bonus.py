from itertools import combinations

import cvxpy


def validate_input(input_given):
    """
        input validating
        """
    if not isinstance(input_given, list):
        raise Exception("input given should be a list")
    if len(input_given) < 1:
        raise Exception("input given length should be greater than 0")
    for i in input_given:
        if not isinstance(i, list):
            raise Exception("input given should be a list of lists")
    input_given_item_length = len(input_given[0])
    for i in input_given:
        if len(i) != input_given_item_length:
            raise Exception("input given should be a list of lists with same length")


def leximin_egalitarian_calc(input_given,  verbose=False):
    """
    preform leximin egalitarian calculation on for n users and m resources

    >>> leximin_egalitarian_calc([[4, 0, 0], [0, 3, 0], [5,5,10], [5,5,10]])
    Agent #1 gets 1.00 of resource #1, 0.00 of resource #2, 0.00 of resource #3.
    Agent #2 gets 0.00 of resource #1, 1.00 of resource #2, 0.00 of resource #3.
    Agent #3 gets 0.00 of resource #1, 0.00 of resource #2, 0.50 of resource #3.
    Agent #4 gets 0.00 of resource #1, 0.00 of resource #2, 0.50 of resource #3.
    >>> leximin_egalitarian_calc([[1, 0, 0], [0, 2, 0], [0,0,1], [0,0,1]])
    Agent #1 gets 1.00 of resource #1, 0.00 of resource #2, 0.00 of resource #3.
    Agent #2 gets 0.00 of resource #1, 1.00 of resource #2, 0.00 of resource #3.
    Agent #3 gets 0.00 of resource #1, 0.00 of resource #2, 0.50 of resource #3.
    Agent #4 gets 0.00 of resource #1, 0.00 of resource #2, 0.50 of resource #3.
    >>> leximin_egalitarian_calc([[1, 0, 0], [0, 1, 0], [0,1,1], [0,0,1]])
    Agent #1 gets 1.00 of resource #1, 0.00 of resource #2, 0.00 of resource #3.
    Agent #2 gets 0.00 of resource #1, 0.67 of resource #2, 0.00 of resource #3.
    Agent #3 gets 0.00 of resource #1, 0.33 of resource #2, 0.33 of resource #3.
    Agent #4 gets 0.00 of resource #1, 0.00 of resource #2, 0.67 of resource #3.
    """
    validate_input(input_given)
    input_variables_matrix = [cvxpy.Variable(len(dude)) for dude in input_given]
    """
    utility adding
    """
    utility_list = []
    for i in range(len(input_given)):
        tmp_utility = None
        for j in range(len(input_given[i])):
            if tmp_utility is None:
                tmp_utility = input_variables_matrix[i][j]*input_given[i][j]
                continue
            tmp_utility += input_variables_matrix[i][j]*input_given[i][j]
        utility_list.append(tmp_utility)

    """
    fixed constraints adding
    """
    constraints_list = []

    # add 0 to 1 constrains
    for i, val in enumerate(input_variables_matrix):
        [constraints_list.append(val[j]<=1) for j in range(len(input_given[i]))]
        [constraints_list.append(val[j]>=0) for j in range(len(input_given[i]))]

    # add limit the sum to 1 constrains
    for i in range(len(input_given[0])):
        constraints_list.append(sum(input_variables_matrix[j][i] for j in range(len(input_given)))<=1)

    """
    problem iterative solving
    """
    utility_constraints_list = []
    last_prob = None
    for i in range(len(input_given)):
        if verbose:
            for u in utility_constraints_list:
                print(u)
        min_utility = cvxpy.Variable()
        last_prob = cvxpy.Problem(
            cvxpy.Maximize(min_utility),
            constraints=constraints_list +
                        utility_constraints_list +
                        [min_utility<=sum(i) for i in combinations(utility_list, i+1)]
                        )
        last_prob.solve()
        utility_constraints_list.extend([min_utility.value<=sum(i) for i in combinations(utility_list, i+1)])

    if verbose:
        for i in constraints_list:
            print(i)
        print("status:", last_prob.status)
        print("optimal value: ", last_prob.value)
        for i, val in enumerate(utility_list):
            print(f"utility of Agent #{i + 1}: {val.value}")

    for i, val in enumerate(input_variables_matrix):
        text_gen = []
        for j, v in enumerate(val.value):
            text_gen.append(f"{abs(v):.2f} of resource #{j + 1}")
        print(f"Agent #{i + 1} gets {', '.join(text_gen)}.")


if __name__ == "__main__":
    #input_given = [[4, 0, 0], [0, 3, 0], [5,5,10], [5,5,10]]
    #leximin_egalitarian_calc(input_given, verbose=True)
    import doctest
    doctest.testmod()