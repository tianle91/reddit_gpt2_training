import argparse
import json
import os

import praw

from data_reddit import gen_qa_training

parser = argparse.ArgumentParser(description='dump user comments')
parser.add_argument('-user', default='spez', type=str)
parser.add_argument('-num-comments', default=1, type=int)
args = parser.parse_args()

with open('praw.cred') as f:
    r = praw.Reddit(**json.load(f))
    print('API state\tread only: %s, user: %s' % (r.read_only, r.user.me()))

u = r.redditor(args.user)
comments_gen = u.comments.new(limit=args.num_comments)
writedir = os.path.join('data_reddit', u.name)
if not os.path.isdir(writedir):
    os.mkdir(writedir)

i = 0
print('getting %d new comments for user: %s' % (args.num_comments, args.user))
for c in comments_gen:
    writepath = os.path.join(writedir, '%s.txt' % c.id)
    if not os.path.isfile(writepath):
        with open(writepath, 'w') as f:
            s = gen_qa_training(c, r)
            f.write(s)
            print('[%d/%d] | comment id: %s | tail: %s' %\
                  (i, args.num_comments, c.id, ' '.join(s.split())[-20:]))
    else:
        print('[%d/%d] | comment id: %s | exists!' % \
              (i, args.num_comments, c.id))
    i += 1
print('done!')
