import os
from datetime import datetime
from data import gen_qa_training, gen_qa_infer


class UserSim:
    def __init__(self, user, reddit, cache_dir='cache'):
        self.u = reddit.redditor(user)
        self.r = reddit
        cache_dir=os.path.join(cache_dir, user)
        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir)
        self.cache_dir = cache_dir
        self.comments = {}

    def get_comments_done(self):
        # consider using file path as value instead if there's a lot of data
        for fpath in os.listdir(self.cache_dir):
            with open(os.path.join(self.cache_dir, fpath), 'r') as f:
                self.comments[''.join(fpath.split('.txt'))] = f.read()

    def get_comments_new(self, count=1000):
        i = 0
        for c in self.u.comments.new(limit=count):
            if c.id not in self.comments:
                s = gen_qa_training(c, self.r)
                print ('[%.0f/%.0f] id: %s, time: %s, s: %s' % (
                    i,
                    count,
                    c.id,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    ' '.join(s.split())[-50:]
                ))
                self.comments[c.id] = s
                fpath = os.path.join(self.cache_dir, '%s.txt' % c.id)
                with open(fpath, 'w') as f:
                    f.write(s)
            else:
                print ('[%.0f/%.0f] id: %s, time: %s, s: %s' % (
                    i,
                    count,
                    c.id,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    '[exists!]'
                ))
            i += 1

    def get_training(self):
        return '\n\n'.join(self.comments.values())

    def get_infer(self, url):
        return gen_qa_infer(url, self.r)


if __name__ == '__main__':
    import praw
    import argparse

    parser = argparse.ArgumentParser(description='dump user comments')
    parser.add_argument('-user', default='spez', type=str)
    parser.add_argument('-num-comments', default=10, type=int)
    parser.add_argument('-output', default='/output', type=str)
    args = parser.parse_args()

    usim = UserSim(user=args.user, reddit=praw.Reddit(), cache_dir=args.output)
    usim.get_comments_done()
    usim.get_comments_new(args.num_comments)

    s = usim.get_training()
    fpath = os.path.join(args.output, '%s.txt' % args.user)
    with open(fpath, 'w+') as f:
        f.write(s)
