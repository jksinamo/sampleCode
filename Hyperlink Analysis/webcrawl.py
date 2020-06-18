import pandas as pd
from selenium import webdriver
from collections import defaultdict
from multiprocessing import Process
from tldextract import tldextract
from random import shuffle
from nltk import FreqDist, word_tokenize, pos_tag
import tkinter as tk
from tkinter import filedialog
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")


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
def get_content(driver, seed):

    contentsList = []
    for i in seed:
        if i is not None:
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

    domainRequirement = []

    tldSource = (tldextract.extract(source))
    if not withinDomain:
        for i in linksList:
            tldTarget = (tldextract.extract(i))
            # tldSource.subdomain != tldSource.subdomain
            if tldSource.domain.lower() == tldTarget.domain.lower() and \
                    tldSource.suffix.lower() == tldTarget.suffix.lower():

                domainRequirement.append(False)

            else:
                domainRequirement.append(True)
    else:
        domainRequirement = [True for i in range(len(linksList))]

    return domainRequirement


def check_contents(keywords, contentsList, minKeywords):

    contentRequirement = []

    if keywords is not None:
        for j in contentsList:
            count = 0
            for k in keywords:
                if k in j:
                    count += 1
            contentRequirement.append(count >= minKeywords)
    else:
        contentRequirement = [True for j in range(len(contentsList))]

    return contentRequirement


# Filter for the crawler; filtering domestic out-links and contents
# source       = the source of outlinks
# linkslist    = outlinks from the source
# contentsList = contents of the outlinks
# withinDomain = whether to crawl outlinks of same domain with the source
# minKeywords  = minimum number of MATCHING keywords required to be in
#                the text content of a website
# keywords     = words / phrase / sentence need to be present in the content
def crawling_filter(domainRequirement, contentRequirement,
                    linksList, contentsList):

    assert len(linksList) == len(contentsList)

    newLinksList = []; newContentsList = []

    for m, n in zip([d and c for d, c in zip(domainRequirement,
                                             contentRequirement)],
                    range(len(linksList))):
        if m:
            newLinksList.append(linksList[n])
            newContentsList.append(contentsList[n])

    del domainRequirement; del contentRequirement

    assert len(newLinksList) == len(newContentsList)
    return newLinksList, newContentsList


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

    df.to_csv(filename, index=False, sep=',')
    del df


# Preparing and starting webdriver bots for parallel processing
# n_bots : number of parallel process desired (no more than 4 at this time)
def load_bots(n_bots, headless = False):

    # settings for the drivers
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    if headless:
        chrome_options.add_argument("--headless")

    botList = []

    for i in range(1, n_bots + 1):
        botList.append(webdriver.Chrome(
            executable_path="/Users/joshuakevinsinamo/"
                            "PycharmProjects/hyperlinkminer/chromedriver" +
                            str(i), options=chrome_options))

    return botList


# Splitting seed links to n split (depending on # of parallel process)
#   in equal chunk length
# seed_list  = list of seeds to be crawled
# n_split    = number of parallel process
def split_seeds(seed_list, n_split):

    container = seed_list; shuffle(container)

    for i in range(0, n_split):
        yield container[i::n_split]


# Main function for web crawling
# seeds        = list of seed links
# depth        = how deep recursively the crawl will be
# driver       = webdriver bots
# withinDomain = whether it'll crawl out-links within the same domain
# minKeywords  = how many keywords need to match the content
# keywords     = keywords that will filter the crawl
# filename      = the filename of its output
def web_crawler(seeds, depth, driver, withinDomain,
                minKeywords, filename, keywords = None):

    depthCounter = depth
    mainSource = []; mainTarget = []
    mainContent = []; mainDepth = []

    while depth > 0:

        layerSource  = []; layerTarget = []
        layerContent = []; layerDepth  = []

        for seed in seeds:
            links    = get_links(driver, seed)
            contents = get_content(driver, links)

            filteredLinks, filteredContents = \
                crawling_filter(seed, links, contents, withinDomain,
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

    save_files(mainSource, mainTarget, mainContent, mainDepth, filename)

    driver.close()


# No join here so that the main process can complete before child process does
def multiprocess_crawling(seeds, depth, withinDomain, minKeywords, filename,
                          n_bots, headless, keywords = None):

    for i, j, k in zip(load_bots(n_bots, headless),  # by the end of this line,
                                                     #   the bots has been
                                                     #   initiated

                       split_seeds(seeds, n_bots),   # shuffling and splitting
                                                     #   the seed links

                       range(1, n_bots + 1)):        # number of multiprocess
        p = Process(target = web_crawler,
                    args = (j, depth, i, withinDomain, minKeywords, filename
                            + str(k), keywords))
        p.start()                                    # Starting the engine


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


class messageColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def welcome():

    print('\n --------- \n Welcome! \n --------- \n\n'
          'The purpose of this program is to mine links and its contents.\n'
          'Intended users are researchers and for non-profit usages only.\n\n'
          'Please refer to laws regarding to research procedures '
          'and intellectual property & copyright to advance\n')

    while True:

        g = input(f"{messageColor.WARNING}"
                  f"Type OK to proceed or exit to close this program: "
                  f"{messageColor.ENDC}")

        if g.lower() == "OK":
            break

        elif g.lower() == "exit":
            print(f"{messageColor.OKGREEN}\nThank you for coming!{messageColor.ENDC}")
            exit(0)

        else:
            print(f"{messageColor.WARNING}\nPlease type OK to proceed, exit to close"
                  f" this program. If you're not sure about the procedure, "
                  f"please consult with your own legal counsel on your "
                  f"situation and specific legal questions you have.\n"
                  f"{messageColor.ENDC}")
            continue


def select_seed_file():

    print("\nTo start, I'll need few things as specified below:\n"
          "--------------------------------------------------\n")
    root = tk.Tk(); root.withdraw()

    print("1. A csv file of seed links separated by newlines")
    time.sleep(2)
    print("selecting file.....")
    file_path_seed = tk.filedialog.askopenfilename()
    print(f"{messageColor.OKGREEN} --OK\n\n{messageColor.ENDC}")

    return csv_to_list(file_path_seed)


def chromedriver_checker(n_bots):

    root = tk.Tk(); root.withdraw()

    chromedriver_address = []; confirmedBots = 0
    while confirmedBots < n_bots:
        try:
            fpath_chromedriver = tk.filedialog.askopenfilename()
            driver = webdriver.Chrome(executable_path=fpath_chromedriver,
                                          options=chrome_options)
            driver.close()
            chromedriver_address.append(fpath_chromedriver)
            confirmedBots += 1
            print(f"{messageColor.OKGREEN}chromedriver #{confirmedBots} out of "
                  f"{n_bots} works!{messageColor.ENDC}")

        except Exception as e:
            print(f"{messageColor.WARNING}"
                  f"That's not a chromedriver and/or an "
                  f"appropriate version of it{messageColor.ENDC}\n"
                  f"{messageColor.FAIL}"
                  f"{e.args}{messageColor.ENDC}\n")

    return chromedriver_address


def select_content_filters():

    root  = tk.Tk(); root.withdraw()
    fpath_content_filter = tk.filedialog.askopenfilename()

    return csv_to_list(fpath_content_filter)


# TODO
def select_output_filename():
    pass


# TODO
def display_progress_bar():
    pass


# TODO
if __name__ == "__main__":
    pass
