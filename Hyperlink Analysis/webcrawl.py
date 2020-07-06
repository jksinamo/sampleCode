import pandas as pd
from selenium import webdriver
from collections import defaultdict
from multiprocessing import Process
import multiprocessing as mp
from tldextract import tldextract
from random import shuffle
from nltk import FreqDist, word_tokenize, pos_tag
import re
import os
import time
from tkinter import messagebox


botsList = []


def csv_to_list(filename):

    with open(str(filename), 'r') as f:
        data = [line.rstrip('\n') for line in f]

    return data


# Get all visible links from a webpage
# driver : webdriver object
# seed   : a string of a link
def get_links(driver, seed):
    linksList = []
    try:
        driver.get(seed)

        linksList = [str(link.get_attribute("href")) for link in
                     driver.find_elements_by_partial_link_text("")]

    except Exception as e:
        print(e.args)

    return linksList


# Get all visible text from a webpage
# driver : webdriver object
# seed   : a string of a link
def get_contents(driver, targets):

    contentsList = []
    for i in targets:
        if "://" in str(i):
            try:
                driver.get(i)
                contentsList.append(
                    str(driver.find_element_by_tag_name("body").text))

            except Exception as e:
                contentsList.append(e.args)
        else:
            contentsList.append("LINK NOT FOUND")

    return contentsList


def check_directions(source, linksList, withinDomain):

    filteredLinks = []

    if not withinDomain:
        tldSource = (tldextract.extract(source))
        for i in linksList:
            tldTarget = (tldextract.extract(i))
            if tldSource.domain.lower() != tldTarget.domain.lower() or \
                    tldSource.suffix.lower() != tldTarget.suffix.lower():

                filteredLinks.append(i)

    else:
        return linksList

    return filteredLinks


# this turns a string query to search for content
# contentsList = string in each website visited
# filename      = from GUI, csv file of a query
def check_contents(contentsList, filename = None):

    if filename is not None:
        filteredContents = []
        with open(filename) as f:
            query = f.read()

        for i in contentsList:
            if eval(re.sub(r"([a-zA-Z]\')", r"\1 in i", query)):
                filteredContents.append(i)
            else:
                filteredContents.append("Query did not match with content")

        return filteredContents
    else:
        return contentsList


# Main function for web crawling
# seeds        = list of seed links
# depth        = how deep recursively the crawl will be
# driver       = webdriver bots
# withinDomain = whether it'll crawl out-links within the same domain
# minKeywords  = how many keywords need to match the content
# keywords     = keywords that will filter the crawl
# filename      = the filename of its output
def web_crawler(seeds, depth, driver, withinDomain,
                container, procnum, filterAddress = None):

    ALLSOURCE  = []
    ALLTARGET  = []
    ALLDEPTH   = []
    ALLCONTENT = []

    trueDepth = depth
    initialNodes = seeds

    while depth > 0:
        layerSource = []; layerTarget = []
        layerContent = []; layerDepth = []

        for seed in seeds:
            filteredLinks = check_directions(
                seed, get_links(driver, seed), withinDomain)
            filteredContents = check_contents(
                get_contents(driver, filteredLinks), filterAddress)

            sourceList = [seed for i in range(len(filteredLinks))]
            depthLabel = [trueDepth - depth + 1 for i in range(len(
                filteredLinks))]

            layerSource.extend(sourceList)
            layerTarget.extend(filteredLinks)
            layerContent.extend(filteredContents)
            layerDepth.extend(depthLabel)

        ALLSOURCE.extend(layerSource)
        ALLTARGET.extend(layerTarget)
        ALLDEPTH.extend(layerDepth)
        ALLCONTENT.extend(layerContent)

        seeds = layerTarget
        depth -= 1

    # information
    ALLSOURCE.extend(["INITIAL SEED" for i in initialNodes])
    ALLTARGET.extend(initialNodes)
    ALLDEPTH.extend([0 for i in initialNodes])
    ALLCONTENT.extend(get_contents(driver, initialNodes))

    container[procnum] = pd.DataFrame({"source" : ALLSOURCE,
                                       "target" : ALLTARGET,
                                       "depth"  : ALLDEPTH,
                                       "targetcontent": ALLCONTENT})

    driver.close()
    driver.quit()


