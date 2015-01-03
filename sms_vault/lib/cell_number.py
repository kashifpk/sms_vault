"Code related to processing cell numbers"

def normalize(number, country_code, network_code):
    """
    Normalizes given cell number to +[countrycode][cellnumber] format
    removing any white spaces dashes etc.
    """
    
    
    
    new_num = number.replace(' ', '').replace('-', '')
    if new_num.startswith('+'):   # already  correct number
        return new_num

    elif not new_num[0].isdigit():
        return number
    
        
    if new_num.startswith(country_code):
        return '+' + new_num
    
    elif new_num.startswith('00'):
        return '+' + new_num[2:]
    
    elif new_num.startswith(network_code) or new_num.startswith('0' + network_code):
        return '+' + country_code + new_num.rstrip(0)
    
    return new_num
    
    
