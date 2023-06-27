import json
import re
import uuid

import emoji
from datasets import Dataset

PROMPT_END_TOKEN = r"<|endofprompt|>"
TEXT_END_TOKEN = r"<|endoftext|>"

# f = open("/home/giang/data/rd_dataset/rddit.json", 'r')
# a = json.load(f)
# f.close()
# n = a['CasualConversation']
# n = [conver for conver in n if len(conver) > 1]
# emoji_list = emoji.unicode_codes.EMOJI_DATA
# n = [conver for conver in n if not any(emoji in line for line in conver for emoji in emoji_list)]
f = open("/home/giang/data/rd_dataset/casual_conversation-no_emoji.jsonl", 'r')
a = [json.loads(line) for line in f.readlines()]
f.close()
filter_words = ['/r/', 'r/', '\\r\\', 'r\\',
                'u/', '/u/', '\\u\\', 'u\\',
                ' op ', ' op,', ' op.',
                'https://', 'http://',
                '\nedit:',
                "\*",
                r'`', '▽', '♡', 'ᴗ', '´', ':)', r"_/¯",
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

all_conversations = [conver for conver in a
                     if not any(x in line[line.index(':') + 1:].lower()
                                for line in conver
                                for x in filter_words
                                )
                     ]
for c_index, conver in enumerate(all_conversations):
    for l_index, line in enumerate(conver):
        header = line[:line.index(': ') + 2]
        content = line[line.index(': ') + 2:]
        for remove_w in remove_words:
            if remove_w in content.lower():
                try:
                    content = content[:line.index(remove_w)] + content[content.index(remove_w) + len(remove_w):]
                except ValueError:
                    pass

        # # replace "abc" with abc
        # content = re.sub(r"(\"+)([^*\n]*)(\"+)", r"\2", content)
        # # replace “abc” with abc
        # content = re.sub(r"(\"+)([^*\n]*)(\"+)", r"\2", content)
        # # replace 'abc' with abc
        # content = re.sub(r"(\'+)([^*\n]*)(\'+)", r"\2", content)
        # replace **abc** with abc
        content = re.sub(r"(\*+)([^*\n]*)(\*+)", r"\2", content)
        # replace ~~abc~~ with abc
        content = re.sub(r"(~+)([^~\n]*)(~+)", r"\2", content)
        # replace >!abc!< with abc
        content = re.sub(r"(>!)([^!<\n]*)(!<+)", r"\2", content)
        # replace ^(abc) with abc
        content = re.sub(r"(\^\()([^^\(\)\n]*)(\))", r"\2", content)
        # replace ^abc ^def with abc def
        content = re.sub(r"(\^)([^\^\n\b]*)", r"\2", content)
        # replace >abc \n\n>def with abc\n\ndef
        content = re.sub(r"^(>)(.*)", r"\2", content)
        line = header + content
        conver[l_index] = line
    all_conversations[c_index] = conver

ds = {
    'instruction': [],
    'input': [],
    'output': [],
}
for conver in all_conversations[:500]:
    instruction_ = 'As Salieri, response to the following conversation:'
    input_ = '\n'.join([line.replace('/u/', '@') for line in conver[:-1]]) + f"\n@Salieri: "
    output_ = conver[-1][conver[-1].index(':') + 1:].strip()
    # id_ = str(uuid.uuid1())
    # messages = '\n'.join(conver[:-1]) + f"\n{conver[-1][:conver[-1].index(':') + 1]} {PROMPT_END_TOKEN}{conver[-1][conver[-1].index(':') + 1:].strip()}{TEXT_END_TOKEN}"
    ds['instruction'].append(instruction_)
    ds['input'].append(input_)
    ds['output'].append(output_)
dataset = Dataset.from_dict(ds)
dataset.push_to_hub("binhgiangnguyendanh/reddit_casual_conversation_for_alpaca_lora", private=True)
pass
