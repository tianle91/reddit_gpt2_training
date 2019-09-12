import argparse
import os

parser = argparse.ArgumentParser(description='dump user comments')
parser.add_argument('-user', default='spez', type=str)
args = parser.parse_args()

writedir = os.path.join('data_reddit', args.user)
comments = []
for fname in os.listdir(writedir):
    with open(os.path.join(writedir, fname)) as f:
        comments.append(f.read())

writepath = os.path.join('data_reddit', '%s.txt' % args.user)
with open(writepath, 'w+') as f:
    f.write('\n\n'.join(comments))
