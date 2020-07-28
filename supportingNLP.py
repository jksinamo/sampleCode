from nltk import FreqDist, word_tokenize, pos_tag
from collections import defaultdict
from stanza.server import CoreNLPClient
import pandas as pd
import io
from selenium import webdriver
import pytesseract
from PIL import Image


# Word tokenizer to analyze content using NLP. This will return
#   the composition of the text by word tags as described by NLTK
#   and also the frequency of that particular tag.
# seed    : source of content
# content : a raw string text content of the seed (or website)
#         : content doesn't have to be tokenized / organized
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


# Extract phrases based on pattern / tag of the phrase
# Pattern choice : NP, VP, etc (please check python-stanza documentation)
# texts = list of texts
# classpath = location of your corenlp folder
# annotators = type of annotator
def extract_phrases(texts, pattern = "NP",
                    classpath = "/stanford-corenlp-4.0.0/*",
                    annotators="tokenize,ssplit,pos,lemma,parse"):

    # In case client stuck----
    # kill localhost:9000
    #    sudo lsof -n -i4TCP:9000
    #    <get the PID>
    #    kill -9 <PID>
    with CoreNLPClient(timeout=30000, memory='2G',
                       classpath=classpath, threads=2) as client:

        for text in texts:

            matches = client.tregex(text, pattern, annotators=annotators)
            print("\n".join(["\t"+sentence[match_id]['spanString'] for sentence in
                  matches['sentences'] for match_id in sentence]))


# Take a screenshot of a webpage and translate the image into text
# url : website url (string)
# path_to_webdriver = absolute location to your chromedriver
def webpage_screenshot_to_text(url, path_to_webdriver):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")

    # window size set to 2000 x 8000 to capture
    #    as much screen as possible

    chrome_options.add_argument("--window-size=2000,8000")
    driver = webdriver.Chrome(
        executable_path=path_to_webdriver,
        options=chrome_options)

    driver.get(url)
    img = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
    driver.quit()

    return pytesseract.image_to_string(img, lang="eng")





