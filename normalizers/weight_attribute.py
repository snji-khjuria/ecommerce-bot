import re
def give_me_quantity_and_units(s):
    weight_normalizer_regex = "^(\d*\.?\d+)\s?(\w+)"
    match = re.search(weight_normalizer_regex, s)
    if match is None:
        return None, None
    return match.group(1), give_me_units_from_key(match.group(2))

def keyHasWeightSignal(k):
    k = k.lower()
    k_words = k.split()
    length_signals = ["weight", "capacity"]
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
    weight_units = {"kg":"kilogram", "kilogram":"kilogram", "g":"gram", "gram":"gram", "kilograms":"kilogram", "grams":"gram", "tons":"tons"}
    w_keys = sorted(weight_units.keys(), key=lambda k: len(k), reverse=True)
    for my_k in w_keys:
        if (" " + my_k) in k or k==my_k:
            return weight_units[my_k]
    return None


def normalizeWeight(quantity, units):
    if units == "gram":
        normalized_value = float(quantity)
    if units == "kilogram":
        normalized_value = float(quantity)*1000
    if units== "tons":
        normalized_value = float(quantity)*907185
    return quantity, units, normalized_value, "gram"


def check_is_weight(tuple):
    k, v = tuple
    if isFloat(v) and keyHasWeightSignal(k):
        num = float(v)
        units = give_me_units_from_key(k)
        if units is not None:
            return True, normalizeWeight(num, units)
    if keyHasWeightSignal(k):
        quantity, units = give_me_quantity_and_units(v)
        if quantity is not None and units is not None:
            return True, normalizeWeight(quantity, units)
    return False, None
