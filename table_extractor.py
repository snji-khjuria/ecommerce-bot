#TODO: W6 is not working and see if is solvable
from utils import give_me_raw_html_content
from bs4 import BeautifulSoup
def give_me_with_content(tags_content):
    output = []
    for instance in tags_content:
        text = instance.text.strip()
        if len(text)==0:
            continue
        output.append(instance)
    return output

def give_me_value_string(values):
    values_out = []
    for v in values:
        if isinstance(v, (list,)):
            v = ' '.join([vv for vv in v])
        values_out.append(v)
    # print([str(v) for v in sorted(values)])
    attr_values = " ".join([str(v) for v in sorted(values_out)])
    return attr_values

def give_me_values_dict(v):
    d = {}
    for i in v:
        item = d.get(i, 0)+1
        d[i]=item
    output = []
    for k, v in d.items():
        if v>2:
            output.append(k)
    return output


def give_me_possible_replacement_attribs(tags):
    attrib_dict = {}
    for tag in tags:
        # print("tag insance is ")
        # print(tag)
        for k, v in tag.attrs.items():
            k = k.strip()
            v = give_me_value_string(v)
            value = attrib_dict.get(k, [])
            value.append(v)
            attrib_dict[k]=value
    attrib_dict = {k:give_me_values_dict(v) for k, v in attrib_dict.items()}
    # print("attrib dict is ", attrib_dict)
    if len(attrib_dict.keys())==0:
        return []
    pick_max = max([len(v) for v in attrib_dict.values()])
    # print("pick max is ", pick_max)
    if pick_max==0:
        return []
    answer = []
    for k, v  in attrib_dict.items():
        if len(v)==0:
            answer.append(k)
    # print("returning ", answer)
    return answer


def give_me_attrib_specific_tags(tag_instances):
    out_dict = {}
    for instance in tag_instances:
        # print("instance is ", instance)
        tag_attribs = "\t".join(sorted(instance.attrs.keys()))
        # print("Attributes are ", tag_attribs)
        # print("text is ", instance.text)
        value = out_dict.get(tag_attribs, [])
        value.append(instance)
        out_dict[tag_attribs] = value
    values = [v for v in out_dict.values() if len(v)>1]
    return values


def do_corelation_computation(tags_dict):
    replacements = []
    for tag, tag_instances in tags_dict.items():
        attrib_specific_tags = give_me_attrib_specific_tags(tag_instances)
        # for item in attrib_specific_tags:
            # print("BOOM\n\n\n\n")
        for each_attrib_specific_tag in attrib_specific_tags:
            pr = give_me_possible_replacement_attribs(each_attrib_specific_tag)
            if len(pr)>0:
                # print("for tag ", tag)
                # print(len(tag_instances))
                # print(pr)
                replacements.extend(pr)
    return replacements


def give_me_keys(page_loc):
    html_content = give_me_raw_html_content(page_loc)
    soup = BeautifulSoup(html_content, "lxml")
    tags = set([tag.name for tag in soup.find_all()])
    tags_dict = {}
    for t in tags:
        # if t!='a':
        #     continue
        tags_content = soup.find_all(t)
        tags_content = give_me_with_content(tags_content)
        tags_dict[t] = tags_content
    # print(tags_dict.keys())
    # content = tags_dict['span']
    # for i in content:
    #     print(i)
    # print("tags are ", tags)
    correlated_tags = do_corelation_computation(tags_dict)
    answer = sorted(list(set(correlated_tags)))
    if 'class' in answer:
        answer.remove('class')
    return answer
    print("replacements are ", correlated_tags)

def preprocess_html_content(content):
    return (" ".join(content.split())).replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<').replace('&quot;', '"').replace('&nbsp;', ' ')

def give_me_my_html_content(url_loc):
    with open(url_loc, 'r') as f:
        content = f.read()
        # print(content)
        content = preprocess_html_content(content)
        return content
