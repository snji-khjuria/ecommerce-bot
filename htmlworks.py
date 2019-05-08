def give_me_attr_key(d):
    key=""
    for k, v in d.items():
        if k!='class':
            continue
        if isinstance(v, list):
            v = "_".join(sorted(v))
        key+=k+"_"+v
    return key

def give_me_distinct_strings(soup):
    d = {}
    for tag in soup.find_all():
        key = give_me_attr_key(tag.attrs)
        d[key] = 1 + d.get(key, 0)

    output = []
    for tag in soup.find_all():
        key = give_me_attr_key(tag.attrs)
        content = " ".join(tag.text.split()).strip()
        if d[key]==1 and len(content.split())<40 and len(content)>0:
            output.append(content)
    return list(set(output))