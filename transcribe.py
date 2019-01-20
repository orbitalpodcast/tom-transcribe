from google.cloud import storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import os
import time
import inspect
import praw
from tqdm import tqdm

# Maybe add async upload? https://cloud.google.com/appengine/docs/standard/python/datastore/async

# Prepare to use speech
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'My First Project-5af21f8ba1d9.json'
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
reddit = praw.Reddit('bot1')
wiki = reddit.subreddit('orbitalpodcast').wiki


# fetch audio
# storage_client = storage.Client()
# bucket = storage_client.get_bucket('tom-transcribe')
# episodes = bucket.list_blobs()
# audio = {"Brooklyn": types.RecognitionAudio(uri='gs://cloud-samples-tests/speech/brooklyn.flac')}
audio = {
         # "clipA": types.RecognitionAudio(uri='gs://tom-transcribe/clipA.flac')}
         # "clipB": types.RecognitionAudio(uri='gs://tom-transcribe/clipB.flac'),
         # "clipC": types.RecognitionAudio(uri='gs://tom-transcribe/clipC.flac'),
         "Episode-192": types.RecognitionAudio(uri='gs://tom-transcribe/Episode-192.flac')}
jobs = {}
output = {}
pbars = {}

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
  wiki_address = 'episodes/' + name[8:11]
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
  wiki[wiki_address].edit(transcript_with_template, reason='Added Raw Transcript')
  transcript.close()



# response = operation.result(timeout=90)

# # Each result is for a consecutive portion of the audio. Iterate through
# # them to get the transcripts for the entire audio file.
# for result in response.results:
#     # The first alternative is the most likely one for this portion.
#     print(u'Transcript: {}'.format(result.alternatives[0].transcript))
#     print('Confidence: {}'.format(result.alternatives[0].confidence))





