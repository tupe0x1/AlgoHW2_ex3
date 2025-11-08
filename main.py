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


def egalitarian_calc(input_given,  verbose=False):
    """
    preform egalitarian calculation on for n users and m resources

    >>> egalitarian_calc([[1, 1, 1], [1, 1, 1], [1,1,1]])
    Agent #1 gets 0.33 of resource #1, 0.33 of resource #2, 0.33 of resource #3.
    Agent #2 gets 0.33 of resource #1, 0.33 of resource #2, 0.33 of resource #3.
    Agent #3 gets 0.33 of resource #1, 0.33 of resource #2, 0.33 of resource #3.


    they have the same value for all so it will be 0.33 for any

    >>> egalitarian_calc([[80, 19, 1], [79, 1, 20]])
    Agent #1 gets 0.50 of resource #1, 1.00 of resource #2, 0.00 of resource #3.
    Agent #2 gets 0.50 of resource #1, 0.00 of resource #2, 1.00 of resource #3.

    this is the class code example

    >>> egalitarian_calc([[81, 19, 1], [70, 1, 29]])
    Agent #1 gets 0.53 of resource #1, 1.00 of resource #2, 0.00 of resource #3.
    Agent #2 gets 0.47 of resource #1, 0.00 of resource #2, 1.00 of resource #3.

    this is the homework example

    >>> egalitarian_calc([[1, 0, 0], [0, 1, 0], [0,0,1]])
    Agent #1 gets 1.00 of resource #1, 0.00 of resource #2, 0.00 of resource #3.
    Agent #2 gets 0.00 of resource #1, 1.00 of resource #2, 0.00 of resource #3.
    Agent #3 gets 0.00 of resource #1, 0.00 of resource #2, 1.00 of resource #3.

    >>> egalitarian_calc([[2, 1, 1], [1, 1, 1], [1,1,2]])
    Agent #1 gets 0.75 of resource #1, 0.00 of resource #2, 0.00 of resource #3.
    Agent #2 gets 0.25 of resource #1, 1.00 of resource #2, 0.25 of resource #3.
    Agent #3 gets 0.00 of resource #1, 0.00 of resource #2, 0.75 of resource #3.
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
    constraints adding
    """
    min_utility = cvxpy.Variable()
    constraints_list = []

    # add utility constrains
    for i in utility_list:
        constraints_list.append(min_utility<=i)

    # add 0 to 1 constrains
    for i, val in enumerate(input_variables_matrix):
        [constraints_list.append(val[j]<=1) for j in range(len(input_given[i]))]
        [constraints_list.append(val[j]>=0) for j in range(len(input_given[i]))]

    # add limit the sum to 1 constrains
    for i in range(len(input_given[0])):
        constraints_list.append(sum(input_variables_matrix[j][i] for j in range(len(input_given)))<=1)

    """
    problem solving
    """
    prob = cvxpy.Problem(
        cvxpy.Maximize(min_utility),
        constraints=constraints_list)
    prob.solve()

    if verbose:
        for i in constraints_list:
            print(i)
        print("status:", prob.status)
        print("optimal value: ", prob.value)
        for i, val in enumerate(utility_list):
            print(f"utility of Agent #{i + 1}: {val.value}")

    for i, val in enumerate(input_variables_matrix):
        text_gen = []
        for j, v in enumerate(val.value):
            text_gen.append(f"{abs(v):.2f} of resource #{j + 1}")
        print(f"Agent #{i + 1} gets {', '.join(text_gen)}.")

if __name__ == "__main__":
    #input_given = [[80, 19, 1], [79, 1, 20]]
    #egalitarian_calc(input_given, verbose=True)
    import doctest
    doctest.testmod()