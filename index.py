import file_utils
import models
import sound_stuff
import s3_utils
import uuid


# Original location of audio file to transcribe
origin_url = 'https://hwcdn.libsyn.com/p/f/f/7/ff7f1a6e683c7dbb/37-_Go_East_Young_Man.mp3?c_id=1453698&cs_id=1453698&expiration=1590267009&hwt=216c6584f6ef2a42be776e773cc7d40b'


bucket = 'test-text-to-speech'
filename = 'bronze-age-collapse.mp3'

# print('Downloading file...')
file_utils.download_file_from_url(origin_url, filename)
# print('...done')

print('Uploading to s3...')
response = s3_utils.upload_file(filename, 'test-text-to-speech')
print(response)
print('...done')

print('Deleting local copy...')
file_utils.delete_file(filename)
print('...done')

job_name = 'job-%s' % uuid.uuid1()
print(job_name)

object_url = "https://%s.s3.amazonaws.com/%s" % (bucket, filename)
print(object_url)


print('Starting transcription job...')
response = sound_stuff.start_transcription_job(job_name, object_url, 'mp3')
print(response)
print('...done')

print('Waiting on transcription task...')
sound_stuff.wait_for_transaction_job(job_name)
print('...done')

print("Loading Text File...")
text = sound_stuff.load_transcript_from_job(job_name)
print("...done")

print("Extracting sentences...")
from spacy.lang.en import English
nlp = English()
sbd = nlp.create_pipe('sentencizer')
nlp.add_pipe(sbd)
doc = nlp(text)
sentences = [sentence.text for sentence in doc.sents]
print("...done")

file_utils.write_json('sentences.json', sentences, 3)

print("Loading summarizer...")
summarizer = models.get_summarizer_model()
print("...done")

print("Summarizing...")

summary_indices = {}

for i in range(1,10):
    ratio = i/10
    summary = summarizer(text, ratio=ratio)
    doc = nlp(summary)
    summary_sentences = [sentence.text for sentence in doc.sents]
    indices = [sentences.index(summary_sentence) for summary_sentence in summary_sentences]
    summary_indices[i] = indices

output = {
    'audio_url': object_url,
    'sentences': sentences,
    'summary_indices': summary_indices
}

file_utils.write_json('summary_output.json', output, indent=3)

