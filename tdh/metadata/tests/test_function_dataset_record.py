import doctest
import unittest

from Testing import ZopeTestCase as ztc

from App.config import setConfiguration

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import tdh.metadata
from tdh.metadata.testing import TDH_METADATA_FUNCTIONAL_TESTING


OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
               doctest.ELLIPSIS

ptc.setupPloneSite(products=['tdh.metadata'])

class TestCase(ptc.PloneTestCase):

    app = TDH_METADATA_FUNCTIONAL_TESTING

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml',
              tdh.metadata)


        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='tdh.metadata',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='tdh.metadata.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'tests/FUNCTION_DATASET_RECORD.tests', 
            package='tdh.metadata',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'BROWSER.TXT',
        #    package='tdh.metadata',
        #    optionflags = OPTION_FLAGS,
        #    test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
