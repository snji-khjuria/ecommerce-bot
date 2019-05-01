from normalizers.camera_attribute import check_is_camera
from normalizers.color_attribute import isColorTuple
from normalizers.length_attribute import check_is_length
from normalizers.weight_attribute import check_is_weight
from normalizers.memory_attribute import check_is_memory


def give_me_clean_tuple(tuple):
    k, v = tuple
    kk = k.lower()
    entries = ["length", "breadth", "height", "width", "depth", "weight", "capacity", "camera", "primary camera", "secondary camera", "memory", "storage", "ram", "hdd", "cache"]
    if kk not in entries:
        return (k, v)
    else:
        vs = v.split()
        if len(vs)==1:
            return (k, v)
        try:
            v1 = float(vs)
            return (k, v)
        except:
            return k, " ".join(vs)

def check_is_float(n):
    try:
        n = float(n)
        return True
    except:
        return False

def tuples_cleaner(tuples):
    helper_dict = {}
    for item in tuples:
        k, v = item
        vv = v.split()
        if len(vv)>1 and not check_is_float(vv[0]):
            vv = vv[0]
            helper_dict[vv] = 1+helper_dict.get(vv, 0)
    helper_dict = sorted(helper_dict.items(), key=lambda k:k[1], reverse=True)
    helper_dict = helper_dict[0]
    more_than_half = int(0.5*len(tuples))
    if helper_dict[1]<more_than_half:
        return tuples
    output = []
    starter = helper_dict[0]
    for item in tuples:
        k, v = item
        if v.startswith(starter):
            v = v[len(starter):].strip()
        output.append((k, v))
    return output


def normalize_tuples(tuples):
    output = []
    # tuples = tuples_cleaner(tuples)
    for tuple in tuples:
        color_status, hex_value, rgb_value = isColorTuple(tuple)
        # print(color_status)
        if color_status==True:
            k, v = tuple
            tuple = (k, v, "Hex: " + hex_value, "RGB: " +rgb_value)
            output.append(tuple)
            continue
        length_status, length_tuple = check_is_length(tuple)
        if length_status==True:
            num_p, units_p, num_n, units_n = length_tuple
            k, v = tuple
            tuple = (k, v, "Quantity: "+str(num_p), "Units: " + str(units_p), "NormalizedQuantity: " + str(num_n), "Normalized_Units: " + str(units_n))
            output.append(tuple)
            continue
        weight_status, weight_tuple = check_is_weight(tuple)
        if weight_status==True:
            num_p, units_p, num_n, units_n = weight_tuple
            k, v = tuple
            tuple = (k, v, "Quantity: " + str(num_p), "Units: " + str(units_p), "NormalizedQuantity: " + str(num_n),
                     "Normalized_Units: " + str(units_n))
            output.append(tuple)
            continue
        memory_status, memory_tuple = check_is_memory(tuple)
        if memory_status==True:
            num_p, units_p, num_n, units_n = memory_tuple
            k, v = tuple
            tuple = (k, v, "Quantity: " + str(num_p), "Units: " + str(units_p), "NormalizedQuantity: " + str(num_n),
                     "Normalized_Units: " + str(units_n))
            output.append(tuple)
            continue
        camera_status, camera_tuple = check_is_camera(tuple)
        if camera_status == True:
            num_p, units_p, num_n, units_n = camera_tuple
            k, v = tuple
            tuple = (k, v, "Quantity: " + str(num_p), "Units: " + str(units_p), "NormalizedQuantity: " + str(num_n),
                     "Normalized_Units: " + str(units_n))
            output.append(tuple)
            continue
    output = [list(i) for i in output]
    return output
    # return "\n".join(["\t".join(row) for row in output])