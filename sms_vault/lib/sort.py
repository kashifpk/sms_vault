"Code for sorting contact names etc"


def alphanumeric_sort(items):
    "Sort given items with alphabets first and then numbers and symbols etc"
    
    alpha_list = []
    other_list = []
    
    for item in items:
        if item[0].isalpha():
            alpha_list.append(item)
        else:
            other_list.append(item)
    
    return sorted(alpha_list) + sorted(other_list)
