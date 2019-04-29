from bs4 import BeautifulSoup
import re
def do_interesting_string_processing(s):
    s = s.lower()
    s = re.sub('[^0-9a-zA-Z]+', ' ', s)
    return " ".join(s.split())

import json
def give_me_page_titles_json(f_loc):
    page_titles = give_me_page_title(f_loc)
    data = {}
    data['titles']=page_titles
    json_data = json.dumps(data)
    return json_data

def give_me_common_list_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return len(result)


def find_all(a_str, sub):
    count=0
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return count
        count+=1
        start += len(sub)


from difflib import  SequenceMatcher
def give_me_longest_substring(candidate, title_tag):
    seqMatch = SequenceMatcher(None, title_tag, candidate)
    match = seqMatch.find_longest_match(0, len(title_tag), 0, len(candidate))
    if match.size==0:
        return 0
    if match.size==len(candidate):
        return len(candidate)
    ans = title_tag[match.a:match.a+match.size]
    while len(ans)>0 and ans[-1]==' ':
        ans = ans[:-1]
    return len(ans)

def filter_boxes_with_once_occurence(content, outputs, title_tag):
    content = do_interesting_string_processing(content)
    results = []
    for output, commonality in outputs:
        modified_output = do_interesting_string_processing(output)
        count = find_all(content, modified_output)
        if count>1:
            results.append((output, commonality, count))
    output = []
    modified_title = do_interesting_string_processing(title_tag)
    for r in results:
        o, c, cc = r
        modified_output = do_interesting_string_processing(o)
        output.append((o, give_me_longest_substring(modified_output, modified_title)))
    output = sorted(output, key=lambda kv:kv[1], reverse=True)
    # print("output ss is ", output)
    output = [item[0] for item in output]
    return output[:min(2, len(output))]
    max_value = max([item[1] for item in output])
    results = [k for k, v in output if v==max_value]
    return results

from utils import give_me_raw_html_content

def give_me_page_title(fname):
    html_content = give_me_raw_html_content(fname)
    soup         = BeautifulSoup(html_content)
    page_title   = soup.title.string
    # print("title is ", page_title)
    page_title = do_interesting_string_processing(page_title)
    title_words = page_title.split()
    # print("title is ", page_title)
    # return
    for s in soup(['script', 'style', 'title', 'head', 'a']):
        s.decompose()
    output = []
    results = set([])
    for s in soup.stripped_strings:
        w = do_interesting_string_processing(s).split()
        if len(w)==0 or len(w)>100:
            continue
        if w[0] in title_words:
            if s in results:
                continue
            output.append((s, give_me_common_list_elements(title_words, w)))
            results.add(s)
    output = sorted(output, reverse=True, key=lambda kv:kv[1])
    # print("input is ", output)
    output = filter_boxes_with_once_occurence(html_content, output, page_title)
    return output