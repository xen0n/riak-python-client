"""
Copyright 2012 Basho Technologies, Inc.

This file is provided to you under the Apache License,
Version 2.0 (the "License"); you may not use this file
except in compliance with the License.  You may obtain
a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import re
from urllib import quote_plus, urlencode
from riak import RiakError
from riak.util import lazy_property


class RiakHttpResources(object):
    """
    Methods for RiakHttpTransport related to URL generation, i.e.
    creating the proper paths.
    """

    def ping_path(self):
        return mkpath(self.riak_kv_wm_ping)

    def stats_path(self):
        return mkpath(self.riak_kv_wm_stats)

    def mapred_path(self, **options):
        return mkpath(self.riak_kv_wm_mapred, **options)

    def bucket_list_path(self, bucket_type=None, **options):
        query = {'buckets': True}
        query.update(options)
        if self.riak_kv_wm_bucket_type and bucket_type:
            return mkpath("/types", quote_plus(bucket_type),
                          "buckets", **query)
        elif self.riak_kv_wm_buckets:
            return mkpath("/buckets", **query)
        else:
            return mkpath(self.riak_kv_wm_raw, **query)

    def bucket_properties_path(self, bucket, bucket_type=None, **options):
        if self.riak_kv_wm_bucket_type and bucket_type:
            return mkpath("/types", quote_plus(bucket_type), "buckets",
                          quote_plus(bucket), "props", **options)
        elif self.riak_kv_wm_buckets:
            return mkpath("/buckets", quote_plus(bucket),
                          "props", **options)
        else:
            query = options.copy()
            query.update(props=True, keys=False)
            return mkpath(self.riak_kv_wm_raw, quote_plus(bucket), **query)

    def bucket_type_properties_path(self, bucket_type, **options):
        return mkpath("/types", quote_plus(bucket_type), "props",
                      **options)

    def key_list_path(self, bucket, bucket_type=None, **options):
        query = {'keys': True, 'props': False}
        query.update(options)
        if self.riak_kv_wm_bucket_type and bucket_type:
            return mkpath("/types", quote_plus(bucket_type), "buckets",
                          quote_plus(bucket), "keys", **query)
        if self.riak_kv_wm_buckets:
            return mkpath("/buckets", quote_plus(bucket), "keys",
                          **query)
        else:
            return mkpath(self.riak_kv_wm_raw, quote_plus(bucket), **query)

    def object_path(self, bucket, key=None, bucket_type=None, **options):
        if key:
            key = quote_plus(key)
        if self.riak_kv_wm_bucket_type and bucket_type:
            return mkpath("/types", quote_plus(bucket_type), "buckets",
                          quote_plus(bucket), "keys", key, **options)
        elif self.riak_kv_wm_buckets:
            return mkpath("/buckets", quote_plus(bucket), "keys",
                          key, **options)
        else:
            return mkpath(self.riak_kv_wm_raw, quote_plus(bucket), key,
                          **options)

    def index_path(self, bucket, index, start, finish=None, bucket_type=None,
                   **options):
        if not self.riak_kv_wm_buckets:
            raise RiakError("Indexes are unsupported by this Riak node")
        if finish:
            finish = quote_plus(str(finish))
        if self.riak_kv_wm_bucket_type and bucket_type:
            return mkpath("/types", quote_plus(bucket_type),
                          "buckets", quote_plus(bucket),
                          "index", quote_plus(index), quote_plus(str(start)),
                          finish, **options)
        else:
            return mkpath("/buckets", quote_plus(bucket),
                          "index", quote_plus(index), quote_plus(str(start)),
                          finish, **options)

    def solr_select_path(self, index, query, **options):
        if not self.riak_solr_searcher_wm or self.yz_wm_search:
            raise RiakError("Search is unsupported by this Riak node")
        qs = {'q': query, 'wt': 'json'}
        qs.update(options)
        if index:
            index = quote_plus(index)
        return mkpath("/solr", index, "select", **qs)

    def solr_update_path(self, index):
        if not self.riak_solr_searcher_wm:
            raise RiakError("Riak Search 1 is unsupported by this Riak node")
        if index:
            index = quote_plus(index)
        return mkpath(self.riak_solr_indexer_wm, index, "update")

    def counters_path(self, bucket, key, **options):
        if not self.riak_kv_wm_counter:
            raise RiakError("Counters are unsupported by this Riak node")

        return mkpath(self.riak_kv_wm_buckets, quote_plus(bucket), "counters",
                      quote_plus(key), **options)

    # Feature detection overrides
    def bucket_types(self):
        return self.riak_kv_wm_bucket_type is not None

    def index_term_regex(self):
        if self.riak_kv_wm_bucket_type is not None:
            return True
        else:
            return super(RiakHttpResources, self).index_term_regex()

    # Resource root paths
    @lazy_property
    def riak_kv_wm_bucket_type(self):
        if 'riak_kv_wm_bucket_type' in self.resources:
            return "/types"

    @lazy_property
    def riak_kv_wm_buckets(self):
        if 'riak_kv_wm_buckets' in self.resources:
            return "/buckets"

    @lazy_property
    def riak_kv_wm_raw(self):
        return self.resources.get('riak_kv_wm_raw') or "/riak"

    @lazy_property
    def riak_kv_wm_link_walker(self):
        return self.resources.get('riak_kv_wm_linkwalker') or "/riak"

    @lazy_property
    def riak_kv_wm_mapred(self):
        return self.resources.get('riak_kv_wm_mapred') or "/mapred"

    @lazy_property
    def riak_kv_wm_ping(self):
        return self.resources.get('riak_kv_wm_ping') or "/ping"

    @lazy_property
    def riak_kv_wm_stats(self):
        return self.resources.get('riak_kv_wm_stats') or "/stats"

    @lazy_property
    def riak_solr_searcher_wm(self):
        return self.resources.get('riak_solr_searcher_wm')

    @lazy_property
    def riak_solr_indexer_wm(self):
        return self.resources.get('riak_solr_indexer_wm')

    @lazy_property
    def riak_kv_wm_counter(self):
        return self.resources.get('riak_kv_wm_counter')

    @lazy_property
    def resources(self):
        return self.get_resources()


def mkpath(*segments, **query):
    """
    Constructs the path & query portion of a URI from path segments
    and a dict.
    """
    # Remove empty segments (e.g. no key specified)
    segments = [s for s in segments if s is not None]
    # Join the segments into a path
    pathstring = '/'.join(segments)
    # Remove extra slashes
    pathstring = re.sub('/+', '/', pathstring)

    # Add the query string if it exists
    _query = {}
    for key in query:
        if query[key] in [False, True]:
            _query[key] = str(query[key]).lower()
        elif query[key] is not None:
            if isinstance(query[key], unicode):
                _query[key] = query[key].encode('utf-8')
            else:
                _query[key] = query[key]

    if len(_query) > 0:
        pathstring += "?" + urlencode(_query)

    if not pathstring.startswith('/'):
        pathstring = '/' + pathstring

    return pathstring
