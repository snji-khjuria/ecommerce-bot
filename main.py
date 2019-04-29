pages_loc  = '/home/maulik/Desktop/textDetection/text-detection-ctpn/main/data/diffbot_dataset/table_pages/pages'
urls_loc   = '/home/maulik/Desktop/textDetection/text-detection-ctpn/main/data/diffbot_dataset/table_urls.tsv'
out_dir = '/home/maulik/Desktop/textDetection/text-detection-ctpn/main/data/diffbot_dataset/csv_outs'

from file_utils import read_urls_tsv, write_str_to_file
from titles_utils import give_me_page_title
import os
filenames_with_urls = read_urls_tsv(urls_loc)
output = ""
all_titles = ""
for item in filenames_with_urls:
    fname, url = item
    print("processing ", fname)
    out_csv_name = fname+".csv"
    fname = fname + ".html"
    f_loc = os.path.join(pages_loc, fname)
    out_csv_loc = os.path.join(out_dir, out_csv_name)
    page_titles = give_me_page_title(f_loc)
    titles_str = "\t".join(page_titles)
    all_titles +=fname+"\t"+titles_str+"\n"
    page_specific_title_str = url + "\t" + titles_str + "\n"
    write_str_to_file(out_csv_loc, page_specific_title_str)
titles_out = os.path.join(out_dir, 'titles_all.csv')
write_str_to_file(titles_out, all_titles)
print("everything is written...")