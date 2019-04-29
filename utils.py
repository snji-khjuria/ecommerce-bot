def give_me_raw_html_content(url_loc):
    with open(url_loc, 'r') as f:
        content = f.read()
        return " ".join(content.split())
