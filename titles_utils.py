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



def longestSubstringFinder(string1, string2):
    from difflib import SequenceMatcher

    match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
    if match is None or match.size==0:
        return ''
    return string1[match.a: match.a + match.size].strip()




def detect_suffix(page_title, saved_str):
    saved_str = saved_str.strip()
    t = page_title.lower()
    search_location = 0
    last_word = saved_str.split()[-1]
    while True:
        search_location = t.find(last_word, search_location)
        if search_location==-1:
            return page_title
        my_string = page_title[:search_location + len(last_word)]
        my_string = do_interesting_string_processing(my_string)
        common = longestSubstringFinder(my_string, saved_str)
        if common.strip()==saved_str:
            loc = search_location + len(last_word)
            while loc<len(page_title) and page_title[loc]!=' ':
                loc+=1
            return page_title[:loc]
        search_location+=1


from utils import give_me_raw_html_content



def give_me_page_title(fname):
    html_content = give_me_raw_html_content(fname)
    soup         = BeautifulSoup(html_content, "lxml")
    page_title   = soup.title.string
    saved_title = page_title
    # print("page title is ", saved_title)
    # page_title = page_title.lower()
    page_title = do_interesting_string_processing(saved_title)
    for s in soup(['script', 'style', 'title', 'head', 'a']):
        s.decompose()
    max_len = 0
    saved_str = ""
    for s in soup.stripped_strings:
        s = do_interesting_string_processing(s)
        if len(s.split())>100:
            continue
        # print(s)
        common = longestSubstringFinder(s, page_title)
        if len(common)>max_len:
            max_len = len(common)
            saved_str = common
    suffix_str = detect_suffix(saved_title, saved_str)
    suffix_str = do_interesting_string_processing(suffix_str)
    # print("suffix str ", suffix_str)
    # s2 = give_me_distinct_strings(soup)
    # print("\n".join(s2))
    # return max_intersected_title(suffix_str, s2)
    # print("suffix is ", suffix_str)
    # print("saved string is ", saved_str)
    candidate = give_me_prefix(html_content, soup, suffix_str, saved_str)
    if candidate is None:
        return saved_title
    return candidate
    return saved_title + '\n' + candidate
    last_word = saved_str.split()[-1]
    t = saved_title.lower()
    loc = t.rfind(last_word)
    if loc==-1:
        return saved_title
    loc+=len(last_word)
    while loc<len(saved_title) and saved_title[loc]!=' ':
        loc+=1
    return saved_title + '\n' + saved_title[:loc]
    # return saved_title + '\n' + saved_str


def filter_titles_candidates(content, dict_values):
    content = do_interesting_string_processing(content)
    # dict_candidates = set([s.lower() for s in dict_value])
    output = []
    processed = set([])
    for c in dict_values:
        # print("c is ", c)
        cc = c.lower()
        if cc in processed:
            continue
        modified_c = do_interesting_string_processing(cc)
        count = find_all(content, modified_c)
        # print(count)
        if count>2:
            output.append(c)
        processed.add(cc)
    return output

def max_intersected_title(suffix_title, filtered_answers):
    # print('answers are ', "\n".join(filtered_answers))
    # print(suffix_title)
    # import sys
    # sys.exit(1)
    saved_str = ''
    ans = ''
    my_first = suffix_title.split()[0]
    # print("My first is ", my_first)
    for a in filtered_answers:
        # if a=='Glen Kitchen Chimney 6071 Touch Sensor 60CM 1250m3 SS':
        #     print("Boom")
        saved_a = a
        a = do_interesting_string_processing(a)
        # print("answer is ", a)
        s = longestSubstringFinder(a, suffix_title)
        if len(s.split())==0:
            continue
        current_s = s.split()[0]
        my_first = a.split()[0]
        # if saved_a == 'Glen Kitchen Chimney 6071 Touch Sensor 60CM 1250m3 SS':
        #     print("answer is ")
        #     print(s)
        #     print(my_first)
        #     print(current_s)
        # print(current_s)
        if len(s.strip())>len(saved_str.strip()):
            saved_str = s
            ans = saved_a
    return ans
