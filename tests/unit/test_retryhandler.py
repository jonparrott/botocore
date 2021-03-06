#!/usr/bin/env
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
from tests import unittest

import mock

from botocore.retryhandler import RetryHandler, delay_exponential


class RetryHandlerTest(unittest.TestCase):

    @mock.patch('time.sleep')
    def test_multiple_attempts(self, sleep_mock):

        def retryable(a=None, b=None, c=None):
            return 0

        def statusfn(attempt, return_value):
            if attempt < 3:
                delay_exponential(attempt)
                return True
            return False

        rh = RetryHandler(retryable, statusfn)
        rv = rh(a=1, b=2)
        self.assertEqual(rv, 0)
        self.assertEqual(rh.attempts, 3)

    @mock.patch('time.sleep')
    def test_return_value_status(self, sleep_mock):
        n = 0

        def retryable(a=None):
            if a['n'] < 4:
                a['n'] += 1
                return 0
            return 1

        def statusfn(attempt, return_value):
            if return_value != 1:
                delay_exponential(attempt)
                return True
            return False

        rh = RetryHandler(retryable, statusfn)
        rv = rh(a={'n': 1})
        self.assertEqual(rv, 1)
        self.assertEqual(rh.attempts, 4)


if __name__ == "__main__":
    unittest.main()
