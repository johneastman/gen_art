from turtle import *


class LSystem:
    """An L-System generator.

    An example L-System can be seen below:
        variables : A B
        constants : none
        axiom : A
        rules : (A → AB), (B → A)

    This system produces the following:
        n = 0 : A
        n = 1 : AB
        n = 2 : ABA
        n = 3 : ABAAB
        n = 4 : ABAABABA
        n = 5 : ABAABABAABAAB
        n = 6 : ABAABABAABAABABAABABA
        n = 7 : ABAABABAABAABABAABABAABAABABAABAAB

    More information about L-Systems can be found here: https://en.wikipedia.org/wiki/L-system
    """
    def __init__(self, variables, axiom, rules):
        """Initialize L-System generator.

        :param variables: values that can be replaced
        :param axiom: the starting string
        :param rules: how variables are replaced during each iteration
        """
        self.variables = variables
        self.axiom = axiom
        self.rules = rules

    def generate(self, n):
        """Generate the L-System sequences

        :param n: the number of iterations
        :return: generator containing the first n iterations
        """
        current_iter = self.axiom
        yield current_iter

        for _ in range(n):
            next_iter = "".join([self.rules.get(c, c) for c in current_iter])
            current_iter = next_iter
            yield next_iter


if __name__ == "__main__":
    l = LSystem(["A", "B"], "A", {"A": "B-A-B", "B": "A+B+A"})
    sequence = list(l.generate(8))
    for s in sequence:
        print(s)
