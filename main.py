def to_camel_case(text):
    new_str = []
    flag = False
    for i in range(len(text)):
        if text[i] == '_' or text[i] == '-':
            flag = True
            continue
        # elif text[0].islower():
        #     flag = True
        elif text[i].isupper():
            new_str.append(text[i].lower())
            continue

        if flag == True:
            new_str.append(text[i].capitalize())
            flag = False
        else:
            new_str.append(text[i])

    return ''.join(new_str)


print(to_camel_case('The-Stealth-Warrior'))
