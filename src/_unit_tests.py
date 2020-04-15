import unittest
from holstep import HolstepTreeParser as HTP, QuickHolstepSeqParser as QHSP

parser = HTP()
seqparser = QHSP()

def check(test, expr, expected, exp_vars=[], exp_varfuncs=[]):
    tree = parser.parse(expr)
    tree.build_unique_info()

    check_node(test, tree, expected)
    test.assertFalse(tree.has_FILL())
    test.assertFalse(any([b > 2 for b in tree.unique_branching.keys()]))
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
            
    def test_multichar_var(self):
        check(self, '|- (!ul. (!k. (((k + (NUMERAL (BIT0 (BIT1 _0)))) <= (LENGTH ul)) ==> _0)))',
              ['|-', 
               ['!', ['ul', ['.']],
                ['!', ['k', ['.']],
                 ['==>',
                  ['<=', 
                   ['+',
                    ['k'],
                    ['NUMERAL', ['BIT0', ['BIT1', ['_0']]]]
                    ],
                   ['LENGTH', ['ul']]
                   ],
                  ['_0']
                  ]]]] , exp_vars=['ul', 'k'])
            
    def test_genpvar_var_and_multi_arg(self):
        check(self, '|- (!y1. (!y2. (!y3. (!y5. (!y6. (real_open (GSPEC (\\GEN%PVAR%8085. ' 
                + '(?y4. (((SETSPEC GEN%PVAR%8085) (((real_lt (real_of_num (NUMERAL _0))) y4) ' 
                + '/\\ ((real_lt (real_of_num (NUMERAL _0))) ((((((delta_y y1) y2) y3) y4) y5) y6)))) y4))))))))))',
              ['|-',
               ['!', ['y1', ['.']],
                ['!', ['y2', ['.']],
                 ['!', ['y3', ['.']],
                  ['!', ['y5', ['.']],
                   ['!', ['y6', ['.']],
                    ['real_open', 
                     ['GSPEC',
                      ['\\', ['GEN%PVAR%8085', ['.']],
                       ['?', ['y4', ['.']],
                        ['SETSPEC',
                         ['GEN%PVAR%8085'],
                         ['ARG', 
                          ['/\\',
                           ['real_lt', 
                            ['real_of_num', ['NUMERAL', ['_0']]],
                             ['y4']
                           ],
                           ['real_lt', 
                            ['real_of_num', ['NUMERAL', ['_0']]],
                            ['delta_y',
                             ['y1'],
                             ['ARG', 
                              ['y2'],
                              ['ARG',
                               ['y3'],
                               ['ARG',
                                ['y4'],
                                ['ARG', ['y5'], ['y6']]
                                ]]]]]], ['y4']
                           ]]]]]]]]]]]]
                           , exp_vars=['y1', 'y2', 'y3', 'y5', 'y6', 'GEN%PVAR%8085', 'y4'])

    def test_constants(self):
        check(self, '|- (!s. ((collinear s) = (?u. (?v. (s SUBSET ((hull affine) (u INSERT (v INSERT EMPTY))))))))',
              ['|-',
               ['!', ['s', ['.']],
                ['=',
                 ['collinear', ['s']],
                 ['?', ['u', ['.']],
                  ['?', ['v', ['.']],
                   ['SUBSET',
                    ['s'],
                    ['hull',
                     ['affine'],
                     ['INSERT',
                      ['u'],
                      ['INSERT',
                       ['v'],
                       ['EMPTY']
                       ]]]]]]]]], exp_vars=['s', 'u', 'v'])
            
    def test_tbd(self):
        check(self, '|- (ldih_x = ((mul6 ((scalar6 ((sub6 ((scalar6 unit6) h0)) ((scalar6 proj_y1) ' 
                  + '((DECIMAL (NUMERAL (BIT1 (BIT0 (BIT1 _0))))) (NUMERAL (BIT0 (BIT1 (BIT0 (BIT1 _0)))' 
                  + ')))))) rh0)) dih_x))',
              ['|-',
               ['=',
                ['ldih_x'],
                ['mul6',
                 ['scalar6', 
                  ['sub6',
                   ['scalar6', ['unit6'], ['h0']],
                   ['scalar6',
                    ['proj_y1'],
                    ['DECIMAL', 
                     ['NUMERAL', ['BIT1', ['BIT0', ['BIT1', ['_0']]]]],
                     ['NUMERAL', ['BIT0', ['BIT1', ['BIT0', ['BIT1', ['_0']]]]]]
                    ]
                    ]],
                 ['rh0']],
                ['dih_x'],
                ]]], exp_vars=['h0'])    
            
    def test_letternumber_var_unquantified(self):
        check(self, '|- (~ (collinear ((vec (NUMERAL _0)) INSERT (v1 INSERT (v2 INSERT EMPTY)))))',
              ['|-',
               ['~',
                ['collinear',
                 ['INSERT',
                  ['vec', ['NUMERAL', ['_0']]],
                  ['INSERT',
                   ['v1'],
                   ['INSERT', ['v2'], ['EMPTY']]
                   ]]]]], exp_vars=['v1', 'v2'])
    
    def test_varfunc_first_before_operation(self):
        check(self, '|- ((E UNION ((v INSERT (w INSERT EMPTY)) INSERT EMPTY)) = E1)',
              ['|-',
               ['=',
                ['UNION',
                 ['E'],
                 ['INSERT',
                  ['INSERT', 
                   ['v'],
                   ['INSERT', ['w'], ['EMPTY']]
                   ],
                  ['EMPTY']
                  ]
                  ],
                  ['E1']
                  ]], exp_vars=['v', 'w'], exp_varfuncs=['E', 'E1']) 
            
    def test_deeper_varfunc_with_nochild_fill_stack(self):
        check(self, '|- (!P. (test = ((P (NUMERAL (BIT1 _0))) /\ (P (NUMERAL (BIT0 (BIT1 _0)))))))',
              ['|-',
               ['!', ['P', ['.']],
                ['=',
                 ['test'],
                 ['/\\',
                  ['P', ['NUMERAL', ['BIT1', ['_0']]]],
                  ['P', ['NUMERAL', ['BIT0', ['BIT1', ['_0']]]]],
                  ]]]], exp_varfuncs=['P'])        

    def test_op_as_term(self):
        check(self, '|- (monoidal +)', ['|-', ['monoidal', ['+']]])  
        
    def test_premise_list_and_conclusion(self):
        check(self, '(!s. (test s)), ((test s) /\ (test s)), (test s) |- '
                  + '((open_in ((subtopology euclidean) t)) s)',
              ['STEP',
               [',',
                ['!', ['s', ['.']],
                 ['test', ['s']]
                 ],
                ['ARG', 
                 ['/\\',
                  ['test', ['s']],
                  ['test', ['s']]
                  ],
                 ['test', ['s']]
                 ]
                ],
                ['|-',
                 ['open_in', 
                  ['subtopology', 
                   ['euclidean'],
                   ['t']
                   ],
                  ['s']
                  ]]], exp_vars=['s', 't']) 
        
    def test_single_premise_list(self):
        check(self, '(closed s) |- ((closed s) = T)',
              ['STEP',
               [',', ['closed', ['s']]],
               ['|-',
                ['=',
                 ['closed', ['s']],
                 ['T']
                 ]]], exp_vars=['s'])    
            
    def test_function_derivative(self):
        check(self, "|- (((has_real_derivative f) f') \\/ (!f'. (f = f')))",
              ['|-',
               ['\\/',
                ['has_real_derivative',
                 ['f'],
                 ['f', "'"]],
                ['!', ['f', ["'"], ['.']],
                 ['=', ['f'], ['f', "'"]]
                 ]]], exp_vars=['f'])
            
    def test_named_premise_args_single(self):
        check(self, "pf |- (test s)",
              ['STEP',
               [',', ['pf']],
               ['|-', ['test', ['s']]]
               ], exp_vars=['pf', 's'])
            
    def test_named_premise_args_many(self):
        check(self, "pf, pg, ph |- (test s)",
              ['STEP',
               [',', 
                ['pf'],
                ['ARG', ['pg'], ['ph']]
                ],
               ['|-', ['test', ['s']]]
               ], exp_vars=['pf', 'pg', 'ph', 's'])
            
    def test_apostrophe_on_value(self):
        check(self, "|- (MMs_v39 scs_4M6')",
              ['|-', ['MMs_v39', ['scs_4M6', ["'"]]]])         

    def test_apostrophe_on_function(self):
        check(self, "|- (nfgtrans' (test g))",
              ['|-', 
               ['nfgtrans',
                ["'"],
                ['test', ['g']]
                ]], exp_vars=['g'])
            
    def test_apostrophe_then_operation(self):
        check(self, "|- (fa' = T)",
              ['|-', 
               ['=',
                ['fa', ["'"]],
                ['T']
                ]], exp_vars=[])            

    def test_named_step_result(self):
        check(self, "(test T) |- generatePolygon_reduction_v7",
              ['STEP',
               [',', ['test', ['T']]],
               ['|-', ['generatePolygon_reduction_v7']]
               ], exp_vars=['generatePolygon_reduction_v7'])
     
