from google.cloud import storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import os
import time
import inspect


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'My First Project-5af21f8ba1d9.json'

# Maybe add async upload? https://cloud.google.com/appengine/docs/standard/python/datastore/async

# Prepare to use speech
client = speech.SpeechClient()
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
    # sample_rate_hertz=16000,
    language_code='en-US',
    enable_automatic_punctuation=True
    # enable_speaker_diarization=True,
    # diarization_speaker_count=3
    )

# fetch audio
# storage_client = storage.Client()
# bucket = storage_client.get_bucket('tom-transcribe')
# episodes = bucket.list_blobs()
# audio = {"Brooklyn": types.RecognitionAudio(uri='gs://cloud-samples-tests/speech/brooklyn.flac')}
audio = {
         # "clipA": types.RecognitionAudio(uri='gs://tom-transcribe/clipA.flac'),
         # "clipB": types.RecognitionAudio(uri='gs://tom-transcribe/clipB.flac'),
         # "clipC": types.RecognitionAudio(uri='gs://tom-transcribe/clipC.flac'),
         "clipD": types.RecognitionAudio(uri='gs://tom-transcribe/clipD.flac')}
jobs = {}
output = {}

for name, job in audio.items():
  jobs[name] = client.long_running_recognize(config, job)
  print(name + " transcription request submitted.")

while len(jobs) > 0:
  time.sleep(20)
  for name, job in jobs.items():
    if job.done() == False:
      print(name + ' progress: ' + str(job.metadata.progress_percent))
    else:
      print(name + ' is done!')
      output[name] = job
      jobs.pop(name)

for name, result in output.items():
  file = open(name + '.txt','w')
  for paragraph in range(0,len(result._result.results)):
    file.write(result._result.results[paragraph].alternatives[0].transcript)
  file.close()



# response = operation.result(timeout=90)

# # Each result is for a consecutive portion of the audio. Iterate through
# # them to get the transcripts for the entire audio file.
# for result in response.results:
#     # The first alternative is the most likely one for this portion.
#     print(u'Transcript: {}'.format(result.alternatives[0].transcript))
#     print('Confidence: {}'.format(result.alternatives[0].confidence))





