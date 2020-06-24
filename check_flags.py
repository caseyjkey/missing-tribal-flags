import csv
import pandas as pd
import re
     
def missing_flags(flags, tribes):
    # Remove all flags which are oversize
    flags = flags[~flags['Notes/Dimensions'].str.contains("Oversize", na=False)]

    tribes_missing_flag = []
    for tribe in tribes['Tribe']:
        # Match shorter tribe name to full tribe name
        # Example: match 'Absentee-Shawnee' and 'Absentee Shawnee Tribe'
        # Example: match 'Ak Chin' and 'Ak-Chin'
        # 1. tokenize tribe by splitting by blankspace
        # 2. If token has hyphens, split by '-'
        tribe_tokens = []
        for token in tribe.split():
            if '-' in token:
                [tribe_tokens.append(token) for token in token.split('-')]
            else:
                tribe_tokens.append(token)

        regex_string = '^'
        for word in tribe_tokens:
            regex_string += '(?=.*\\b' + word + '\\b)'
        regex_string += '.*$'
        r = re.compile(regex_string)
        
        # Determine if a flag is in museum's collection
        flags_in_collection = list(filter(r.match, flags['Tribal Nation'].tolist()))
        if not flags_in_collection:
            print(tribe, ' does not have a flag. Tokens: ', tribe_tokens)
            tribes_missing_flag.append(tribe) 

            
    return tribes_missing_flag


if __name__ == '__main__':
    tribes = pd.read_csv('tribes.csv')
    flags = pd.read_excel('flags.xlsx')
    tribes = missing_flags(flags, tribes)
    print(len(tribes))
    with open('output.csv', 'w', newline='') as outfile:
        wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['Tribe'])
        for tribe in tribes:
            wr.writerow([tribe])
    assert('Rosebud' not in tribes)
    assert('Oglala Sioux' in tribes)
    
