import argparse
import os
import json

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


def clean_str(s):
    return ' '.join(s.split())


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
    parser = argparse.ArgumentParser(description='dump user comments')
    parser.add_argument('-user', default='spez', type=str)
    parser.add_argument('-num-comments', default=100, type=int)
    args = parser.parse_args()

    with open('praw.cred') as f:
        r = praw.Reddit(**json.load(f))
        print('API state\tread only: %s, user: %s' % (r.read_only, r.user.me()))

    u = r.redditor(args.user)
    comments_gen = u.comments.new(limit=args.num_comments)
    directory = os.path.join('data_reddit', '[u]_%s' % u.name)
    if not os.path.isdir(directory):
        os.mkdir(directory)

    for c in comments_gen:
        fname = os.path.join(directory, 'comment_id_%s.txt' % c.id)
        if not os.path.isfile(fname):
            with open(fname, 'w') as f:
                qatemp = gen_formatted_as_qa(c, r)
                print('-' * 100)
                print('id: %s' % c.id)
                print('-' * 100)
                print(qatemp)
                f.write(qatemp)
        else:
            print ('exists: %s' % fname)