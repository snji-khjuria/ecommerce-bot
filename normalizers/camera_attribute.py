import re
def give_me_quantity_and_units(s):
    length_normalizer_regex = "^(\d*\.?\d+)\s?(\w+)"
    match = re.search(length_normalizer_regex, s)
    if match is None:
        return None, None
    return match.group(1), give_me_units_from_key(match.group(2))


def keyHasCameraSignal(k):
    k = k.lower()
    k_words = k.split()
    camera_signals = ["camera", "primary", "secondary"]
    for w in camera_signals:
        if w in k_words:
            return True
    return False

def isFloat(v):
    try:
        v = float(v)
        return True
    except:
        return False

def give_me_units_from_key(k):
    k = k.lower()
    k = k.replace("(", " ").replace(")", " ").strip()
    k = " ".join(k.split())
    camera_units = {"mp":"megapixels", "pixels":"pixels", "megapixels":"megapixels"}
    c_keys = sorted(camera_units.keys(), key=lambda k: len(k), reverse=True)
    for my_k in c_keys:
        if (" " + my_k in k) or (k==my_k):
            return camera_units[my_k]
    return None


def normalizeCameraUnits(quantity, units):

    if units == "megapixels":
        normalized_value = str(quantity)+" x 1000000"
    if units == "pixels":
        normalized_value = str(quantity)
    return quantity, units, normalized_value, "pixels"



def check_is_camera(tuple):
    k, v = tuple
    if keyHasCameraSignal(k):
        if isFloat(v):
            quantity = float(v)
            units = give_me_units_from_key(k)
        else:
            quantity, units = give_me_quantity_and_units(v)
        if quantity is not None and units is not None:
            return True, normalizeCameraUnits(quantity, units)
    return False, None