import re
def give_me_modified_content(words_to_replace, s):
    for word in words_to_replace:
        r = word + '=".+?"'
        s = re.sub(r, word+'="id"', s)
    return s



def give_me_brand_new_key(instance):
    t = instance.text.strip()
    if len(t)==0:
        return str(instance)
    whole = str(instance)
    start_loc = whole.find(t)
    end_loc = start_loc + len(t)
    # print("whole is ", whole)
    return whole[:start_loc] + whole[end_loc:]


def work_with_tag_attribs3(all_instances):
    tag_d = {}
    for instance in all_instances:
        # print("instance is ", instance)
        key = give_me_brand_new_key(instance)
        value = tag_d.get(key, [])
        value.append(instance)
        tag_d[key] = value
    tag_d = [v for k, v in tag_d.items() if len(v)>1]
    return tag_d


def work_with_tags_dict2(tags_dict):
    tag_results = {}
    for tag_name, tag_content in tags_dict.items():
        # if tag_name!='td':
        #     continue
        my_tag_dict = {}
        for tag_instance in tag_content:
            # key = give_me_brand_new_key(tag_instance)
            tag_attribs = "\t".join(sorted(tag_instance.attrs.keys()))
            value = my_tag_dict.get(tag_attribs, 0) + 1
            my_tag_dict[tag_attribs] = value
        new_tag_content = []
        for tag_instance in tag_content:
            # print("for instance ", str(tag_instance))
            tag_attribs = "\t".join(sorted(tag_instance.attrs.keys()))
            # print("tag attribs are ", )
            if my_tag_dict[tag_attribs]>1:
                new_tag_content.append(tag_instance)
        # if tag_name=='td':
        #     print("here the results are ", "\n".join([str(t) for t in new_tag_content]))
        new_tag_content = work_with_tag_attribs3(new_tag_content)
        if len(new_tag_content)>0:
            tag_results[tag_name] = new_tag_content
    return tag_results

def isNum(t):
    try:
        t = int(t)
        return True
    except ValueError:
        return False

def find_all_pattern_locs(content, pattern_start):
    output = []
    start = 0
    while True:
        # print(start)
        start = content.find(pattern_start, start)
        if start == -1: return output
        output.append((start, start+len(pattern_start)))
        start += len(pattern_start)

def find_next_pattern_available(content, patterns):
    content = content.strip()
    # print("here content is ", content[:100])
    # for p in patterns:
    #     print("ok")
    #     print(p)
    # print("patterns are ", patterns)
    # import sys
    # sys.exit(1)
    for sp, ep in patterns:
        # print("sp is ", sp)
        loc = content.find(sp)
        str_rem = content[:loc].strip()
        if len(str_rem)==0:
            return (sp, ep)
        if len(str_rem)<3:
            continue
        if str_rem[0]!='<' or str_rem[1]!='/' or str_rem[-1]!='>':
            continue
        str_rem = str_rem[2:-1]
        word_count = len(str_rem.split())
        if word_count==1:
            return (sp, ep)
    # import sys
    # sys.exit(1)
    return None

#values
def find_table(start_loc, pattern, next_pattern, raw_html):
    start = start_loc
    end   = start
    current = start_loc
    p_s, p_e = pattern
    n_s, n_e = next_pattern
    count=0
    while True:
        s_loc = raw_html.find(p_s, current)
        if s_loc==-1 or abs(s_loc-current)>200 or (count>0 and s_loc==current):# or (abs(s_loc-current)==0 and flag_same==True and count>0):
            return raw_html[start:end], current, count
        pattern_end_loc = s_loc + len(p_s)
        # print("pattern end location is ", pattern_end_loc)
        se_loc = raw_html.find(p_e, pattern_end_loc)
        # print("se end loc is ")
        # print(raw_html[se_loc:])
        if se_loc==-1:
            return raw_html[start:end], current, count
        key_diff = abs(se_loc-pattern_end_loc)
        if key_diff>200:
            return raw_html[start:end], current, count
        n_start = se_loc + len(p_e)
        # print("start2 is ")
        # print(raw_html[n_start:])
        raw = raw_html[n_start:].strip()
        # print("raw is ", raw)
        n_loc = raw.find(n_s)
        # print(n_loc)
        if n_loc!=0:
            return raw_html[start:n_start], n_start, count
        pattern_end_loc = n_loc + len(n_s)
        ne_loc = raw.find(n_e, pattern_end_loc)
        # print("end loc is ", ne_loc)
        # print("ans is ", raw[ne_loc:])
        if ne_loc==-1:
            return raw_html[start:n_start], n_start, count
        value_diff = abs(pattern_end_loc-ne_loc)
        # print("value diff is ", value_diff)
        if value_diff>200:
            return raw_html[start:n_start], n_start, count
        value_consumed = ne_loc + len(n_e)
        end = n_start+value_consumed
        # print("I am starting at ")
        # print(raw_html[end:])
        current = end
        count+=1

