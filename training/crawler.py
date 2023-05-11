import requests
import praw
from praw.models import Submission
import requests.auth


# client_auth = requests.auth.HTTPBasicAuth('0KT3p7otbaKdocVLi5z5Mg', 'NxCwLtSbSIh83V5QWmrfnWRjBRdJwQ')
# post_data = {"grant_type": "password", "username": "totally_not_aqua", "password": "Ndbghdvn1998"}
# headers = {"User-Agent": "anything/0.1 by totaly_not_aqua"}
# response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
#                          headers=headers)
# a = response.json()
# access_token = a['access_token']


def tree_to_list_recursion(root, limit_to_top: int = None,
                           max_depth: int = None,
                           __depth: int = 1):
    reps = [c for c in root.replies]
    root_body = f"/u/{root.author.name}: {root.body}"
    if not reps or (max_depth and __depth >= max_depth):
        return [[root_body]]
    reps = [rep for rep in reps if rep.score > 0 and rep.author]
    if limit_to_top:
        reps = sorted(reps, key=lambda rep: rep.score, reverse=True)[:limit_to_top]
    result = [[root_body] + c
              for rep in reps
              for c in tree_to_list_recursion(rep, limit_to_top, max_depth, __depth=__depth + 1)]
    return result


def get_all_conversation_in_post(submission: Submission,
                                 replace_limit: int = 0,
                                 limit_to_top: int = None,
                                 max_depth: int = None,
                                 min_replies: int = 0) -> list[list[str]]:
    """
    Get all conversations in a post
    :param submission: :class:`.Submission` the post to get all conversations
    :param replace_limit: The maximum number of :class:`.MoreComments` instances to replace.
                            Each will need another API call. Set to 0 to delete all of them
    :param limit_to_top: get only top <number> of replies
    :param max_depth: max replies depth
    :param min_replies: min length of the comment chain
    :return:
    """
    submission.comments.replace_more(limit=replace_limit)
    comment_list = [i for i in submission.comments if i.author]
    if limit_to_top:
        comment_list = sorted(comment_list, key=lambda comment: comment.score, reverse=True)[:limit_to_top]
    all_messages = []
    for root in comment_list:
        all_messages += tree_to_list_recursion(root,
                                               limit_to_top=limit_to_top,
                                               max_depth=max_depth)
    return [message for message in all_messages if len(message) >= min_replies]


def main():
    client = praw.Reddit(
        client_id="0KT3p7otbaKdocVLi5z5Mg",
        client_secret="NxCwLtSbSIh83V5QWmrfnWRjBRdJwQ",
        user_agent="anything/0.1",
    )
    print(client.read_only)
    submissions = client.subreddit("CasualConversation").top(limit=10)
    submissions = [submission for submission in submissions]
    conversations = [conversation
                     for submission in submissions
                     for conversation in get_all_conversation_in_post(submission, limit_to_top=3,
                                                                      min_replies=3, max_depth=None)
                     ]
    # short_conversations = tuple(set(tuple(con[:4]) for con in conversations if len(con) >= 3))
    # short_conversations = get_all_conversation_in_post(submissions[3], limit_to_top=3)
    pass


if __name__ == '__main__':
    main()
