def check_sentance(arr):
    for word in arr:
        if(word.cmp_sentance == False):
            return False
        
    return True

def check_translation(arr):
    for word in arr:
        if(word.cmp_translation == False):
            return False
        
    return True