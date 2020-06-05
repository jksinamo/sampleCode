import pandas as pd
from selenium import webdriver
from collections import defaultdict
from multiprocessing import Process
from tldextract import tldextract


def webCrawler(seeds, driver, depth, withinDomain, filename,
               keywords = ""):

    mainSource = []; mainTarget = []; mainContent = []
    while depth > 0:

        layerSource = []; layerTarget = []; layerContent = []
        for seed in seeds:

            currentSource, currentTarget, currentContent = \
                linkFilter(seed, getLinks(driver, seed), driver, keywords,
                           withinDomain)

            layerSource.extend(currentSource)
            layerTarget.extend(currentTarget)
            layerContent.extend(currentContent)

        mainSource.extend(layerSource)
        mainTarget.extend(layerTarget)
        mainContent.extend(layerContent)

        webCrawler(layerTarget, driver, depth - 1,
                   withinDomain, filename, keywords)

    df = pd.DataFrame({"source"  : mainSource,
                       "target"  : mainTarget,
                       "content" : mainContent})

    df.to_csv(filename, index = False, sep='\t'); del df


# driver : webdriver object
# seed   : a string of a link
def getLinks(driver, seed):
    candidateLinks = []
    try:
        driver.get(seed)

        candidateLinks = [str(link.get_attribute("href")) for link in
                          driver.find_elements_by_partial_link_text("")]

    except Exception as e:
        print(e.args)

    return candidateLinks


# source          : a string
# candidateTarget : a list of hyperlinks inside the source
# keywords        : a string that will be checked
def linkFilter(source, candidateTarget, driver, keywords , withinDomain = False):

    filteredSource = []; filteredTarget = []; targetContent = []
    content = ''

    if withinDomain is False:
        for candidate in candidateTarget:

            tldSource = (tldextract.extract(source))
            tldTarget = (tldextract.extract(candidate))

            try:
                driver.get(candidate)
                content = driver.find_element_by_tag_name("body").text

            except Exception as e2:
                print(e2.args)

            if (tldSource.domain != tldTarget.domain and
                tldSource.suffix  != tldTarget.suffix  and
                tldSource.subdomain != tldSource.subdomain) and \
                    sum([True for key in keywords if key in content]) == len(
                keywords):

                filteredSource.append(source)
                filteredTarget.append(candidate)
                targetContent.append(content)

    elif withinDomain is True:
        for candidate in candidateTarget:
            try:
                driver.get(candidate)
                content = driver.find_element_by_tag_name("body").text

            except Exception as e3:
                print(e3.args)

            filteredSource.append(source)
            filteredTarget.append(candidate)
            targetContent.append(content)

    return filteredSource, filteredTarget, targetContent


if __name__ == "__main__":

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--headless")

    driver1 = webdriver.Chrome(
        executable_path="/Users/joshuakevinsinamo/PycharmProjects/"
                        "hyperlinkminer/chromedriverA", options=chrome_options)

    '''
    driver2 = webdriver.Chrome(
    executable_path="/Users/joshuakevinsinamo/PycharmProjects/"
                    "hyperlinkminer/chromedriverB", options=chrome_options)

    # change executable path to your absolute path to the third driver
    driver3 = webdriver.Chrome(
    executable_path="/Users/joshuakevinsinamo/PycharmProjects/"
                    "hyperlinkminer/chromedriverC", options=chrome_options)

    # change executable path to your absolute path to the fourth driver
    driver4 = webdriver.Chrome(
    executable_path="/Users/joshuakevinsinamo/PycharmProjects/"
                    "hyperlinkminer/chromedriverD", options=chrome_options)
    '''
    seeds1 = ["http://umich.edu"]
    p1 = Process(target = webCrawler,
                 args = (seeds1, driver1, 1, False, "firstSet.csv", "all",
                         ["test", "and"]))
    p1.start()

    #driver2.close()
    #driver3.close()
    #driver4.close()

    '''
    p2 = Process(target=webCrawler,
                 args=(seeds, driver1, 1, False, "firstSet.csv", "all",
                       ["test", "and"]))
    p2.start()
    p3 = Process(target=webCrawler,
                 args=(seeds, driver1, 1, False, "firstSet.csv", "all",
                       ["test", "and"]))
    p3.start()
    p4 = Process(target=webCrawler,
                 args=(seeds, driver1, 1, False, "firstSet.csv", "all",
                       ["test", "and"]))
    p4.start()
    '''





