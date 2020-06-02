import boto3
import json
import time




S3_BUCKET = 'test-text-to-speech'


def start_transcription_job(job_name, audio_url, media_format):

    client = boto3.client('transcribe')
    response = client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode='en-US',
        MediaFormat=media_format,
        Media={
            'MediaFileUri': audio_url
        },
        OutputBucketName='test-text-to-speech'
    )

    return response


def wait_for_transaction_job(job_name):

    status = None
    client = boto3.client('transcribe')

    while status != "COMPLETED":

        time.sleep(1)

        response = client.get_transcription_job(
            TranscriptionJobName=job_name
        )
        status = response['TranscriptionJob']['TranscriptionJobStatus']
        print(status)

    return response


def load_transcript_from_job(job_name):

    s3 = boto3.resource('s3')
    obj = s3.Object(S3_BUCKET, '%s.json' % job_name)
    body = obj.get()['Body'].read()
    j = json.loads(body)
    transcript = j['results']['transcripts'][0]['transcript']
    return transcript
