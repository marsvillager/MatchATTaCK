import re

from stix2 import Filter

from classification.attack_classification import get_all_src
from match import get_stop_words

if __name__ == '__main__':
    file = open("./data/techniques_mobile_data.txt", mode="w", encoding="utf-8")

    filer_list: list = ["(e.g.,", "e.g.", "(i.e.", "n.d)", "*", "-", "(Citation"]
    wrap_list: list = [",", ".", ";", "(", ")"]  # newline
    stop_words: list[str] = get_stop_words("../resources/stop_en_words.txt") + filer_list

    count = 0  # count numbers, relationship?
    src = get_all_src('../mitre_attack_data/cti')
    filter_list = [
        Filter("type", "=", "attack-pattern")
        # Filter("x_mitre_domains", "=", "mobile-attack")
    ]
    mitre_lists: list = src.query(filter_list)
    for mitre_list in mitre_lists:
        if 'description' in mitre_list:
            count += 1
            # file.write(str(count) + "......")
            description_list: list = re.split('[\s/:"“”]', mitre_list['description'])  # space, /, :, ", ”, ”
            print(description_list)
            for description in description_list:
                flag: bool = True
                for stop_word in stop_words:
                    # case insensitive
                    if description.upper() == stop_word.upper():
                        flag = False
                        break
                if flag:
                    if "'s" in description:  # Android's ==> Android
                        file.write(description[:-2] + " ")
                    else:
                        for wrap in wrap_list:
                            loc = description.find(wrap)
                            if loc != -1:
                                tolist = list(description)
                                tolist[loc] = "\n"
                                description = ''.join(tolist)
                        file.write(description + " ")
            file.write("\n")

    print(count)
    file.close()
