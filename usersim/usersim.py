import json
import os
import praw
from usersim.data import gen_qa_training, gen_qa_infer


class UserSim:
    def __init__(self, user, reddit, cache_dir='/data'):
        self.u = reddit.redditor(user)
        self.r = reddit
        self.cache_dir = cache_dir
        self.comments = {}

    def get_comments_done(self):
        for fpath in os.listdir(self.cache_dir):
            with open(fpath, 'r') as f:
                self.comments[''.join(fpath.split('.'))] = f.read()

    def get_comments_new(self, count=1000):
        for c in self.u.comments.new(limit=count):
            if c not in self.comments:
                fpath = os.path.join(self.cache_dir, '%s.txt' % c.id)
                with open(fpath, 'w') as f:
                    f.write(gen_qa_training(c, self.r))

    def get_training(self):
        return '\n\n'.join(self.comments.values())

    def get_infer(self, url):
        return gen_qa_infer(url, self.r)


if __name__ == '__main__':
    r = praw.Reddit()
    