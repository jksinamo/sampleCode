**Status:** OK

**How to easily run this?** 
- Download the zip of the entire repo
- Make sure you have chrome browser in your computer and four chromedrivers to the version of your chrome browser, I have included them in the folder (if your chrome browser is ver. 83, you don't need to download them). Other versions available at:https://chromedriver.chromium.org/. You can download one and duplicate/copy-paste them 4 times and rename them chromedrivers1 .... chromedrivers4 and put it in the Hyperlink Analysis folder you downloaded from this repo
- Open terminal / command prompt and browse into the Hyperlink Analysis folder
- type: python MainWindow.py 
- A window for the app will appear, you can try few settings for webcrawling. Enjoy! 

![](webcrawl.gif)

**Disclaimer:** This is NOT the entirity of a kit needed for hyperlink analysis, rather a crawler to fetch an appropriate set of data for calculations of hyperlink analysis. Such kit for calculations of network centralities and measurements are available via NetworkX package in Python which accept the output resulted from my code. Also, I'm experimenting on using outlinks only and compensating it by enabling crawling for virtually unlimited number of steps (depending on time and # of CPU you have). There are similar tool availabe via web interface at issuecrawler.net or Voson Uberlink, however they're limited to at most 4 steps crawling (from the initial seed links).

**Dummy sites I created to test functions:**
- https:sites.google.com/view/crawlingtestunit1
- https:sites.google.com/view/crawlingtestunit2
- https:sites.google.com/view/crawlingtestunit3

**What's next :**
- Adding more test cases to webcrawl_test
- Testing it on anti-vaccine online community
