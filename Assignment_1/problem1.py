import re


def problem1(NPs, S):
    # first, we case-fold the string
    S = S.casefold()
    print("THE STRING: ", S)
    # because any of the noun phrases can be in the string, let's define a string and append all nouns separated by "|"
    all_noun_options = ""
    for i in range(len(NPs)):
        all_noun_options += "("
        all_noun_options += NPs[i]
        if i == len(NPs) - 1:
            all_noun_options += ")"
            break
        all_noun_options += ")"
        all_noun_options += "|"

    print("ALL NOUN OPTIONS: ", all_noun_options)

    # let's now define the regular expressions including all noun phrases
    first_type_re = re.compile(rf'\b({all_noun_options})\b\s((is)|(are)|(was))+\s(a|an)?(a (type|kind)\sof)?\s*\b({all_noun_options})\b')
    second_type_re = re.compile(rf'\b({all_noun_options})\b,\s((including)|(such as))\s\b({all_noun_options})\b(,?\s(or|and)?\s?\b({all_noun_options})\b,?)*')

    # we will store the results in lists
    first_re_list = first_type_re.findall(S)
    second_re_list = second_type_re.findall(S)

    # this set will store all the found hypernym results
    results = set()

    size_options = len(NPs)
    # now let's run through the first list and get all tuples if applicable
    for regular_expression in first_re_list:
        # we know that the last string is the hypernym while the first is the hyponym
        # print(regular_expression)
        couple = tuple((regular_expression[len(regular_expression)-size_options-1], regular_expression[0]))
        results.add(couple)

    # now let's run through the second list and get all tuples if applicable
    # we know that the first string is the hypernym while the rest are hyponyms
    # so, we can safely assume that if a noun is presents from NPs, it is a hyponym
    for regular_expression in second_re_list:
        hypernym = regular_expression[0]
        for noun in NPs:
            if noun == hypernym:
                continue
            if noun in regular_expression:
                couple = tuple((hypernym, noun))
                results.add(couple)

    print("RESULTS: ", results)
    return results
    
    
