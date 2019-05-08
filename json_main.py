from titles_utils import give_me_page_title
from table_extractor import give_me_page_tables
from normalizers.normalizer_util import normalize_tuples
import json
# page_loc  = '/home/maulik/Desktop/textDetection/text-detection-ctpn/main/data/diffbot_dataset/table_pages/pages/alibaba0.html'
import sys
page_loc = sys.argv[1]
# page_loc = '/home/maulik/Desktop/textDetection/text-detection-ctpn/main/data/diffbot_dataset/table_pages/pages/hs0.html'
# titles_json = give_me_page_titles_json(page_loc)
page_titles = give_me_page_title(page_loc)
tables = give_me_page_tables(page_loc)
normalized_tables = normalize_tuples(tables)
# print("titles json is ", titles_json)

data = {}
data['titles'] = page_titles
data['tables'] = tables
data['normalized_tables'] = normalized_tables
json_data = json.dumps(data)
print(json_data)
