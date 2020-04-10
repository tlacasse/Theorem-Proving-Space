import unittest
from holstep import HolstepTreeParser as HTP, QuickHolstepSeqParser as QHSP

parser = HTP()
seqparser = QHSP()

def check(test, expr, expected, exp_vars=[], exp_varfuncs=[]):
    tree = parser.parse(expr)
    tree.build_unique_info()

    check_node(test, tree, expected)
    test.assertFalse(tree.has_FILL())
    test.assertFalse(any([b for b in tree.unique_branching.keys() if b > 2]))
    test.assertEqual(len(seqparser.parse(expr)), tree.node_count())
    
    test.assertEqual(len(parser.stack), 1)
    test.assertEqual(len(parser.varlist), len(exp_vars))
    for a, e in zip(parser.varlist, exp_vars):
        test.assertEqual(a, e)
    test.assertEqual(len(parser.varfunclist), len(exp_varfuncs))
    for a, e in zip(parser.varfunclist, exp_varfuncs):
        test.assertEqual(a, e)
    
def check_node(test, node, expected):
    print('"{}" =?= "{}"'.format(node.value, expected[0]))
    test.assertEqual(node.value, expected[0])
    test.assertTrue(len(node.children) <= 2)
    test.assertEqual(len(node.children), len(expected[1:]))
    for n, e in zip(node.children, expected[1:]):
        check_node(test, n, e)

class TestHolstepTreeParsing(unittest.TestCase):

    def test_basic_parsing(self):
        check(self, '|- (!n. (!m. (((SUC m) - (SUC n)) = (m - n))))',
              ['|-', 
               ['!', ['n', ['.']],
                 ['!', ['m', ['.']],
                   ['=',
                    ['-',
                     ['SUC', ['m']],
                     ['SUC', ['n']]
                     ],
                    ['-', ['m'], ['n']]
                    ]]]], exp_vars=['n', 'm'])
    
    
    def test_predicates_and_negation(self):
        check(self, '|- (!P. ((~ (?x. (P x))) = (!x. (~ (P x)))))',
              ['|-',
               ['!', ['P', ['.']],
                ['=',
                 ['~', 
                  ['?', ['x', ['.']],
                   ['P', ['x']]
                  ],
                 ], 
                 ['!', ['x', ['.']],
                  ['~', 
                   ['P', ['x']]
                   ]]]]], exp_vars=['x'], exp_varfuncs=['P'])
    
    def test_predicate_var_and_func(self):
        check(self, '|- (!P. (!Q. ((P \/ (!x. (Q x))) = (!x. (P \/ (Q x))))))',
              ['|-',
               ['!', ['P', ['.']],
                ['!', ['Q', ['.']],
                 ['=',
                  ['\\/', 
                   ['P'],
                   ['!', ['x', ['.']], ['Q', ['x']]]
                  ],
                  ['!', ['x', ['.']],
                   ['\\/', ['P'], ['Q', ['x']]]
                   ]]]]], exp_vars=['x'], exp_varfuncs=['P', 'Q'])
    
    def test_T_F_and_non_quantified_vars(self):
        check(self, '|- ((!x. (P x)) = ((P T) /\ (P F)))',
              ['|-',
               ['=',
                ['!', ['x', ['.']], ['P', ['x']]],
                ['/\\',
                 ['P', ['T']],
                 ['P', ['F']]
                 ]]]
               , exp_vars=['x'], exp_varfuncs=['P'])

    def test_deep_operation(self):
        check(self, '|- (!x. (!y. ((NUMERAL (BIT1 _0)) + (NUMERAL (BIT1 _0)))))',
              ['|-', 
               ['!', ['x', ['.']],
                 ['!', ['y', ['.']],
                   ['+',
                    ['NUMERAL', ['BIT1', ['_0']]],
                    ['NUMERAL', ['BIT1', ['_0']]]
                ]]]], exp_vars=['x', 'y'])
            
    def test_chained_funcs(self):
        check(self, '|- (((real_div x) (real_of_num (NUMERAL (BIT1 _0)))) = x)',
              ['|-', 
               ['=',
                ['real_div', 
                 ['x'],
                 ['real_of_num', ['NUMERAL', ['BIT1', ['_0']]]]
                ],
                ['x']
                ]], exp_vars=['x'])
            
    def test_word_operation(self):
        check(self, '|- (!n. ((n EXP (NUMERAL (BIT0 (BIT1 _0)))) = (n * n)))',
              ['|-', 
               ['!', ['n', ['.']],
                ['=',
                 ['EXP',
                  ['n'],
                  ['NUMERAL', ['BIT0', ['BIT1', ['_0']]]]
                  ],
                 ['*', ['n'], ['n']
                 ]]]], exp_vars=['n'])
            
    def test_func_composition(self):
        check(self, '|- ((!f. (!g. (!x. (((f o g) x) = (f (g x)))))) ==> (\\f. (!g. (!x. ((f o g) x)))))',
              ['|-', 
               ['==>',
                ['!', ['f', ['.']],
                 ['!', ['g', ['.']],
                  ['!', ['x', ['.']],
                   ['=', 
                    ['o', 
                     ['f', ['g']],
                     ['x']
                     ],
                    ['f', ['g', ['x']]]
                    ]]]],
                ['\\', ['f', ['.']],
                 ['!', ['g', ['.']],
                  ['!', ['x', ['.']],
                   ['o',
                    ['f', ['g']],
                    ['x']
                    ]]]]]], exp_vars=['f', 'g', 'x'])

if __name__ == '__main__':
    unittest.main()
