import json
import random
import re

PROMPT_END = '~##~'
COMPLETION_END = '~#END#~'
f = open("/home/giang/data/less commands/[136542963336478720] [part 10].txt", 'r')
raw_data = f.read()
assert not (PROMPT_END in raw_data or COMPLETION_END in raw_data)
f.close()
# remove emoji
raw_data = re.sub(r"(<a?)?:\w+:(\d{18}>)?", "", raw_data)
data = raw_data.split('\t')
# decode //n
data = [bytes(d, "utf-8").decode("unicode_escape").strip() for d in data]
# remove messages with only emoji
data = [d for d in data if not (d.count(':') < 2 and d.split(':')[1].strip() == '')]
# get list of users
users = set([d.split(':')[0] for d in data])
# get messages from the user with the most messages
# user_message_count = [(user, len([d for d in data if d.startswith(user)])) for user in users]
user_message_count = {user: 0 for user in users}
for d in data:
    user_message_count[d.split(':')[0]] += 1
user_message_count = [(key, value) for key, value in user_message_count.items()]
user_message_count = sorted(user_message_count, key=lambda x: x[1], reverse=True)
user_messages = [data[index - 9:index + 1]
                 for index, value in enumerate(data)
                 if (value.startswith(user_message_count[2][0]) or value.startswith(user_message_count[1][0]))
                 and index > 10]
# TODO: random empty messages
training_data = [
    {
        'prompt': '\n'.join(message[:-1]) + f"\n{message[-1].split(':')[0]}:{PROMPT_END}",
        'completion': f" {':'.join(message[-1].split(':')[1:])}{COMPLETION_END}",
    }
    for message in user_messages]
# remove messages with mentions. If we are making a discord bot then this will not be needed
training_data = [line for line in training_data if '@' not in line['prompt'] and '@' not in line['completion']]

training_data_length = int(input("Training data length: "))
training_data = random.sample(training_data, training_data_length)
f = open("./training.jsonl", 'w')
f.write('\n'.join([json.dumps(line) for line in training_data]))
f.close()
print('done')
pass