# Saving output in csv format; ready for most network analysis software
#   such as Gephi, Cytoscape, UCINET, etc
# mainSource = list of all source of outlinks
# mainTarget = list of all outlinks
# mainDepth  = depth position of the target / outlinks
# filename    = filename of our outputs
def save_files(mainSource, mainTarget, mainContent, mainDepth, filename):

    assert len(mainSource) == len(mainTarget) == \
           len(mainContent) == len(mainDepth)

    df = pd.DataFrame({
        "depth" : mainDepth,
        "source": mainSource,
        "target": mainTarget,
        "targetcontent": mainContent})

    df.to_csv(filename + '.csv', index=False, sep=',')
    del df


# Preparing and starting webdriver bots for parallel processing
# n_bots : number of parallel process desired (no more than 4 at this time)
def load_bots(n_bots, headless = False):

    # settings for the drivers
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    if headless:
        chrome_options.add_argument("--headless")

    global botsList
    for i in range(1, n_bots + 1):
        botsList.append(webdriver.Chrome(
            executable_path="/Users/joshuakevinsinamo/"
                            "PycharmProjects/hyperlinkminer/chromedriver" +
                            str(i), options=chrome_options))

    return botsList


# Splitting seed links to n split (depending on # of parallel process)
#   in equal chunk length
# seed_list  = list of seeds to be crawled
# n_split    = number of parallel process
def split_seeds(seed_list, n_split):

    container = seed_list; shuffle(container)

    for i in range(0, n_split):
        yield container[i::n_split]


def multiprocess_crawling(seedAddress, depth, withinDomain,
                          n_bots, outputFname, filterAddress = None):

    startTime = time.time()
    seeds = csv_to_list(seedAddress)
    scrambledSeeds = split_seeds(seeds, n_bots)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--mute-audio")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    dirPath = os.path.dirname(os.path.realpath(__file__))

    manager = mp.Manager()
    container = manager.dict()
    jobs = []

    global botsList

    for k in range(1, n_bots + 1):
        botsList.append(webdriver.Chrome(
            executable_path=dirPath + "/chromedriver" + str(k),
            options = chrome_options))
    for i, j in zip(scrambledSeeds, list(range(n_bots))):

        p = Process(target = web_crawler,
                    args = (i, depth, botsList[j], withinDomain,
                            container, j, filterAddress))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()

    data = pd.concat(container.values())
    data.to_csv(outputFname, index = False, sep=',')
    endTime = time.time()
    messagebox.showinfo(message="Your crawl has finished!\n"
                                f"Elapsed time = {endTime - startTime}")


# AUXILIARY FUNCTION
# Word tokenizer to analyze content using NLP. This will return
#   the composition of the text by word tags as described by NLTK
#   and also the frequency of that particular word.
# seed    : source of content
# content : text content of the seed (or website)
def word_counter(seed, content):

    columns = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS",
               "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PRP", "PRP$",
               "RB", "RBR","RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG",
               "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"]

    text_dict = dict(FreqDist(pos_tag(word_tokenize(content.lower()))))
    e = {}
    for k, v in text_dict.items():
        e[v] = e.get(v, [])
        e[v].append(k)

    for i in e.keys():
        d = defaultdict(list)
        for v, k in e[i]:
            d[k].append(v)
        e[i] = dict(d); del d

    f = pd.DataFrame(e).T.sort_index()

    df = f[f.columns.intersection(columns)]
    df = df.dropna(how="all")
    df['index'] = seed

    # break the lists inside DataFrame into text
    df = df.applymap(lambda x:
                     x if not isinstance(x, list)
                     else ';'.join(x) if len(x) else '')
    df['frequency'] = df.index

    return df