def parse_table_and_also_filter_key(t):
    table_content, p, next_p = t
    p_s, p_e = p
    next_s, next_e = next_p
    table_out = []
    while(True):
        search_loc = table_content.find(p_s)
        if search_loc==-1:
            return table_out
        table_content = table_content[search_loc+len(p_s):]
        search_loc = table_content.find(p_e)
        if search_loc==-1:
            return table_out
        key = table_content[:search_loc].strip()
        key = preprocess_html_content(key)
        table_content = table_content[search_loc+len(p_e):]
        search_loc = table_content.find(next_s)
        if search_loc==-1:
            return table_out
        table_content = table_content[search_loc+len(next_s):]
        search_loc=table_content.find(next_e)
        if search_loc==-1:
            return table_out
        value = table_content[:search_loc].strip()
        value = preprocess_html_content(value)
        table_content = table_content[search_loc+len(next_e):]
        if len(key)>50 and len(value)>50:
            continue
        table_out.append(key+"\t"+value)

def give_me_first_key(content):
    loc = content.rfind(">")
    if loc==-1:
        return ""
    return content[loc+1:]

def give_me_last_value(content):
    loc = content.find("<")
    if loc==-1:
        return ""
    return content[:loc]


def give_me_complete_table_answer(raw_html, key_pattern, value_pattern):
    start_location = 0
    kp_start, kp_end = key_pattern
    vp_start, vp_end = value_pattern
    output = []
    while True:
        key_loc = raw_html.find(kp_start, start_location)
        if key_loc==-1:
            return output
        # print("I found answer at ", raw_html[key_loc:key_loc+100])
        pattern_end_loc = key_loc+len(kp_start)
        kpend_loc = raw_html.find(kp_end, pattern_end_loc)
        # print("kp end loc is ", raw_html[kpend_loc:kpend_loc+100])
        if kpend_loc==-1:
            return output
        key = raw_html[pattern_end_loc:kpend_loc]
        # print("key is ", key)
        # print("Content is ", raw_html[kpend_loc:kpend_loc+100])
        # print("output is ", output)
        # print("Key I found is ", key)
        # print(raw_html[pattern_end_loc:pattern_end_loc+2000])
        # import sys
        # sys.exit(1)
        pattern_end_loc = kpend_loc+len(kp_end)
        while pattern_end_loc<len(raw_html) and raw_html[pattern_end_loc]==' ':
            pattern_end_loc+=1
        value_loc = raw_html.find(vp_start, pattern_end_loc)
        if value_loc==-1:
            return output
        # print(raw_html[value_loc-100:value_loc])
        # import sys
        # sys.exit(1)
        if value_loc!=pattern_end_loc:
            start_location=key_loc+1
            continue
        pattern_end_loc = value_loc+len(vp_start)
        vpend_loc = raw_html.find(vp_end, pattern_end_loc)
        if vpend_loc==-1:
            return output
        value = raw_html[pattern_end_loc:vpend_loc]
        start_location = vpend_loc+len(vp_end)
        key = preprocess_html_content(key)
        value = preprocess_html_content(value)
        output.append((key, value))
    return output