class TestHolstepParserSplitWord(unittest.TestCase):

    def test_just_word(self):
        token, parens, comma = parser.split_end_parens('test')
        self.assertEqual(token, 'test')
        self.assertIsNone(parens)
        self.assertIsNone(comma)
        
    def test_word_and_paren(self):
        token, parens, comma = parser.split_end_parens('test)')
        self.assertEqual(token, 'test')
        self.assertEqual(parens, ')')
        self.assertIsNone(comma)
        
    def test_word_and_many_parens(self):
        token, parens, comma = parser.split_end_parens('test)))')
        self.assertEqual(token, 'test')
        self.assertEqual(parens, ')))')
        self.assertIsNone(comma)
        
    def test_word_and_paren_and_comma(self):
        token, parens, comma = parser.split_end_parens('test),')
        self.assertEqual(token, 'test')
        self.assertEqual(parens, ')')
        self.assertEqual(comma, ',')
        
    def test_word_and_many_parens_and_comma(self):
        token, parens, comma = parser.split_end_parens('test))),')
        self.assertEqual(token, 'test')
        self.assertEqual(parens, ')))')
        self.assertEqual(comma, ',')
        
    def test_comma_as_word(self):
        token, parens, comma = parser.split_end_parens(',)))')
        self.assertEqual(token, ',')
        self.assertEqual(parens, ')))')
        self.assertIsNone(comma)
        
    def test_comma_as_word_with_comma(self):
        token, parens, comma = parser.split_end_parens(',))),')
        self.assertEqual(token, ',')
        self.assertEqual(parens, ')))')
        self.assertEqual(comma, ',')
        
    def test_just_word_and_comma(self):
        token, parens, comma = parser.split_end_parens('test,')
        self.assertEqual(token, 'test')
        self.assertIsNone(parens)
        self.assertEqual(comma, ',')

if __name__ == '__main__':
    unittest.main()
