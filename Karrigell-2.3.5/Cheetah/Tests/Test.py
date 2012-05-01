#!/usr/bin/env python
# $Id: Test.py,v 1.42 2005/01/03 20:07:53 tavis_rudd Exp $
"""Core module of Cheetah's Unit-testing framework

TODO
================================================================================
# combo tests
# negative test cases for expected exceptions
# black-box vs clear-box testing
# do some tests that run the Template for long enough to check that the refresh code works

Meta-Data
================================================================================
Author: Tavis Rudd <tavis@damnsimple.com>,
License: This software is released for unlimited distribution under the
         terms of the Python license.
Version: $Revision: 1.42 $
Start Date: 2001/03/30
Last Revision Date: $Date: 2005/01/03 20:07:53 $
"""
__author__ = "Tavis Rudd <tavis@damnsimple.com>"
__revision__ = "$Revision: 1.42 $"[11:-2]


##################################################
## DEPENDENCIES ##

import sys
import unittest_local_copy as unittest

##################################################
## CONSTANTS & GLOBALS

try:
    True, False
except NameError:
    True, False = (1==1),(1==0)

##################################################
## TESTS

import SyntaxAndOutput
import NameMapper
import Template
import FileRefresh
import CheetahWrapper

SyntaxSuite = unittest.findTestCases(SyntaxAndOutput)
NameMapperSuite = unittest.findTestCases(NameMapper)
TemplateSuite = unittest.findTestCases(Template)
FileRefreshSuite = unittest.findTestCases(FileRefresh)
CheetahWrapperSuite = unittest.findTestCases(CheetahWrapper)

from SyntaxAndOutput import *
from NameMapper import *
from Template import *
from FileRefresh import *
from CheetahWrapper import *

##################################################
## if run from the command line

if __name__ == '__main__':
    unittest.main()



