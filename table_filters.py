def find_all_start_tags(s):
    closes = []
    opens = []
    loc=0
    while True:
        loc = s.find("<", loc)
        if loc==-1 or loc==len(s)-1:
            return opens, closes
        start_loc = loc+1
        if s[start_loc]=='/':
            close=""
            start_loc+=1
            while start_loc<len(s) and s[start_loc]!='>':
                close+=s[start_loc]
                start_loc+=1
            if start_loc==len(s):
                return opens, closes
            closes.append(close.strip())
            loc = start_loc+1
            continue
        else:
            open=""
            while start_loc < len(s) and s[start_loc] != '>' and s[start_loc]!=' ':
                open+=s[start_loc]
                start_loc+=1
            if start_loc==len(s):
                return opens, closes
            opens.append(open.strip())
            loc = start_loc+1
            continue

def find_all_end_tags(s):
    pass

def endsBeforeStart(s, intersected):
    loc = 0
    while True:
        loc = s.find("<", loc)
        if loc==-1:
            return False
        loc = loc+1
        if s[loc:].startswith(intersected):
            return False
        if s[loc:].startswith("/"+intersected):
            return True
    # return False
def is_table_row(s):
    # print("Checking table row for ", s)
    s1, s2 = find_all_start_tags(s)
    s1 = set(s1)
    s2 = set(s2)
    intersected  = s1.intersection(s2)
    for i in intersected:
        if endsBeforeStart(s, i):
            # print("Hell Yeah...")
            return True
    return False
    # return len(s1.intersection(s2))>0


def pattern_with_link(p):
    l, r = p
    s1, s2 = find_all_start_tags(l[0] + " " + l[1] + " " + r[0] + " " + r[1])
    if 'a' in s1 or 'a' in s2:
        return True
    return False
