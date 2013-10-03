#!/usr/bin/env python
import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mothertongue.tests.test_settings'

parent = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.insert(0, parent)

from django.test.simple import DjangoTestSuiteRunner

def runtests():

    tester = DjangoTestSuiteRunner(verbosity=1, interactive=True)
    failures = tester.run_tests(['tests'])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()

