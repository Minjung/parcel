import unittest2 as unittest
import sys
import os
import tempfile
import shutil

from parcel.cache import FileCache
from mixins import WebServerMixin
from mock import MagicMock, patch


## Some functions to help building and clearing a directory
def mkdir():
    return tempfile.mkdtemp()
    
def rmdir(path):
    shutil.rmtree(path)

mock_makedirs = MagicMock(name="mock_makedirs")
mock_makedirs.side_effect = OSError(2, 'Test exception', 'test')

##
## Test Suite
##
class CacheTestSuite(unittest.TestCase, WebServerMixin):
    """Versions test cases."""
    def setUp(self):
        self.path = None  # use this in tests for a directory that will always be deleted
    
    def tearDown(self):
        if self.path:
            rmdir(self.path)
        self.path = None
        
    def test_new_cache_makes_directory(self):
        # make a path
        self.path = mkdir()
        
        # delete it. so the cache has to create it
        rmdir(self.path)
  
        # make a cache with it
        cache = FileCache(self.path)
        
        # director should exist
        self.assertTrue(os.path.isdir(self.path))
        
        # directory should be empty
        self.assertFalse(os.listdir(self.path))
        
    def test_new_cache_uses_existing_directory(self):
        # make path
        self.path = mkdir()
        
        # make a cache with it
        cache = FileCache(self.path)
        
        # directory should exist
        self.assertTrue(os.path.isdir(self.path))
        
        # directory should be empty
        self.assertFalse(os.listdir(self.path))
        
    def test_get_tarball_url(self):
        self.startWebServer()
        
        # make cache
        self.path = mkdir()
        cache = FileCache(self.path)
        
        # get test tarball
        path = cache.get("http://localhost:%d/tip.tar.gz"%self.port)

        self.assertTrue(cache.is_cached('tip.tar.gz'))  # check it reports file as cached
        self.assertTrue('tip.tar.gz' in os.listdir(self.path))  # make sure file is in cache
        self.assertEquals(path, os.path.join(self.path,'tip.tar.gz'))  # make sure thats what was returned

        # get it again to exercise cache
        path = cache.get("http://localhost:%d/tip.tar.gz"%self.port)
        
        self.stopWebServer()

    @patch('os.makedirs', mock_makedirs)
    def test_oserror_path(self):
        self.path = mkdir()
        with self.assertRaises(OSError):
            cache = FileCache(self.path)
        mock_makedirs.assert_called_once(self.path)

