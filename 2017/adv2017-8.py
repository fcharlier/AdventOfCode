#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator
from StringIO import StringIO

expression = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""

expression = StringIO(expression)


# with open(input_data) as expression:
#     parse_expression(expression)


class ExpressionEvaluator(object):
    def __init__(self):
        self.regs = {}
        self.ops = {
            'inc': operator.add,
            'dec': operator.sub
        }
        self.tests = {
            '<': operator.lt,
            '>': operator.gt,
            '<=': operator.le,
            '>=': operator.ge,
            '==': operator.eq,
            '!=': operator.ne
        }
        self.max = None

    def get(self, name):
        return self.regs.get(name, 0)

    def set(self, name, value):
        self.regs[name] = value
        if self.max is None or self.max < value:
            self.max = value
        return self.regs[name]

    def test_condition(self, reg, op, value):
        print "\tTest cond:", reg, op, value
        reg = self.get(reg)
        op = self.tests[op]
        print "\tDebug:", reg, op, value
        result = op(reg, value)
        print "\t\tResult:", result
        return result

    def do_op(self, reg, op, count):
        regV = self.get(reg)
        op = self.ops[op]
        result = op(regV, count)
        self.set(reg, result)
        return self.get(reg)

    def eval_expression(self, expression):
        for line in expression:
            line = line.strip()
            regW, op, count, _, regT, opT, value = line.split()
            count = int(count)
            value = int(value)

            print 'Evaluating: %s' % line
            if self.test_condition(regT, opT, value):
                print 'Condition ok, operation result: ',
                self.do_op(regW, op, count)
                print '%s ← %d' % (regW, self.get(regW))

        print 'Largest register value is: %d' % max(self.regs.values())
        print 'Largest register value during the run is: %d' % self.max


if __name__ == '__main__':
    ev = ExpressionEvaluator()
    with open('adv2017-8.input') as expression:
        ev.eval_expression(expression)
