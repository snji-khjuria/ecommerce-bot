import re
def give_me_quantity_and_units(s):
    length_normalizer_regex = "^(\d*\.?\d+)\s?(\w+)"
    match = re.search(length_normalizer_regex, s)
    if match is None:
        return None, None
    return match.group(1), give_me_units_from_key(match.group(2))


def keyHasLengthSignal(k):
    k = k.lower()
    k_words = k.split()
    length_signals = ["length", "breadth", "height", "width", "depth"]
    for w in length_signals:
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
    length_units = {"mm": "millimeters", "m": "meters", "cm": "centimeters", "millimeter": "millimeters",
                    "centimeter": "centimeters", "kilometer": "kilometers", "meter": "meters"}
    l_keys = sorted(length_units.keys(), key=lambda k: len(k), reverse=True)
    for my_k in l_keys:
        if (" " + my_k in k) or (k==my_k):
            return length_units[my_k]
    return None


def normalizeLength(quantity, units):
    if units == "millimeters":
        normalized_value = float(quantity) / 10.0
    if units == "centimeters":
        normalized_value = float(quantity)
    if units == "meters":
        normalized_value = float(quantity) * 100.0
    if units == "kilometers":
        normalized_value = float(quantity) * 100000.0
    # print("units are ", units)
    return quantity, units, normalized_value, "centimeters"


def check_is_length(tuple):
    k, v = tuple
    # print("tuple called is ", tuple)
    if keyHasLengthSignal(k):
        # print("yes key has singal")
        if isFloat(v):
            quantity = float(v)
            units = give_me_units_from_key(k)
        else:
            # print("moving on for value extraction")
            quantity, units = give_me_quantity_and_units(v)
            # print("qunatity and units", quantity, units)
        if quantity is not None and units is not None:
            return True, normalizeLength(quantity, units)
    return False, None

# print(give_me_quantity_and_units("34 cm"))
# print(check_is_length(("Length (mm)", "22")))