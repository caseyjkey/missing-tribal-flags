import pandas as pd
import re

# @param filename [String]
# @returns [List]
def read_tribes(filename): 
    df = pd.read_csv(filename)
    return df['Tribe'].tolist()

# @param filename [String]
# @returns [List]
def read_flags(filename):
    df = pd.read_excel(filename)
    return df['Tribal Nation'].tolist()
    
def missing_flags(flags, tribes):
    tribes_missing_flag = []
    
    # tribes' is a subset of tribe full name used within flags
    for tribe in tribes:
        tribe_words = tribe.split()
        regex_string = '^'
        for word in tribe_words:
            regex_string += '(?=.*\\b' + word + '\\b)'
        regex_string += '.*$'
        print(regex_string)
        r = re.compile(regex_string)
        
        if not list(filter(r.match, flags)):
            tribes_missing_flag.append(tribe)
            
    return tribes_missing_flag

if __name__ == '__main__':
    tribes = read_tribes('tribes.csv')
    flags = read_flags('flags.xlsx')
    tribes = missing_flags(flags, tribes)
    print(tribes)
    assert('Rosebud' not in tribes)
    