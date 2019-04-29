import csv

def read_urls_tsv(fname):
    output = []
    with open(fname, 'r', encoding="utf16") as f:
        # print("f is ", f)
        next(f)
        reader = csv.reader(f, delimiter='\t')
        for fname, url in reader:
            output.append((fname, url))
    return output



def write_str_to_file(f_loc, s):
    with open(f_loc, 'w') as f:
        f.write(s)