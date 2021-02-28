import re


def remove_superscripts(string):
    result = re.sub("<s\s*.*>\s*.*<\/s>", "", string)
    return result


print(remove_superscripts("Hello<s>3</s>"))