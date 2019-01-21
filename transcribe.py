from google.cloud import storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import os
import time
import inspect
import praw
from tqdm import tqdm
import ConfigParser

# Maybe add async upload? https://cloud.google.com/appengine/docs/standard/python/datastore/async

# Load config file. Note that praw loads the same file on its own to initialize itself.
config = ConfigParser.ConfigParser()
config.read('praw.ini')


# Prepare to use speech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.get('google', 'application_credentials')
client = speech.SpeechClient()
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
    # sample_rate_hertz=16000,
    language_code='en-US',
    enable_automatic_punctuation=True
    # enable_speaker_diarization=True,
    # diarization_speaker_count=3
    )

# Prepare to use Reddit
reddit = praw.Reddit('reddit')
wiki = reddit.subreddit(subreddit).wiki


# fetch audio
storage_client = storage.Client()
bucket = storage_client.get_bucket(config.get('google', 'bucket'))
audio = {}
for blob in bucket.list_blobs():
  squished_URI = 'gs://{}/{}'.format(config.get('google', 'bucket'), blob.name)
  audio[str(blob.name.rsplit('.')[0])] = types.RecognitionAudio(uri=squished_URI)
jobs = {}
output = {}
pbars = {}

import pdb; pdb.set_trace()

# Make a new Speech job for every clip in the audio dict
for name, job in audio.items():
  jobs[name] = client.long_running_recognize(config, job)
  # print(name + " transcription request submitted.")
  pbars[name] = tqdm(total=100, desc=name)

# Wait until the jobs are done, update progress bars, and finally put their results in the output dict.
while len(jobs) > 0:
  time.sleep(20)
  for name, job in jobs.items():
    if job.done() == False:
      pbars[name].update(job.metadata.progress_percent)
    else:
      output[name] = job
      jobs.pop(name)
      pbars[name].close()

# Process the results in the output dict
for name, result in output.items():
  # parse some handy names for later
  backup_file = 'backup/' + name + '.txt'
  wiki_address = 'episodes/' + name.rsplit('.')[1]
  # open a local backup file
  if not os.path.isdir('backup'):
    os.mkdir('backup')
  file = open(backup_file,'w')
  # concat all of the segments, close the backup
  for paragraph in range(0,len(result._result.results)):
    file.write(result._result.results[paragraph].alternatives[0].transcript)
  file.close()
  # push the result up to a similarly named page on the wiki
  transcript = open(backup_file,'r') # why concat twice?
  if os.path.isfile('template.txt'):
    template = open('template.txt', 'r')
    transcript_with_template = template.read() + transcript.read()
    template.close()
  else:
    transcript_with_template = transcript
  wiki[wiki_address].edit(transcript_with_template, reason='Init')
  transcript.close()



# response = operation.result(timeout=90)

# # Each result is for a consecutive portion of the audio. Iterate through
# # them to get the transcripts for the entire audio file.
# for result in response.results:
#     # The first alternative is the most likely one for this portion.
#     print(u'Transcript: {}'.format(result.alternatives[0].transcript))
#     print('Confidence: {}'.format(result.alternatives[0].confidence))





