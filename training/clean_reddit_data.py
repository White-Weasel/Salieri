import json
import re

import emoji

# f = open("/home/giang/data/rd_dataset/rddit.json", 'r')
# a = json.load(f)
# f.close()
# n = a['CasualConversation']
# n = [conver for conver in n if len(conver) > 1]
# emoji_list = emoji.unicode_codes.EMOJI_DATA
# n = [conver for conver in n if not any(emoji in line for line in conver for emoji in emoji_list)]
f = open("/home/giang/data/rd_dataset/casual_conversation-cleaned.jsonl", 'r')
a = [json.loads(line) for line in f.readlines()]
f.close()
filter_words = ['/r/', 'r/', '\\r\\', 'r\\',
                'u/', '/u/', '\\u\\', 'u\\',
                ' op ', ' op,', ' op.',
                'https://', 'http://',
                '\nedit:',
                "\*"
                ]
remove_words = ['/s', '\s',
                '^',
                '&#x200b;',
                ]
reformat_keywords = [
    '*abc*',
    '[\w+](*)',
    '~~abc~~',
    '¯\_( ͠° ͟ʖ °͠ )_/¯',
    '**abc**',
    '\n\n\n\n...',
    '*abc\n',
    '>!Do you remember !<',
    '^(this is a joke lol)',
    '^"holy ^shit"',
    '>it was my lymph nodes \
     >bad muscle aches everywhere\
     >bad chills....fever....low temperature\
     >SPO2 levels of 89-91\
     >Everything gets stiff and pops like crazy constantly',
    '`?show=all`'
]

all_conversations = [conver for conver in a if not any(x in ''.join(conver).lower() for x in filter_words)]
for conver in all_conversations:
    for line in conver:
        for remove_w in remove_words:
            if remove_w in line.lower():
                line = line[:line.index(remove_w)] + line[line.index(remove_w) + len(remove_w):]

        # replace **abc** with abc
        line = re.sub(r"(\*+)([^*\n]*)(\*+)", r"\2", line)
        # replace ~~abc~~ with abc
        line = re.sub(r"(~+)([^~\n]*)(~+)", r"\2", line)
        # replace >!abc!< with abc
        line = re.sub(r"(>!)([^!<\n]*)(!<+)", r"\2", line)
        # replace ^(abc) with abc
        line = re.sub(r"(\^\()([^^\(\)\n]*)(\))", r"\2", line)
        # replace ^abc ^def with abc def
        line = re.sub(r"(\^)([^\^\n\b]*)", r"\2", line)
        # replace >abc \n\n>def with abc\n\ndef
        line = re.sub(r"^(>)(.*)", r"\2", line)

pass
