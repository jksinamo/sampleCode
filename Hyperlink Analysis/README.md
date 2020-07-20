**Status:** OK

**How to easily run this?** 
- Download the zip of the entire repo
- Make sure you have chrome browser in your computer and four chromedrivers to the version of your chrome browser, I have included them in the folder (if your chrome browser is ver. 83, you don't need to download them). Other versions available at:https://chromedriver.chromium.org/. You can download one and duplicate/copy-paste them 4 times and rename them chromedrivers1 .... chromedrivers4 and put it in the Hyperlink Analysis folder you downloaded from this repo
- Open terminal / command prompt and browse into the Hyperlink Analysis folder
- type: python MainWindow.py 
- A window for the app will appear, you can try few settings for webcrawling. Enjoy! 
![](webcrawl.gif)

**Overview**
![](mainwindow.png)
- "Load your seed file": press the button to browse your seed file
  - Seed file must be in csv format 
- "Crawling depth" : drop-down to select your desired crawling depth. Technically, the limit can be set to unlimited, but at this stage, the limit is set on 10
- "Filter type"
  - Non-domestic: when selected, the program will exclude all the domestic links from the crawl (domestic : toplevel domain name and suffix are the same between source and target; e.g. if google.com has an edge directed to mail.google.com, this edge will be excluded and mail.google.com will also be excluded from nodes list for that particular instance of crawling)
  - Keywords : If you have any desired query to be matched to the text content of your crawl, you can check the box and then the "select filter file" button will be enabled. Acceptable format for the query file is csv with quotation mark surrounding each instance of string. 
    - Sample query 1 (in your csv file): ('test' and 'bool') or 'boolean' 
    - Sample query 2 (in your csv file): 'what' and 'is' or 'this' 
    - Sample query 3 (in your csv file): 'might as well get a sentence' and 'is' or 'this' 
- Number of concurrent crawling : Technically, it can be set to 100, however for the purpose of this testing stage, limit is set to 4
- Edges filename : filename of your edges file
- Nodes filename : filename of your nodes file
   

When the box for disclaimer has been selected, press the "run the crawl" button. You will see this window upon pressing the button:
![](review.png)
Press "yes" to execute the crawl, or if you're unsure of the profile, press "back to previous window". If you need to kill the crawling process immediately, "stop everything" button will be enabled after crawl is executed.

Example on how it looks on Mac:
![](webcrawl.gif)

**Disclaimer:** This is NOT the entirity of a kit needed for hyperlink analysis, rather a crawler to fetch an appropriate set of data for calculations of hyperlink analysis. Such kit for calculations of network centralities and measurements are available via NetworkX package in Python which accept the output resulted from my code. Also, I'm experimenting on using outlinks only and compensating it by enabling crawling for virtually unlimited number of steps (depending on time and # of CPU you have). There are similar tool availabe via web interface at issuecrawler.net or Voson Uberlink, however they're limited to at most 4 steps crawling (from the initial seed links).


**What's next :**
- Adding more test cases to webcrawl_test
- Testing it on anti-vaccine online community
