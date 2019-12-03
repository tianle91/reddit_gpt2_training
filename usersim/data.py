from praw.exceptions import ClientException


def get_parent_comments(comment, reddit):
    '''return list of [(parent_comment.author.name, parent_comment.body), ...]'''
    parent_id = comment.parent_id
    parent_comments = []
    while parent_id != comment.link_id:
        parent_comment = reddit.comment(id=parent_id[3:])
        parent_comments.append((
            parent_comment.author.name if parent_comment.author is not None else '[deleted]',
            parent_comment.body
        ))
        parent_id = parent_comment.parent_id
    return parent_comments


def format_submission(submission):
    sl = ['<r/%s>: %s' % (submission.subreddit.display_name, submission.title)]
    if len(submission.selftext) > 0:
        sl.append(submission.selftext)
    return '\n\n'.join(sl)


def get_parent_submission(comment, reddit):
    return reddit.submission(id=comment.link_id[3:])


def gen_comment_string(user, body):
    return '<u/%s>: %s' % (user, body)


def gen_qa_training(comment, redditor, reddit):
    # https://openai.com/blog/better-language-models/#task1
    # format the context/paragraph
    sl = [format_submission(get_parent_submission(comment, reddit))]
    for u, s in get_parent_comments(comment, reddit)[::-1]:
        sl.append(gen_comment_string(u, s))
    sl.append(gen_comment_string(redditor.name, comment.body))
    return '\n\n'.join(sl)


def gen_qa_infer(url, redditor, reddit):
    try:
        # if it's a comment, then generate QA format
        comment = reddit.comment(url=url)
        sl = [gen_qa_training(comment, comment.author, reddit)]
    except ClientException:
        # otherwise, it's a submission, then generate context with only Q
        submission = reddit.submission(url=url)
        sl = [format_submission(submission)]
    return '\n\n'.join(sl + [gen_comment_string(redditor.name, '')])


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
        print(gen_qa_training(c, u, r))

    print(breakstr)
    print('test gen_qa_infer on submission...')
    print(breakstr)
    print(gen_qa_infer(
        'https://www.reddit.com/r/AskReddit/comments/d2anfy/how_are_you_doing_today_you_sexy_mother_fucker/',
        u,
        r
    ))

    print(breakstr)
    print('test gen_qa_infer on comment...')
    print(breakstr)
    print(gen_qa_infer(
        'https://www.reddit.com/r/AskReddit/comments/d2anfy/how_are_you_doing_today_you_sexy_mother_fucker/eztp4fx',
        u,
        r
    ))
