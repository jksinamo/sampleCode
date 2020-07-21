import unittest
import webcrawl
from selenium import webdriver
import tldextract


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver1 = webdriver.Chrome(
            executable_path="/Users/joshuakevinsinamo/PycharmProjects/"
                            "hyperlinkminer/chromedriver1",
            options=chrome_options)


class TestGetContent(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGetContent, self).__init__(*args, **kwargs)
        self.link_content_present = \
            'http://sites.google.com/view/crawlingtestunit1'
        self.link_content_absent  = \
            'http://sites.google.com/view/crawlingtestunit2'

    def test_scrape_with_content_present(self):

        self.assertEqual(webcrawl.get_contents(driver1,
                                               self.link_content_present),

                         'Crawling Test Unit 1\nThis is the content '
                         'to scrape\nlink',

                         "Output should be: 'Crawling Test Unit 1\nThis is the "
                         "content to scrape\nlink'")

    def test_scrape_with_no_content_present(self):

        self.assertEqual(webcrawl.get_contents(driver1,
                                               self.link_content_absent),
                         '', "should be '' or empty")


class TestGetLinks(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGetLinks, self).__init__(*args, **kwargs)
        self.crawlingTestUnit1 = webcrawl.get_links(
            driver1, 'http://sites.google.com/view/crawlingtestunit1')
        self.crawlingTestUnit2 = webcrawl.get_links(
            driver1, 'http://sites.google.com/view/crawlingtestunit2')

    def test_get_links_length_from_website_with_links(self):
        self.assertEqual(len(self.crawlingTestUnit1), 1,
                         "Length should be : 1")

    def test_get_links_length_from_website_with_no_links(self):
        self.assertEqual(len(self.crawlingTestUnit2),
                         0,
                         "Length should be : 0")

    def test_get_links_name_from_website_with_links(self):
        self.assertIn('google', '; '.join(self.crawlingTestUnit1),
                      "'google' should be in the link (this link has "
                      "redirection)")

    def test_get_links_name_from_website_with_no_links(self):
        self.assertEqual(self.crawlingTestUnit2,
                         [],
                         "Should be empty")


class TestCheckDirections(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCheckDirections, self).__init__(*args, **kwargs)
        self.source = tldextract.extract(
            'http://sites.google.com/view/crawlingtestunit1')
        self.SDSS = 'http://sites.google.com/view/crawlingtestunit2'
        self.DDSS = 'http://somelink.com'
        self.DDDS = 'http://somelink.edu'
        self.SDDS = 'http://google.edu'

        self.domestic_yes = True
        self.domestic_no = False

    def test_domestic_is_TRUE_and_same_domain_same_suffix(self):
        self.assertEqual(webcrawl.direction_is_OK(
            self.source, self.SDSS, self.domestic_yes), True,
            "Output should be: True")

    def test_domestic_is_TRUE_and_same_domain_different_suffix(self):
        self.assertEqual(webcrawl.direction_is_OK(
            self.source, self.SDDS, self.domestic_yes), True,
            "Output should be: True")

    def test_domestic_is_TRUE_and_different_domain_same_suffix(self):
        self.assertEqual(webcrawl.direction_is_OK(
            self.source, self.DDSS, self.domestic_yes), True,
            "Output should be: True")

    def test_domestic_is_TRUE_and_different_domain_different_suffix(self):
        self.assertEqual(webcrawl.direction_is_OK(
            self.source, self.DDDS, self.domestic_yes), True,
            "Output should be: True")

    def test_domestic_is_FALSE_and_same_domain_same_suffix(self):
        self.assertEqual(webcrawl.direction_is_OK(
            self.source, self.SDSS, self.domestic_no), False,
            "Output should be: False")

    def test_domestic_is_FALSE_and_same_domain_different_suffix(self):
        self.assertEqual(webcrawl.direction_is_OK(
            self.source, self.SDDS, self.domestic_no), True,
            "Output should be: True")

    def test_domestic_is_False_and_different_domain_same_suffix(self):
        self.assertEqual(webcrawl.direction_is_OK(
            self.source, self.DDSS, self.domestic_no), True,
            "Output should be: True")

    def test_domestic_is_False_and_different_domain_different_suffix(self):
        self.assertEqual(webcrawl.direction_is_OK(
            self.source, self.DDDS, self.domestic_no), True,
            "Output should be: True")


class TestCheckContents(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCheckContents, self).__init__(*args, **kwargs)
        self.content = "please check this body of text"
        self.single_word_MATCH = "'please'"
        self.single_word_NOTMATCH = "'cchheecckk'"
        self.multiple_words_MATCH = "('please' and 'check')"
        self.multiple_words_NOTMATCH = "('whatever1' or 'whatever2')"
        self.chunk_MATCH = "'please check this body of text'"
        self.chunk_NOTMATCH = "'please check or dont'"

    def test_single_word_MATCH(self):
        self.assertEqual(webcrawl.content_is_OK(self.content,
                                                self.single_word_MATCH),
                         True,
                         'Output should be: True')

    def test_single_word_NOTMATCH(self):
        self.assertEqual(webcrawl.content_is_OK(self.content,
                                                self.single_word_NOTMATCH),
                         False,
                         'Output should be: False')

    def test_multiple_words_MATCH(self):
        self.assertEqual(webcrawl.content_is_OK(self.content,
                                                self.multiple_words_MATCH),
                         True,
                         'Output should be: True')

    def test_multiple_words_NOTMATCH(self):
        self.assertEqual(webcrawl.content_is_OK(self.content,
                                                self.multiple_words_NOTMATCH),
                         False,
                         'Output should be: False')

    def test_multiple_word_NOTMATCH(self):
        self.assertEqual(webcrawl.content_is_OK(self.content,
                                                self.multiple_words_NOTMATCH),
                         False,
                         'Output should be: False')

    def test_chunk_MATCH(self):
        self.assertEqual(webcrawl.content_is_OK(self.content,
                                                self.chunk_MATCH),
                         True,
                         'Output should be: True')

    def test_chunk_NOTMATCH(self):
        self.assertEqual(webcrawl.content_is_OK(self.content,
                                                self.chunk_NOTMATCH),
                         False,
                         'Output should be: False')

    def test_NO_QUERY(self):
        self.assertEqual(webcrawl.content_is_OK(self.content),
                         True,
                         'Output should be: True')


if __name__ == '__main__':

    unittest.main()
