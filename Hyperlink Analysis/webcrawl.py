import pandas as pd
from selenium import webdriver
from collections import defaultdict
from multiprocessing import Process
from tldextract import tldextract


# driver : webdriver object
# seed   : a string of a link
def getLinks(driver, seed):
    linksList = []
    try:
        driver.get(seed)

        linksList = [str(link.get_attribute("href")) for link in
                     driver.find_elements_by_partial_link_text("")]

    except Exception as e:
        print(e.args)

    return linksList


# driver : webdriver object
# seed   : a string of a link
def getContent(driver, seed):

    contentsList = []
    for i in seed:
        if i is not None:
            try:
                driver.get(i)
                contentsList.append(str(driver.find_element_by_tag_name("body")))

            except Exception as e:
                contentsList.append(e.args)
        else:
            contentsList.append("LINK NOT FOUND")

    return contentsList


def crawlingFilter(source, linksList, contentsList, withinDomain,
                   minKeywords, keywords = None):

    assert len(linksList) == len(contentsList)

    domainRequirement  = []
    contentRequirement = []

    newLinksList    = []
    newContentsList = []

    tldSource = (tldextract.extract(source))
    if withinDomain:
        for i in linksList:
            tldTarget = (tldextract.extract(i))

            if tldSource.domain != tldTarget.domain or \
               tldSource.suffix != tldTarget.suffix or \
               tldSource.subdomain != tldSource.subdomain:

                domainRequirement.append(True)

            else:
                domainRequirement.append(False)
    else:
        for i in linksList:
            domainRequirement.append(True)

    if keywords is not None:
        for j in contentsList:
            count = 0
            for k in keywords:
                if k in j:
                    count += 1
            contentRequirement.append(count >= minKeywords)
    else:
        for j in contentsList:
            contentRequirement.append(True)

    for m, n in zip(domainRequirement and contentRequirement,
                    range(len(linksList) - 1)):
        if m:
            newLinksList.append(linksList[n])
            newContentsList.append(contentsList[n])

    del domainRequirement; del contentRequirement

    assert len(newLinksList) == len(newContentsList)
    return newLinksList, newContentsList


def saveFiles(mainSource, mainTarget, mainContent, mainDepth, filename):

    assert len(mainSource) == len(mainTarget) == \
           len(mainContent) == len(mainDepth)

    df = pd.DataFrame({
        "depth" : mainDepth,
        "source": mainSource,
        "target": mainTarget,
        "targetcontent": mainContent})

    df.to_csv(filename, index=False, sep='\t')
    del df


# TODO
def loadBots():
    pass


def webCrawler(seeds, depth, driver, withinDomain,
               minKeywords, keywords, filename):

    depthCounter = depth
    mainSource = []; mainTarget = []
    mainContent = []; mainDepth = []

    while depth > 0:

        layerSource  = []; layerTarget = []
        layerContent = []; layerDepth  = []

        for seed in seeds:
            links    = getLinks(driver, seed)
            contents = getContent(driver, links)

            filteredLinks, filteredContents = \
                crawlingFilter(seed, links, contents, withinDomain,
                               minKeywords, keywords)
            sourceList = [seed for i in range(len(filteredLinks))]
            depthLabel = [depthCounter - depth
                          for i in range(len(filteredLinks))]

            layerSource.extend(sourceList)
            layerTarget.extend(filteredLinks)
            layerContent.extend(filteredContents)
            layerDepth.extend(depthLabel)

        mainSource.extend(layerSource)
        mainTarget.extend(layerTarget)
        mainContent.extend(layerContent)
        mainDepth.extend(layerDepth)

        seeds = layerTarget; depth -= 1

    saveFiles(mainSource, mainTarget, mainContent, mainDepth, filename)


if __name__ == "__main__":

    # sample run

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--headless")

    driver1 = webdriver.Chrome(
        executable_path="/Users/joshuakevinsinamo/PycharmProjects/"
                        "hyperlinkminer/chromedriverA", options=chrome_options)

    seedList = ["https://www.umich.edu"]

    webCrawler(seedList, 1, driver1, False,
               -1, "", "testing1.csv")

    driver1.close()








