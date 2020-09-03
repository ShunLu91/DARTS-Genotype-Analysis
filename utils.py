def dict_normalize(_dict):
    total = 0
    for i in _dict.values():
        total += i
    for j in _dict.keys():
        _dict[j] /= total
    return _dict


def print_dict(_dict, sort=False, info=None, accuracy=0):
    if info:
        print(info)
    if sort:
        _dict = dict(sorted(_dict.items(), key=lambda x: x[1], reverse=True))

    for _, (k, v) in enumerate(_dict.items()):
        if accuracy != 0:
            v = round(v, accuracy)
            print(k, v)
        else:
            print(k, v)
