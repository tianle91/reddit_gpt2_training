import argparse
import json
import os

import praw


def get_parent_comments(comment, reddit):
    # parent_id	The ID of the parent comment. 
    # If it is a top-level comment, this returns the submission ID instead (prefixed with ‘t3’).
    parent_id = comment.parent_id
    parent_comments = []
    # link_id	The submission ID that the comment belongs to.
    # recursively get parent of comment until parent_id == comment.link_id
    while parent_id != comment.link_id:
        parent_comment = reddit.comment(id=parent_id[3:])
        parent_comments.append(parent_comment.body)
        parent_id = parent_comment.parent_id
    return parent_comments


def get_parent_submission(comment, reddit):
    # link_id	The submission ID that the comment belongs to.
    submission = reddit.submission(id=comment.link_id[3:])
    # return ' '.join(submission.title.split() + submission.selftext.split())
    return {
        'subreddit': submission.subreddit.display_name,
        'str': ' '.join(submission.title.split() + submission.selftext.split())
    }


def gen_qa_string(q, a):
    return 'Q: %s\nA: %s' % (q, a)


def gen_formatted_as_qa(comment, reddit):
    parents = get_parent_comments(comment, reddit)
    nparents = len(parents)
    submission = get_parent_submission(comment, reddit)

    # https://openai.com/blog/better-language-models/#task1
    # format the context/paragraph
    sl = ['In subreddit: %s' % submission['subreddit'], submission['str']]

    if nparents > 1:
        for i in range(1, nparents):
            sl.append(gen_qa_string(parents[i - 1], parents[i]))
    else:
        # default, if top-level comment
        qstr = 'What do you think?'
        if nparents == 1:
            qstr = parents[0]
        sl.append(gen_qa_string(qstr, comment.body))
    return '\n\n'.join(sl)


if __name__ == '__main__':
    # spez BennyFeldman whiskeysquid
    parser = argparse.ArgumentParser(description='dump user comments')
    parser.add_argument('-user', default='spez', type=str)
    parser.add_argument('-num-comments', default=100, type=int)
    args = parser.parse_args()

    with open('praw.cred') as f:
        r = praw.Reddit(**json.load(f))
        # print('API state\tread only: %s, user: %s' % (r.read_only, r.user.me()))

    u = r.redditor(args.user)
    comments_gen = u.comments.new(limit=args.num_comments)
    with open(os.path.join('data_reddit', '%s.txt' % u.name), 'a+') as f:
        i = 0
        print('getting %d new comments for user: %s' % (args.num_comments, args.user))
        for c in comments_gen:
            print('[%d/%d] parsing comment id: %s' % (i, args.num_comments, c.id))
            f.write(gen_formatted_as_qa(c, r) + '\n'*2)
            i += 1
