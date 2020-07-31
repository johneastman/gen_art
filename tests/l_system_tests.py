import unittest
from l_system import LSystem


class LSystemTest(unittest.TestCase):

    def test_l_system_init_no_constants(self):

        variables = ["A", "B"]
        axiom = "A"
        rules = {"A": "AB", "B": "A"}

        l = LSystem(variables, axiom, rules)

        self.assertEqual(variables, l.variables)
        self.assertEqual(axiom, l.axiom)
        self.assertEqual(rules, l.rules)

    def test_l_system_init_with_constants(self):

        variables = ["0", "1"]
        axiom = "0"
        rules = {"1": "11", "0": "1[0]0"}

        l = LSystem(variables, axiom, rules)

        self.assertEqual(variables, l.variables)
        self.assertEqual(axiom, l.axiom)
        self.assertEqual(rules, l.rules)

    def test_generate_1(self):
        l = LSystem(["A", "B"], "A", {"A": "AB", "B": "A"})
        expected = [
            "A",
            "AB",
            "ABA",
            "ABAAB",
            "ABAABABA",
            "ABAABABAABAAB",
            "ABAABABAABAABABAABABA",
            "ABAABABAABAABABAABABAABAABABAABAAB"
        ]

        self.assertEqual(expected, list(l.generate(len(expected) - 1)))

    def test_generate_2(self):
        l = LSystem(["0", "1"], "0", {"1": "11", "0": "1[0]0"})
        expected = [
            "0",
            "1[0]0",
            "11[1[0]0]1[0]0",
            "1111[11[1[0]0]1[0]0]11[1[0]0]1[0]0"
        ]

        self.assertEqual(expected, list(l.generate(len(expected) - 1)))


if __name__ == "__main__":
    unittest.main()
