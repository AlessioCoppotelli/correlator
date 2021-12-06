# calc average of number in a list
def average(lst) :
    if type(lst) is not list :
        out = lst
    else :
        out = sum(lst) / len(lst)
    return out
