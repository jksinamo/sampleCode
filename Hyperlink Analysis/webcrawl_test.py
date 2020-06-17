import unittest
import webcrawl
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver1 = webdriver.Chrome(
        executable_path="/Users/joshuakevinsinamo/PycharmProjects/"
                        "hyperlinkminer/chromedriver1",
        options=chrome_options)


class TestGetContent(unittest.TestCase):

    def test_scrape_with_content_present(self):

        self.assertEqual(
            webcrawl.get_content(driver1,
            ["https://sites.google.com/view/crawlingtestunit1"]),
            ['Crawling Test Unit 1\nCrawling Test Unit\nThis is the content '
             'to scrape\nlink'],
            "should be ['Crawling Test Unit 1\nCrawling Test Unit\nThis is the "
            "content to scrape]\nlink" )

    def test_scrape_with_no_content_present(self):

        self.assertEqual(
            webcrawl.get_content(driver1,
            ["https://sites.google.com/view/crawlingtestunit2"]),
            [''], "should be [] or empty" )


class TestGetLinks(unittest.TestCase):

    crawlingTestUnit1 = webcrawl.get_links(driver1,
                            "sites.google.com/view/crawlingtestunit1")
    crawlingTestUnit2 = webcrawl.get_links(driver1,
                            "sites.google.com/view/crawlingtestunit1")

    def test_get_links_from_website_with_links_LENGTH(self):
    
        self.assertEqual(len(TestGetLinks.crawlingTestUnit1), 2,
                         "Length should be : 2")

    def test_get_links_from_website_with_links_CONTENT(self):
        self.assertIn(" ".join(str(x) for x in TestGetLinks.crawlingTestUnit1),
                      "crawlingtestunit2",
                      "Should contain crawlingtestunit2")

    def test_get_links_from_website_without_links_LENGTH(self):
        self.assertEqual(len(TestGetLinks.crawlingTestUnit2), 0,
                         "Length should be : 0")

    def test_get_links_from_website_without_links_CONTENT(self):
        self.assertEqual(TestGetLinks.crawlingTestUnit2, [],
                         "content should be : ['']")



class TestCheckDirections(unittest.TestCase):

    # Domestic outlinks = False
    def test_no_domestic_outlinks_and_not_accepting_domestic_outlinks(self):
        self.assertEqual(webcrawl.check_directions("test1.com",
                                                   ["test2.com", "test3.com"],
                                                   False), [True, True],
                         "Output should be: ['False', 'False'] ")

    def test_no_domestic_outlinks_but_accepting_domestic_outlinks(self):
        self.assertEqual(webcrawl.check_directions("test1.com",
                                                   ["test2.com", "test3.com"],
                                                   True), [True, True],
                         "Output should be: ['False', 'False'] ")

    def test_domestic_outlinks_but_not_accepting_domestic_outlinks(self):
        self.assertEqual(webcrawl.check_directions("test1.com",
                                                   ["test1.com", "test3.com"],
                                                   False), [False, True],
                         "Output should be: [False, True]")

    def test_domestic_outlinks_and_accepting_domestic_outlinks(self):
        self.assertEqual(webcrawl.check_directions("test1.com",
                                                   ["test1.com", "test3.com"],
                                                   True), [True, True],
                         "Output should be: [True, True]")


class TestCheckContents(unittest.TestCase):

    def test_no_match_exist_but_positive_minKeywords_(self):

        self.assertEqual(
            webcrawl.check_contents(["content"], ["cont", "tent"], 1),
            [False, False], "Output should be: [False, False]")

    def test_match_exist_and_positive_minKeywords(self):
        self.assertEqual(
            webcrawl.check_contents(["content"], ["cont", "content"], 1),
            [False, True], "Output should be: [False, True]")

    def test_match_exist_but_zero_minKeywords(self):
        self.assertEqual(
            webcrawl.check_contents(["content"], ["cont", "content"], 0),
            [True, True], "Output should be: [True, True]")

    def test_no_match_exist_and_zero_minKeywords(self):
        self.assertEqual(
            webcrawl.check_contents(["content"], ["cont", "tent"], 0),
            [True, True], "Output should be: [True, True]")


class TestCrawlingFilter(unittest.TestCase):

    def test_links_ALL_TRUE_but_content_ALL_FALSE(self):

        self.assertEqual(webcrawl.crawling_filter([True, True],
                                                  [False, False],
                                                  ["test1.com", "test2.com"],
                                                  ["content1", "content2"]),
                         ([], []), "Output should be: ([], [])")

    def test_links_ALL_FALSE_but_content_ALL_TRUE(self):
        self.assertEqual(webcrawl.crawling_filter([False, False],
                                                  [True, True],
                                                  ["test1.com", "test2.com"],
                                                  ["content1", "content2"]),
                         ([], []), "Output should be: ([], [])")

    def test_links_and_contents_MIXED_opposite(self):
        self.assertEqual(webcrawl.crawling_filter([False, True],
                                                  [True, False],
                                                  ["test1.com", "test2.com"],
                                                  ["content1", "content2"]),
                         ([], []), "Output should be: ([], [])")

    def test_links_and_contents_MIXED_identical(self):
        self.assertEqual(webcrawl.crawling_filter([False, True],
                                                  [False, True],
                                                  ["test1.com", "test2.com"],
                                                  ["content1", "content2"]),
                         (["test2.com"], ["content2"]),
                         "Output should be: (['test2.com'], ['content2'])")

    def test_empty(self):
        self.assertEqual(webcrawl.crawling_filter([], [], [], []),
                         ([], []),
                         "Output should be: (['test2.com'], ['content2'])")
        
        
class TestSplitSeeds(unittest.TestCase):

    def test_equal_list_length(self):

        for i in webcrawl.split_seeds([1, 2, 3, 4], 4):
            self.assertEqual(len(i), 1, "All length should be 1")

    def test_differing_list_length_1(self):

        for i in webcrawl.split_seeds([1, 2, 3], 4):
            self.assertTrue(len(i) == 1 or len(i) == 0 ,
                            "All length should be 1 or 0")
        
        
# TODO
class TestWordCounter(unittest.TestCase):
    pass


if __name__ == '__main__':

    # MORE WILL BE ADDED ABOVE
    unittest.main()
    driver1.close()