def give_me_complete_table_answer_for_colon_table(raw_html, key_pattern, value_pattern):
    start_location = 0
    kp_start, kp_end = key_pattern
    vp_start, vp_end = value_pattern
    # print("Key pattern is ", key_pattern)
    # print("Value pattern is ", value_pattern)
    output = []
    patterns = []
    prev_value_end = -1
    while True:
        key_loc = raw_html.find(kp_start, start_location)
        if key_loc==-1:
            return output, patterns
        # print("I found answer at ", raw_html[key_loc:key_loc+100])
        pattern_end_loc = key_loc+len(kp_start)
        kpend_loc = raw_html.find(kp_end, pattern_end_loc)
        # print("kp end loc is ", raw_html[kpend_loc:kpend_loc+100])
        if kpend_loc==-1:
            return output, patterns
        key = raw_html[pattern_end_loc:kpend_loc]
        # print("key is ", key)
        # print("Content is ", raw_html[kpend_loc:kpend_loc+100])
        # print("output is ", output)
        # print("Key I found is ", key)
        # print(raw_html[pattern_end_loc:pattern_end_loc+2000])
        # import sys
        # sys.exit(1)
        pattern_end_loc = kpend_loc+len(kp_end)
        while pattern_end_loc<len(raw_html) and raw_html[pattern_end_loc]==' ':
            pattern_end_loc+=1
        value_loc = raw_html.find(vp_start, pattern_end_loc)
        if value_loc==-1:
            return output, patterns
        # print(raw_html[value_loc-100:value_loc])
        # import sys
        # sys.exit(1)
        if value_loc!=pattern_end_loc:
            start_location=key_loc+1
            continue
        pattern_end_loc = value_loc+len(vp_start)
        vpend_loc = raw_html.find(vp_end, pattern_end_loc)
        if vpend_loc==-1:
            return output, patterns
        value = raw_html[pattern_end_loc:vpend_loc]
        start_location = vpend_loc+len(vp_end)
        key = preprocess_html_content(key)
        value = preprocess_html_content(value)
        output.append((key, value))
        # print("Adding ", (key, value))
        if prev_value_end!=-1:
            patterns.append(raw_html[prev_value_end:key_loc])
        # print("patternsa re ", patterns)
        prev_value_end = vpend_loc

    return output, patterns


def give_me_kv_patterns(raw_html, table_patterns):
    output_tables = []
    for i, p in enumerate(table_patterns):
        sp, ep = p
        # if p!=('<td class="attrLabels">', '</td>'):
        #     continue
        # print("pattern is ", p)
        # print("calling with pattern ", sp, " and ", ep)
        pattern_locs = find_all_pattern_locs(raw_html, sp)
        if len(pattern_locs)>100:
            continue
        # print("pattern locs are ", len(pattern_locs))
        rem_patterns = table_patterns[:i] + table_patterns[i+1:]
        # print("rem patterns are ", rem_patterns)
        # rem_patterns = table_patterns
        table_end_location = -1
        ii=0
        for start_loc, end_loc in pattern_locs:
            if start_loc<table_end_location:
                continue
            table_end_location = start_loc
            content = raw_html[end_loc:]
            ep_loc = content.find(ep)
            if ep_loc==-1:
                continue
            content = content[ep_loc+len(ep):]
            next_pattern = find_next_pattern_available(content, rem_patterns)
            # print("content is ", content[:100])
            if next_pattern is None or next_pattern==p:
                continue
            table, temp_end_loc, count_rows = find_table(start_loc, p, next_pattern, raw_html)
            # print("content is ", content)
            # print(table)
            if table is not None and count_rows>1:
                output_tables.append((table, p, next_pattern))
                table_end_location = temp_end_loc

    return output_tables


