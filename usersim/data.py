from praw.exceptions import ClientException

QSTR = 'What do you think?'


def get_parent_comments(comment, reddit):
    '''return list of [parent_comment.body]'''
    parent_id = comment.parent_id
    parent_comments = []
    while parent_id != comment.link_id:
        parent_comment = reddit.comment(id=parent_id[3:])
        parent_comments.append(parent_comment.body)
        parent_id = parent_comment.parent_id
    return parent_comments


def format_submission(submission):
    return '\n\n'.join([
        'In subreddit: %s' % submission.subreddit.display_name,
        'Title: %s' % submission.title,
        'Body: %s' % submission.selftext
    ])


def get_parent_submission(comment, reddit):
    return reddit.submission(id=comment.link_id[3:])


def gen_qa_string(q, a):
    q = ' '.join(q.split())
    a = ' '.join(a.split())
    return 'Q: %s\nA: %s' % (q, a)


def gen_qa_training(comment, reddit):
    # https://openai.com/blog/better-language-models/#task1
    # format the context/paragraph
    sl = [format_submission(get_parent_submission(comment, reddit))]
    comments_chain = [comment.body] + get_parent_comments(comment, reddit) + [QSTR]
    for i in range(len(comments_chain) - 1, 0, -1):
        sl.append(gen_qa_string(comments_chain[i], comments_chain[i - 1]))
    return '\n\n'.join(sl)


def gen_qa_infer(url, reddit):
    try:
        # if it's a comment, then generate QA format
        comment = reddit.comment(url=url)
        sl = [gen_qa_training(comment, reddit), gen_qa_string(comment.body, '')]
    except ClientException:
        # otherwise, it's a submission, then generate context with only Q
        submission = reddit.submission(url=url)
        sl = [format_submission(submission), gen_qa_string(QSTR, '')]
    return '\n\n'.join(sl)


if __name__ == '__main__':
    import praw
    r = praw.Reddit()

    breakstr = '-' * 100
    print(breakstr)
    print('test gen_qa_training on comments...')
    print(breakstr)
    u = r.redditor('spez')
    comments_gen = u.comments.new(limit=2)
    for c in comments_gen:
        print(c.id)
        print(gen_qa_training(c, r))

    print(breakstr)
    print('test gen_qa_infer on submission...')
    print(breakstr)
    print(gen_qa_infer(
        'https://www.reddit.com/r/AskReddit/comments/d2anfy/how_are_you_doing_today_you_sexy_mother_fucker/', r))

    print(breakstr)
    print('test gen_qa_infer on comment...')
    print(breakstr)
    print(gen_qa_infer(
        'https://www.reddit.com/r/AskReddit/comments/d2anfy/how_are_you_doing_today_you_sexy_mother_fucker/eztp4fx', r))
