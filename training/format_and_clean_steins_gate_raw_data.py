import json

f = open(r"./raw_data/steins_gate_raw_text.txt", 'r')
raw_text = f.read()
f.close()
len(raw_text)
all_lines = raw_text.split('\n')
all_conver = []
context = []
conver = {
    'context': []
}
is_context = False
is_conver = False
char = ''


def get_char_name(xml_tag):
    xml_tag = xml_tag[xml_tag.index('<voice name="') + len('<voice name="'):]
    xml_tag = xml_tag[:xml_tag.index(r'"')]
    return xml_tag


def remove_xml_tags(mess):
    # mot the best way to remove xml tags, but it will do
    tmp = mess.split('<')
    for i, val in enumerate(tmp):
        if '>' in val or val.startswith('/'):
            val = val[val.index(">") + 1:]
        elif i > 0:
            val = '<' + val
        tmp[i] = val

    return ''.join(tmp)


for line in all_lines:
    if line.startswith('<PRE'):
        is_context = True
        is_conver = False
        context = ''
        continue
    if line.startswith('<voice'):
        is_context = False
        is_conver = True
        char = get_char_name(line)
        continue
    if line.startswith('</PRE'):
        is_context = False
        is_conver = False
        continue
    if not line:
        continue

    line = remove_xml_tags(line)
    if is_context:
        conver['context'].append(line)
        continue
    if is_conver:
        is_conver = False
        is_context = True
        line = line.replace('"', '')
        conver['char'] = char
        conver['message'] = line
        all_conver.append(conver)
        conver = {
            'context': []
        }
        continue
pass
f = open(r"./formatted_data/steins_gate_conversations.json", 'w')
json.dump(all_conver, f, indent=4)
f.close()
