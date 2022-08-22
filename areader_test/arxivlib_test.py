from areader.arvxivlib import *

import unittest

class ArxvilibTest(unittest.TestCase):
    def test_urlgen(self):

        page_url = "http://export.arxiv.org/api/query?search_query=cat:astro-ph.SR+OR+cat:astro-ph.EP+OR+cat:physics.comp-ph+OR+cat:cs.DC&id_list=&sortBy=submittedDate&sortOrder=descending&start="

        cats = ["astro-ph.SR","astro-ph.EP","physics.comp-ph","cs.DC"]

        purl = get_query_url(cats)

        self.assertEqual(page_url, purl)