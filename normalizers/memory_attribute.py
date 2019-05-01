import re
def give_me_quantity_and_units(s):
    length_normalizer_regex = "^(\d*\.?\d+)\s?(\w+)"
    match = re.search(length_normalizer_regex, s)
    if match is None:
        return None, None
    return match.group(1), give_me_units_from_key(match.group(2))


def keyHasMemorySignal(k):
    k = k.lower()
    k_words = k.split()
    memory_signals = ["memory", "storage", "ram", "hdd", "external", "cache"]
    for w in memory_signals:
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
    memory_units = {"tb":"terabytes", "gb":"gigabytes", "mb":"megabytes", "kb":"kilobytes", "terabytes":"terabytes", "gigabytes":"gigabytes", "megabytes":"megabytes", "kilobytes":"kilobytes"}
    m_keys = sorted(memory_units.keys(), key=lambda k: len(k), reverse=True)
    for my_k in m_keys:
        if (" " + my_k in k) or (k==my_k):
            return memory_units[my_k]
    return None


def normalizeMemory(quantity, units):
    if units == "terabytes":
        normalized_value = float(quantity) *1024 * 1024 * 1024 * 1024
    if units == "gigabytes":
        normalized_value = float(quantity) *1024 * 1024 * 1024 * 1024
    if units == "megabytes":
        normalized_value = float(quantity) * 1024 * 1024
    if units == "kilobytes":
        normalized_value = float(quantity) * 1024
    # print("units are ", units)
    return quantity, units, normalized_value, "bytes"



def isPossibleMemoryString(s):
    s = s.lower()
    if "gb" in s or "mb" in s or "kb" in s or "bytes" in s:
        return True
    return False


def check_is_memory(tuple):
    k, v = tuple
    tuple_string = k+" " + v
    if isPossibleMemoryString(tuple_string):
        if keyHasMemorySignal(k):
            if isFloat(v):
                quantity = float(v)
                units = give_me_units_from_key(k)
            else:
                quantity, units = give_me_quantity_and_units(v)
                # print("qunatity and units", quantity, units)
            if quantity is not None and units is not None:
                return True, normalizeMemory(quantity, units)
            return False, None
    return False, None