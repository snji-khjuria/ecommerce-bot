from titles_utils import give_me_page_titles_json
page_loc  = '/home/maulik/Desktop/textDetection/text-detection-ctpn/main/data/diffbot_dataset/table_pages/pages/alibaba0.html'
titles_json = give_me_page_titles_json(page_loc)
print("titles json is ", titles_json)