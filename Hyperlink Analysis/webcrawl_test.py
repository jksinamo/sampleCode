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


if __name__ == '__main__':

    # MORE WILL BE ADDED ABOVE
    unittest.main()
    driver1.close()

