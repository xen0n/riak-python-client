# -*- coding: utf-8 -*-
import os
import platform
import time
if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest

RUN_YZ = int(os.environ.get('RUN_YZ', '0'))



class YZSearchTests(object):
    @unittest.skipUnless(RUN_YZ, 'RUN_YZ is undefined')
    def test_solr_search_from_bucket_yz(self):
        bucket = self.client.bucket('searchbucket')
        bucket.new("user", {"username_s": "roidrage"}).store()
        time.sleep(1)
        results = bucket.search("username_s:roidrage")
        self.assertEquals(1, len(results['docs']))

#     @unittest.skipUnless(RUN_YZ, 'RUN_YZ is undefined')
#     def test_solr_search_with_params_from_bucket(self):
#         bucket = self.client.bucket(self.search_bucket)
#         bucket.new("user", {"username_s": "roidrage"}).store()
#         results = bucket.search("username_s:roidrage", wt="xml")
#         self.assertEquals(1, len(results['docs']))

#     @unittest.skipUnless(RUN_YZ, 'RUN_YZ is undefined')
#     def test_solr_search_with_params(self):
#         bucket = self.client.bucket(self.search_bucket)
#         bucket.new("user", {"username_s": "roidrage"}).store()
#         results = self.client.solr.search(self.search_bucket,
#                                           "username_s:roidrage", wt="xml")
#         self.assertEquals(1, len(results['docs']))

#     @unittest.skipUnless(RUN_YZ, 'RUN_YZ is undefined')
#     def test_solr_search(self):
#         bucket = self.client.bucket(self.search_bucket)
#         bucket.new("user", {"username_s": "roidrage"}).store()
#         results = self.client.solr.search(self.search_bucket,
#                                           "username_s:roidrage")
#         self.assertEquals(1, len(results["docs"]))

#     @unittest.skipUnless(RUN_YZ, 'RUN_YZ is undefined')
#     def test_search_integration(self):
#         # Create some objects to search across...
#         bucket = self.client.bucket(self.search_bucket)
#         bucket.new("one", {"foo": "one", "bar": "red"}).store()
#         bucket.new("two", {"foo": "two", "bar": "green"}).store()
#         bucket.new("three", {"foo": "three", "bar": "blue"}).store()
#         bucket.new("four", {"foo": "four", "bar": "orange"}).store()
#         bucket.new("five", {"foo": "five", "bar": "yellow"}).store()

#         # Run some operations...
#         results = self.client.solr.search(self.search_bucket,
#                                           "foo:one OR foo:two")
#         if (len(results) == 0):
#             print "\n\nNot running test \"testSearchIntegration()\".\n"
#             print """Please ensure that you have installed the Riak
#             Search hook on bucket \"searchbucket\" by running
#             \"bin/search-cmd install searchbucket\".\n\n"""
#             return
#         self.assertEqual(len(results['docs']), 2)
#         query = "(foo:one OR foo:two OR foo:three OR foo:four) AND\
#                  (NOT bar:green)"
#         results = self.client.solr.search(self.search_bucket, query)

#         self.assertEqual(len(results['docs']), 3)
