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

def is_table_row(s):
    s1, s2 = find_all_start_tags(s)
    s1 = set(s1)
    s2 = set(s2)
    return len(s1.intersection(s2))>0