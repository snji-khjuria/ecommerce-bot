pages_loc  = '/home/maulik/Desktop/textDetection/text-detection-ctpn/main/data/diffbot_dataset/table_pages/pages'
urls_loc   = '/home/maulik/Desktop/textDetection/text-detection-ctpn/main/data/diffbot_dataset/table_urls.tsv'
out_dir = '/home/maulik/Desktop/textDetection/text-detection-ctpn/main/data/diffbot_dataset/csv_outs'

from file_utils import read_urls_tsv, write_str_to_file
from titles_utils import give_me_page_title
from table_extractor import give_me_page_tables
from normalizers.normalizer_util import normalize_tuples
import os
filenames_with_urls = read_urls_tsv(urls_loc)
output = ""
all_titles = ""
for i, item in enumerate(filenames_with_urls):
    fname, url = item
    # print(i)
    # if i<50:
    #     continue
    # pages = ['alibaba0', 'amazon0', 'cf0', 'ebay0', 'flipkart0', 'hs0', 'jabong0', 'myntra0', 'olx0', 'paytm0', 'shopclues0', 'snapdeal0', 'w0']
    # # pages = ['hs0']
    # if not fname in pages:
    #     continue
    # if fname !='flipkart0':
    #     continue
    print("processing ", fname)
    out_csv_name = fname+".csv"
    fname = fname + ".html"
    f_loc = os.path.join(pages_loc, fname)
    out_csv_loc = os.path.join(out_dir, out_csv_name)
    page_titles = give_me_page_title(f_loc)
    titles_str = "\t".join(page_titles)
    all_titles +=fname+"\t"+titles_str+"\n"
    page_specific_tables = give_me_page_tables(f_loc)
    page_specific_tables_str = "\n".join([k+"\t"+v for k, v in page_specific_tables])
    # print("string is ", page_specific_tables_str)
    normalized_table = normalize_tuples(page_specific_tables)
    normalized_table = "\n".join(["\t".join(r) for r in normalized_table])
    page_specific_title_str = url + "\t" + titles_str + "\n" + "\ntable\n" + page_specific_tables_str + "\n" + normalized_table
    write_str_to_file(out_csv_loc, page_specific_title_str)
titles_out = os.path.join(out_dir, 'titles_all.csv')
write_str_to_file(titles_out, all_titles)
print("everything is written...")