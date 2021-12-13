from __future__ import with_statement

import sys
import unittest

from flexmock import flexmock
from conditional import conditional


class ConditionalTests(unittest.TestCase):

    def make_one(self, **kw):
        attrs = dict(__enter__=lambda:None, __exit__=lambda x,y,z:None)
        attrs.update(kw)
        return flexmock(**attrs)

    def test_true_condition_enters_context_manager(self):
        cm = self.make_one()
        flexmock(cm).should_call('__enter__').once
        flexmock(cm).should_call('__exit__').once

        with conditional(True, cm):
            pass

    def test_false_condition_does_not_enter_context_manager(self):
        cm = self.make_one()
        flexmock(cm).should_call('__enter__').never
        flexmock(cm).should_call('__exit__').never

        with conditional(False, cm):
            pass

    def test_true_condition_returns_enter_result(self):
        cm = self.make_one(__enter__=lambda:42)
        flexmock(cm).should_call('__enter__').once
        flexmock(cm).should_call('__exit__').once

        with conditional(True, cm) as value:
            self.assertEqual(value, 42)

    def test_false_condition_returns_None(self):
        cm = self.make_one()
        flexmock(cm).should_call('__enter__').never
        flexmock(cm).should_call('__exit__').never

        with conditional(False, cm) as value:
            self.assertEqual(value, None)

    def test_returning_true_from_exit_handles_exception(self):
        cm = self.make_one(__exit__=lambda x,y,z:True)
        flexmock(cm).should_call('__enter__').once
        flexmock(cm).should_call('__exit__').once

        with conditional(True, cm):
            raise RuntimeError()

    def test_returning_None_from_exit_lets_exception_propagate(self):
        cm = self.make_one()
        flexmock(cm).should_call('__enter__').once
        flexmock(cm).should_call('__exit__').once

        try:
            with conditional(True, cm):
                raise RuntimeError()
        except RuntimeError:
            pass # success
        else:
            self.fail('RuntimeError not raised')

