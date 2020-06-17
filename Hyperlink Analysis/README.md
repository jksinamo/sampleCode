**Status:** Under development. webcrawl works as intended, but need to fix the domestic outlinks filter

**Disclaimer:** This is NOT the entirity of a kit for hyperlink analysis, rather a crawler to fetch an appropriate set of data for calculations of hyperlink analysis. Such kit for calculations of network centralities and measurements are available via NetworkX package in Python which accept the output resulted from my code. Also, I'm experimenting on using outlinks only and compensating it by enabling crawling for virtually unlimited number of steps (depending on time and CPU available for you). There are similar tool availabe via web interface at issuecrawler.net or Voson Uberlink, however they're limited to 4 steps crawling (from the initial seed links).

In addition to libraries, you will also need chromedriver in the version of your Chrome browser. 
Available at:https://chromedriver.chromium.org/

**Dummy sites used to test:**
- https:sites.google.com/view/crawlingtestunit1
- https:sites.google.com/view/crawlingtestunit2
- https:sites.google.com/view/crawlingtestunit3

**What's next :**
- Fix domestic outlinks filter
- Adding more test cases to webcrawl_test
- Testing it on anti-vaccine online community