def give_me_some_patterns(raw_html, table_patterns):
    output_tables = []
    for i, p in enumerate(table_patterns):
        sp, ep = p
        # print("pattern is ", p)
        # print("calling with pattern ", sp, " and ", ep)
        pattern_locs = find_all_pattern_locs(raw_html, sp)
        if len(pattern_locs)>100:
            continue
        # print("pattern locs are ", len(pattern_locs))
        # rem_patterns = table_patterns[:i] + table_patterns[i+1:]
        rem_patterns = [table_patterns[i]]
        table_end_location = -1
        ii=0
        for start_loc, end_loc in pattern_locs:
            if start_loc<table_end_location:
                continue
            table_end_location = start_loc
            content = raw_html[end_loc:]
            ep_loc = content.find(ep)
            if ep_loc==-1:
                continue
            content = content[ep_loc+len(ep):]
            next_pattern = find_next_pattern_available(content, rem_patterns)
            # print("content is ", content[:100])
            if next_pattern is None:
                continue
            table, temp_end_loc, count_rows = find_table(start_loc, p, next_pattern, raw_html)
            # print("content is ", content)
            # print(table)
            if table is not None and count_rows>1:
                output_tables.append((table, p, next_pattern))
                table_end_location = temp_end_loc
    return output_tables


def give_me_filtered_patterns(output_tables):
    table_results_dictionary = {}
    for table in output_tables:
        parsed_table = parse_table_and_also_filter_key(table)
        if len(parsed_table)==0:
            continue
        table_candidate, p, next_p = table
        key = (p, next_p)
        value = table_results_dictionary.get(key, [])
        value.extend(parsed_table)
        table_results_dictionary[key] = value
    # print("total tables are ", table_results_dictionary)
    filtered_patterns = [k for k, v in table_results_dictionary.items() if len(v)>1]
    # print("Filtered patterns are ", filtered_patterns)
    # tuples = []
    return filtered_patterns

def give_me_table_content_from_patterns(filtered_patterns, raw_html):
    output = []
    for pattern in filtered_patterns:
        # print("pattern is ")
        # print(pattern)
        key_pattern, value_pattern = pattern
        complete_table_content = give_me_complete_table_answer(raw_html, key_pattern, value_pattern)
        complete_table_content = filter_table_rows(complete_table_content)
        complete_table_content = modify_table_keys(complete_table_content)
        complete_table_content = set(complete_table_content)
        if not istable(complete_table_content):
            continue
        complete_table_content = remove_html_from_tuples(complete_table_content)
        output.extend(complete_table_content)
        # table = "\n".join([k+"\t"+v for k, v in complete_table_content])
        # print("table is ")
        # print(table)
        # tuples.extend(complete_table_content)
        # output+=table+"\nNextTable\tNextTable\n\n"
    return output


import re
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def remove_html_from_tuples(complete_table_content):
    output = []
    for k, v in complete_table_content:
        k = cleanhtml(k)
        v = cleanhtml(v)
        output.append([k, v])
    return output

def give_me_table_content_colon_from_patterns(filtered_patterns, raw_html):
    output = []
    for pattern in filtered_patterns:
        # print("pattern is ")
        # print(pattern)
        key_pattern, value_pattern = pattern
        complete_table_content, inside_patterns = give_me_complete_table_answer_for_colon_table(raw_html, key_pattern, value_pattern)
        inside_patterns_set = set(inside_patterns)
        complete_table_content = filter_table_rows(complete_table_content)
        complete_table_content = set(complete_table_content)
        # print("Complete table content is ")
        # print(complete_table_content)
        if not istable_with_colon(complete_table_content, inside_patterns, inside_patterns_set):
            continue
        # print("yoyo")
        complete_table_content = modify_table_keys(complete_table_content)
        complete_table_content = remove_html_from_tuples(complete_table_content)
        output.extend(complete_table_content)
        # table = "\n".join([k+"\t"+v for k, v in complete_table_content])
        # print("table is ")
        # print(table)
        # tuples.extend(complete_table_content)
        # output+=table+"\nNextTable\tNextTable\n\n"
    return output



