import emoji
import pandas


def main():
    dtypes = {
        "0": str,
        "1": str,
        "2": str,
        "3": str,
    }
    raw_data = pandas.read_csv("/home/giang/data/reddit dataset/casual_data_windows.csv",
                               dtype=dtypes, keep_default_na=False, na_values=['NaN'])
    raw_data = [line[1:] for line in raw_data.values]
    # remove /s, subreddit, user mentions, ...
    filtered = ['/r/', 'r/', '\\r\\', 'r\\', 'u/', '/u/', '\\u\\', 'u\\', '/s', ' op ', ' op,', ' op.']
    data = [line for line in raw_data if not any(x in ''.join(line).lower() for x in filtered)]
    # remove emoji (?)
    data = [[emoji.replace_emoji(value, '') for value in line] for line in data]

    all_conversations = []

    def is_root(value):
        return value in [con[0] for con in all_conversations]

    def is_leaf(value):
        return value in [con[-1] for con in all_conversations]

    # noinspection PyShadowingNames
    def find_nodes(value: str):
        return [(i, j) for i, line in enumerate(all_conversations) for j, val in enumerate(line) if val == value]

    # noinspection PyShadowingNames
    def find_leafs(value: str):
        return [index for index, line in enumerate(all_conversations) if line[-1] == value] or False

    # noinspection PyShadowingNames
    def find_branches(con: list[str]):
        return [index for index, line in enumerate(all_conversations) if all(x in line for x in con)]

    for index, line in enumerate(data):
        branch = find_branches(line[:2])
        if branch:
            all_conversations[branch[0]].append(line[2])
            continue
        else:
            branch = find_branches(line[:1])
            if branch:
                new_branch = all_conversations[branch[0]].copy()
                new_branch += line[1:]
                all_conversations.append(new_branch)
            else:
                all_conversations.append(line)
        print(f"done {index + 1} lines")

    pass


if __name__ == '__main__':
    main()
