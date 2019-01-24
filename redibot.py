import praw
import os
import ConfigParser
import re
from datetime import datetime
import time

# Load config file. Note that praw loads the same file on its own to initialize itself.
config = ConfigParser.ConfigParser()
config.read('praw.ini')

# Prepare to use Reddit
reddit = praw.Reddit('reddit')
my_sub = config.get('reddit', 'subreddit')
wiki = reddit.subreddit(my_sub).wiki


directory = []       # A list of episode pages
all_revisions = {}   # A dict of timestamp: revision
# Find all episode pages
for wp in reddit.subreddit('orbitalpodcast').wiki:
  if re.match('episodes/', wp.name):
    directory.append(wp)
# Check the date of the latest revision
for page in directory:
  for revision in page.revisions():
    all_revisions[revision['timestamp']] = revision
# Sort by revision timestamp
sorted_rev_dates = sorted(all_revisions, reverse=True)
sorted_rev_dates = sorted_rev_dates[0:10]
# Build an updated table
rev_table = ''
# If the rev table ever needs to be rebuilt:
# rev_table =  '# Recent episode page updates\r\n'
# rev_table += 'Time|Page|Reason|Author\r\n'
# rev_table += '|-|-|-|-|\r\n'
for timestamp in sorted_rev_dates:
  revision = all_revisions[timestamp]
  rev_table += '{}|{}|{}|{}\r\n'.format(datetime.utcfromtimestamp(timestamp).strftime('%A, %b %d, %H:%M'),
                                            revision['page'].name,
                                            revision['reason'],
                                            revision['author'].name)

# Find out if the table needs to be updated
index_last_revision = wiki['index'].revisions()
index_last_revision = index_last_revision.next()['timestamp']
if index_last_revision < sorted_rev_dates[0]:
  # Find out what the index looks like and where the updates table is
  old_index = wiki['index'].content_md
  old_table_location = old_index.find('# Recent episode page updates\r\nTime|Page|Reason|Author\r\n|-|-|-|-|\r\n')+67
  new_page = old_index[:old_table_location] + rev_table
  wiki['index'].edit(new_page, reason='update recent episode page updates')
  print 'Updated the updates summary table.'
else:
  print 'No updates needed to the updates summary table.'