def give_me_page_tables(page_loc):
    words_to_replace = give_me_keys(page_loc)
    html_content = give_me_my_html_content(page_loc)
    html_content = give_me_modified_content(words_to_replace, html_content)
    soup = BeautifulSoup(html_content, "lxml")
    tags = set([tag.name for tag in soup.find_all()])
    tags_dict = {}
    for t in tags:
        tags_content = soup.find_all(t)
        tags_dict[t] = tags_content
    # attrib_tags_dict = work_with_tags_dict(tags_dict)
    attrib_tags_dict2 = work_with_tags_dict2(tags_dict)
    total_tables = 0
    table_patterns = []
    for k, tables in attrib_tags_dict2.items():
        for table in tables:
            saved_table = table
            table = [t.text for t in table]
            tt    = [str(t) for t in saved_table]
            table = [t for t in table if len(t)<100]
            num_flag = all([isNum(t) for t in table])
            total_values = len(set(table))
            table = " ".join(table).strip()
            # print(len(table)>0 and not num_flag and total_values>1)
            if len(table)>0  and not num_flag and total_values>1: #and max_table_value<800
                for row in saved_table:
                    text = row.text.strip()
                    html_row = str(row)
                    if len(text)>0:
                        start_index = html_row.find(text)
                        end_index = start_index + len(text)
                        start = html_row[:start_index].strip()
                        end = html_row[end_index:].strip()
                        table_patterns.append((start, end))
                        break

    raw_html = give_me_raw_html_content(page_loc)
    raw_html = give_me_modified_content(words_to_replace, raw_html)
    output_tables = give_me_kv_patterns(raw_html, table_patterns)
    # print("output tables are ", output_tables)
    filtered_patterns = give_me_filtered_patterns(output_tables)
    # print("patterns are ", filtered_patterns)
    output = give_me_table_content_from_patterns(filtered_patterns, raw_html)
    # print("output is ", output)
        # print("Boom")
    # tuples = set(tuples)
    some_patterns = give_me_some_patterns(raw_html, table_patterns)
    filtered_patterns = give_me_filtered_patterns(some_patterns)
    # print("Some patterns are ", filtered_patterns)
    some_table_output = give_me_table_content_colon_from_patterns(filtered_patterns, raw_html)
    if len(some_table_output)>0:
        output.extend(some_table_output)
    # if len(some_table_output)!=0:
    #     output+="\nNextTable\tNextTable\n"+some_table_output
    # print("total tables output is ", len(output_tables))
    # print("output is ", output)
    # tuples = "\n".join(k+"\t"+v for k, v in tuples)
    return output


def filter_table_rows(complete_table_content):
    return [(k, v) for k, v in complete_table_content if len(v)>0 and len(k)>0 and len(v.split())<10]
def modify_table_keys(complete_table_content):
    output = []
    for k, v in complete_table_content:
        k = k.strip()
        v = v.strip()
        if len(k)>0 and k[-1]==':':
            k = k[:-1].strip()
        if len(v)>0 and v[0]==':':
            v = v[1:].strip()
        output.append((k, v))
    return output

from table_filters import is_table_row
def istable_with_colon(complete_table_content, inside_patterns, inside_patterns_set):
    # print("table row is ", inside_patterns_set)
    if abs(len(inside_patterns_set)-len(inside_patterns))>=1 and is_table_row(list(inside_patterns_set)[0]):
        return True
    if len(complete_table_content)<2:
        return False
    start_value = set([v[0] for k, v in complete_table_content if len(v)>0])
    end_key = set([k[-1] for k, v in complete_table_content if len(k)>0])
    if ':' in start_value or ':' in end_key:
        return True
    return False

def istable(complete_table_content):
    if len(complete_table_content)<2:
        return False
    last_char_value_list = set([v[-1] for k, v in complete_table_content])
    # last_char_key_list = set([k[-1] for k, v in complete_table_content])
    max_key_value = max([len(k) for k, v in complete_table_content])
    if len(last_char_value_list)<=1 or max_key_value<4 or len(complete_table_content)<2:
        return False
    return True
