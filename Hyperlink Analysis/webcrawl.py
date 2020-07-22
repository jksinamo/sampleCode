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
import config


# Convert csv to list
# filename = absolute path (in str) to your fiilename
def csv_to_list(filename):

    with open(str(filename), 'r') as f:
        data = [line.rstrip('\n') for line in f]

    return data


# Get all links inside a webpage
# driver = webdriver (chrome)
# seed   = string of webpage link
def get_links(driver, seed):
    linksList = []
    try:
        # open the webpage
        driver.get(seed)

        # get all links inside that webpage
        linksList = [str(link.get_attribute("href")) for link in
                     driver.find_elements_by_partial_link_text("")]

    # if website can't be opened, print the error
    except Exception as e:
        print(e.args)

    return linksList


# Get all TEXT content inside a webpage in string
# driver = webdriver (chrome)
# target = website which text content to be extracted
def get_contents(driver, target):

    content = "ERROR"
    if "://" in str(target):
        try:
            driver.get(target)
            content = driver.find_element_by_tag_name("body").text

        except Exception as e:
            print(e.args)

    return content


# Check whether the edge respect the domestic outlink restriction (if any)
# tldSource    = tuple of top domain & suffix name
# target       = string of target link
# withinDomain = user input from tkinter on whether they want domestic outlinks
def direction_is_OK(tldSource, target, withinDomain):

    # if we don't want any domestic outlinks
    if not withinDomain:

        tldTarget = (tldextract.extract(target))

        # check whether website name and website suffix (.com, .edu, etc)
        # are the same
        return tldSource.domain.lower() != tldTarget.domain.lower() or \
            tldSource.suffix.lower() != tldTarget.suffix.lower()

    # if we want domestic outlinks
    # WARNING: THIS WILL MAKE THE PROCESS EXPONENTIALLY LARGER
    else:
        return True


# this turns a string query to search for content
# contentsList = string in each website visited
# filename      = from GUI, csv file of a query
def content_is_OK(content, query = None):

    # Changing string query to evaluable pythonic statement
    # For example :  "('word1' and 'word2') or 'word3'"
    #             :  will be ('word1' in content and 'word2' in content)
    #             :           or 'word3' in content

    if (query is not None
        and eval(re.sub(r"([a-zA-Z0-9]\')", r"\1 in content", query)))\
            or query is None:

        return True

    # if query doesn't match
    else:
        return False


# Main function for web crawling
# seeds        = list of seed links
# depth        = how deep recursively the crawl will be
# driver       = webdriver bot
# withinDomain = whether it'll crawl out-links within the same domain
# edgesDict    = dictonary for edges to be shared between main processes
# nodesDict    = dictionary for nodes to be shared between main processes
# nextSource   = list of potential targets to be shared between sub-processes
# filterAddress = File address of the filter file (string)
def web_crawler(seeds, depth, driver, withinDomain,
                edgesDict, nodesDict, nextSource, query):

    # get contents for all initial seed links
    if depth == 1:
        for i in seeds:
            initialContent = get_contents(driver, i)
            nodesDict[i] = [[0], initialContent]

    for seed in seeds:

        # get toplevel domain & suffix name
        tldSource = (tldextract.extract(seed))
        for i in get_links(driver, seed):

            # if status is OK; stopThis is used to stop the app immediately
            # as tracer (with 5sec max delay estimated)
            if not config.stopThis:
                if (seed, i) in edgesDict:
                    # add weight if the edge is already exist in the edges dict
                    edgesDict[(seed, i)] += 1

                else:
                    # check whether the node is a domestic outlinks
                    # and whether it aligns with the crawling parameter
                    if direction_is_OK(tldSource, i, withinDomain):
                        potentialContent = get_contents(driver, i)

                        # check whether the content fit with query
                        if content_is_OK(potentialContent, query):
                            edgesDict[(seed, i)] = 1

                            # check whether there's duplicate of target
                            if i not in nextSource:
                                nextSource.append(i)

                            # check whether there's duplicate of node
                            if i not in nodesDict:
                                nodesDict[i] = [[depth], potentialContent]
                            else:
                                nodesDict[i][0].append(depth)

            # if tracer indicates that program should stop immediately,
            #   stop with return null
            else:
                return


# Saving output in csv format; ready for most network analysis software
#   such as Gephi, Cytoscape, UCINET, etc
# edgesDict      = dictionary of all directed edges (or relationship)
# nodesDict      = dictionary of all nodes and their contents
# edgesFilename  = .csv filename to save for edgesDict
# nodesFilename  = .csv filename to save for nodesDict
def save_files(edgesDict, nodesDict, edgesFilename, nodesFilename):

    edgesFile = pd.DataFrame(dict(edgesDict), index=[0]).T.reset_index()
    nodesFile = pd.DataFrame(dict(nodesDict)).T.reset_index()

    edgesFile.columns = ["source", "target", "weight"]
    nodesFile.columns = ["site", "depth", "content"]

    edgesFile.to_csv(edgesFilename + '.csv', index=False, sep=',')
    nodesFile.to_csv(nodesFilename + '.csv', index=False, sep=',')

    del edgesFile; del nodesFile


# Splitting seed links to n split (depending on # of parallel process)
#   and minimize difference in length between sets using generator
# seed_list  = list of seeds to be crawled
# n_split    = number of parallel process
def split_seeds(seed_list, n_split):

    container = seed_list; shuffle(container)

    for i in range(0, n_split):
        yield container[i::n_split]


def multiprocess_crawling(seedAddress, depth, withinDomain,
                          n_bots, edgesFilename, nodesFilename,
                          filterAddress = None):

    config.startTime = time.time()
    seeds = csv_to_list(seedAddress)
    scrambledSeeds = split_seeds(seeds, n_bots)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-notifications")
    dirPath = os.path.dirname(os.path.realpath(__file__))

    mainManager = mp.Manager()
    edgesDict = mainManager.dict()
    nodesDict = mainManager.dict()

    for k in range(1, n_bots + 1):
        config.botsList.append(webdriver.Chrome(
            executable_path=dirPath + "/chromedriver" + str(k),
            options = chrome_options))

    trueDepth = depth
    query = None
    if filterAddress is not None:
        with open(filterAddress) as f:
            query = f.read()

    while depth > 0:

        manager = mp.Manager()
        nextSource = manager.list()

        for subList, bot in zip(scrambledSeeds, config.botsList):

            p = Process(target = web_crawler,
                        args = (subList, trueDepth - depth + 1,
                                bot, withinDomain, edgesDict, nodesDict,
                                nextSource, query))
            config.jobs.append(p)
            p.start()

        for proc in config.jobs:
            proc.join()

        scrambledSeeds = split_seeds(nextSource, n_bots)
        depth -= 1

    if not config.stopThis:

        for bot in config.botsList:
            bot.quit()

        save_files(edgesDict, nodesDict, edgesFilename, nodesFilename)

    config.endTime = time.time()

    messagebox.showinfo(message="Your crawl has finished!\n"
                                f"Elapsed time = "
                                f"{config.endTime - config.startTime}")


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



