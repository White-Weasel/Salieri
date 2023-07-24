import os
import time
import json
import requests
import praw
from praw.models import Submission
import requests.auth


# client_auth = requests.auth.HTTPBasicAuth(os.environ.get("client_id"), os.environ.get("client_secret"))
# post_data = {"grant_type": "password", "username": "totally_not_aqua", "password": os.environ.get("passwd")}
# headers = {"User-Agent": "anything/0.1 by totaly_not_aqua"}
# response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
#                          headers=headers)
# a = response.json()
# access_token = a['access_token']


def tree_to_list_recursion(root,
                           limit_to_top: int = None,
                           min_score: int = 0,
                           max_depth: int = None,
                           get_mod_comment=False,
                           __depth: int = 1):
    reps = [c for c in root.replies
            if c.author  # deleted
            and (hasattr(c.author, 'is_mod')
                 and ((get_mod_comment and c.author.is_mod) or (not get_mod_comment and not c.author.is_mod))
                 )  # mod
            and c.body != '[removed]'  # removed
            and c.body != '[deleted]'  # removed
            ]
    root_body = f"/u/{root.author.name}: {root.body}"
    reps = [rep for rep in reps if rep.score > min_score and rep.author]
    if not reps or (max_depth and __depth >= max_depth):
        return [[root_body]]
    if limit_to_top:
        reps = sorted(reps, key=lambda rep: rep.score, reverse=True)[:limit_to_top]
    result = [[root_body] + c
              for rep in reps
              for c in tree_to_list_recursion(rep, limit_to_top=limit_to_top, max_depth=max_depth,
                                              get_mod_comment=get_mod_comment, __depth=__depth + 1)]
    return result


def get_all_conversation_in_post(submission: Submission,
                                 replace_limit: int = 0,
                                 limit_to_top: int = None,
                                 min_score: int = 0,
                                 max_depth: int = None,
                                 min_replies: int = 0) -> list[list[str]]:
    """
    Get all conversations in a post
    :param min_score:
    :param submission: :class:`.Submission` the post to get all conversations
    :param replace_limit: The maximum number of :class:`.MoreComments` instances to replace.
                            Each will need another API call. Set to 0 to delete all of them
    :param limit_to_top: get only top <number> of replies
    :param max_depth: max replies depth
    :param min_replies: min length of the comment chain
    :return:
    """
    # s_time = time.perf_counter()
    if limit_to_top:
        submission.comment_sort = "top"
        submission.comment_limit = limit_to_top
    submission.comments.replace_more(limit=replace_limit)
    # print(f"replace_more takes {time.perf_counter() - s_time} seconds")
    # comment_list = [i for i in submission.comments
    #                 if not isinstance(i, praw.models.reddit.more.MoreComments) and i.author]
    comment_list = [i for i in submission.comments if i.author]
    if limit_to_top:
        comment_list = sorted(comment_list, key=lambda comment: comment.score, reverse=True)[:limit_to_top]
    all_messages = []
    for root in comment_list:
        all_messages += tree_to_list_recursion(root,
                                               limit_to_top=limit_to_top,
                                               min_score=min_score,
                                               max_depth=max_depth)
    return [message for message in all_messages if len(message) >= min_replies]


def main():
    # client = praw.Reddit(
    #     client_id=os.environ.get("client_id"),
    #     client_secret=os.environ.get("client_secret"),
    #     user_agent="anything/0.1",
    # )
    client = praw.Reddit(
        client_id=os.environ.get("client_id"),
        client_secret=os.environ.get("client_secret"),
        password=os.environ.get("passwd"),
        user_agent="Python:test.app.api:0.01 (by /u/totally_not_aqua)",
        username="totally_not_aqua",
    )

    print(client.read_only)
    s_time = time.perf_counter()
    subreddits = ["4chan"]
    conversations = {}
    try:
        for sub in subreddits:
            conversations[sub] = []
            submissions = client.subreddit(sub).top(limit=1000)
            submissions = [submission for submission in submissions]
            print(f"Get {len(submissions)} submissions from /r/{sub}")
            for index, submission in enumerate(submissions):
                s_time = time.perf_counter()
                conversations[sub] += get_all_conversation_in_post(submission,
                                                                   replace_limit=5,
                                                                   limit_to_top=100,
                                                                   min_score=10,
                                                                   min_replies=3,
                                                                   max_depth=None)
                print(f"fetching submission {index + 1}/{len(submissions)} from {sub} "
                      f"takes {time.perf_counter() - s_time} seconds")

            # conversations += [conversation
            #                   for submission in submissions
            #                   for conversation in get_all_conversation_in_post(submission,
            #                                                                    replace_limit=3,
            #                                                                    limit_to_top=False,
            #                                                                    min_score=10,
            #                                                                    min_replies=False,
            #                                                                    max_depth=None)
            #                   ]
    except KeyboardInterrupt:
        print("Saving...")
    finally:
        # short_conversations = tuple(set(tuple(con[:4]) for con in conversations if len(con) >= 3))
        # short_conversations = get_all_conversation_in_post(submissions[3], limit_to_top=3)
        f = open("/home/giang/data/rddit.json", "w")
        json.dump(conversations, f)
        f.close()
    pass


if __name__ == '__main__':
    main()