from htmlworks import give_me_distinct_strings
def give_me_prefix(content, soup, suffix_title, common):
    # print('suffix title ', suffix_title)
    # print("common is ", common)
    page_title = suffix_title
    half = len(common)/2
    page_title = page_title.lower()
    title_words = page_title.split()
    first_title_word = title_words[0]
    rem_words        = title_words[1:]
    d = {}
    # print(first_title_word)
    # print(rem_words)
    for s in soup.stripped_strings:
        s_saved = s
        if len(s.split())>30:
            continue
        s = do_interesting_string_processing(s)
        s = s.split()
        if len(s)==0:
            continue
        s = [ss.lower() for ss in s]
        # print(s)
        current_first = s[0]
        if len(s)>1:
            current_rem   = s[1:]
        else:
            current_rem = s
        # if s_saved=='Voltas 1.5 Ton 5 Star 185LZH Window Air Conditioner':
        #     print("boom")
        #     print(s)
        #     print(current_first)
        #     print(first_title_word)
        #     print(current_rem[0])
        #     print(rem_words[0])
        if current_first in rem_words or (current_first==first_title_word and current_rem[0]==rem_words[0]):
            v = d.get(current_first, [])
            v.append(s_saved)
            d[current_first] = v
    d_keys = set([k for k, v in d.items()])
    index_dict = {}
    # print(d_keys)
    # print("d is ", d)
    d_answers = []
    for v in d.values():
        d_answers.extend(v)
    d_answers = set(d_answers)
    # s2 = give_me_distinct_strings(soup)
    # return max_intersected_title(page_title, s2)
    # print("give me distinct strings ", d_answers)
    # intersected = d_answers.intersection(s2)
    # print("intersection is ", intersected)
    # if len(intersected)>0:
    #     intersected = sorted(intersected, reverse=True, key=lambda k:len(k))
    #     return intersected[0]
    index=-1
    for k in d_keys:
        i = title_words.index(k)
        index_dict[k]=i
    index_sorted = sorted(index_dict.items(), key=lambda kv:kv[1])
    # print("index sorted is ", index_sorted)
    output = []
    for k, v in index_sorted:
        d_answers = d[k]
        # print('answers are ', d_answers)
        filtered_answers = filter_titles_candidates(content, d_answers)
        # print("filtered answers are")
        # print(filtered_answers)
        if len(filtered_answers)>0 and max([len(s) for s in filtered_answers])<half:
            continue
        # print("answers")
        if len(filtered_answers)>0:
            t = max_intersected_title(suffix_title, filtered_answers)
            if len(t)<half:
                continue
            return t
            # return max_intersected_title(suffix_title, filtered_answers)
            # return filtered_answers[0]
    return None

#get min index
def give_me_page_title3(fname):
    html_content = give_me_raw_html_content(fname)
    soup         = BeautifulSoup(html_content, "lxml")
    page_title   = soup.title.string
    saved_title = page_title
    page_title = page_title.lower()
    title_words = page_title.split()
    first_title_word = title_words[0]
    rem_words        = title_words[1:]
    for s in soup(['script', 'style', 'title', 'head', 'a']):
        s.decompose()
    d = {}
    for s in soup.stripped_strings:
        s_saved = s
        if len(s.split())>100:
            continue
        s = s.split()
        s = [ss.lower() for ss in s]
        current_first = s[0]
        if len(s)>1:
            current_rem   = s[1:]
        else:
            current_rem = s
        if current_first in rem_words or (current_first==first_title_word and current_rem[0]==rem_words[0]):
            v = d.get(current_first, 0) + 1
            d[current_first] = v
    d_keys = set([k for k, v in d.items() if v>1])
    index=-1
    for k in d_keys:
        i = title_words.index(k)
        if index==-1 or i<index:
            index=i
    values = " ".join(title_words[index:])
    return page_title + "\n" + values
    d = [k+"\t"+str(v) for k,v in d.items() if v>1]
    d = '\n'.join(d)
    return page_title + "\n" + d
def give_me_page_title2(fname):
    html_content = give_me_raw_html_content(fname)
    soup         = BeautifulSoup(html_content, "lxml")
    page_title   = soup.title.string
    # print(page_title)
    # print("title is "
    #, page_title)
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
