import webcolors
def normalize_color(color_name):
    try:
        hex_value = webcolors.name_to_hex(color_name)
        rgb_value = webcolors.name_to_rgb(color_name)
        return str(hex_value), str(rgb_value)
    except:
        color_words = color_name.split(" ")
        for i in range(1, len(color_words)):
            try:
                word = " ".join(color_words[i:])
                hex_value = webcolors.name_to_hex(word)
                rgb_value = webcolors.name_to_rgb(word)
                return str(hex_value), str(rgb_value)
            except:
                continue
        return None, None
def isColorTuple(tuple):
    # print("tuple is ", tuple)
    k, v = tuple
    k = k.lower().strip()
    support_list = ["color", "colour"]
    for item in support_list:
        if item in k:
            hex_value, rgb_value = normalize_color(v)
            if hex_value==None or rgb_value==None:
                return False, None, None
            else:
                return True, hex_value, rgb_value
    return False, None, None
