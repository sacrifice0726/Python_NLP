import os
import logging
os.environ['GRPC_POLL_STRATEGY'] = 'epoll1'
from google.oauth2 import service_account
from aiy.voice.audio import AudioFormat, Recorder
from google.cloud import speech_v1 as speech 

END_OF_SINGLE_UTTERANCE = speech.types.StreamingRecognizeResponse.SpeechEventType.END_OF_SINGLE_UTTERANCE
AUDIO_SAMPLE_RATE_HZ = 16000
AUDIO_FORMAT=AudioFormat(sample_rate_hz=AUDIO_SAMPLE_RATE_HZ,
                         num_channels=1,
                         bytes_per_sample=2)

logger = logging.getLogger(__name__)

# https://cloud.google.com/speech-to-text/docs/reference/rpc/google.cloud.speech.v1
class CloudSpeechClient:
    def __init__(self, service_accout_file=None):
        if service_accout_file is None:
            service_accout_file = os.path.expanduser('~/cloud_speech.json')

        credentials = service_account.Credentials.from_service_account_file(service_accout_file)
        self._client = speech.SpeechClient(credentials=credentials)

    def _make_config(self, language_code, hint_phrases):
        return speech.types.RecognitionConfig(
            encoding=speech.types.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=AUDIO_SAMPLE_RATE_HZ,
            language_code=language_code,
            speech_contexts=[speech.types.SpeechContext(phrases=hint_phrases)])

    def recognize_bytes(self, data, language_code='en-US', hint_phrases=None):
        streaming_config=speech.types.StreamingRecognitionConfig(
            config=self._make_config(language_code, hint_phrases),
            single_utterance=True)
        responses = self._client.streaming_recognize(
            config=streaming_config,
            requests=[speech.types.StreamingRecognizeRequest(audio_content=data)])

        for response in responses:
            for result in response.results:
                if result.is_final:
                    return result.alternatives[0].transcript

        return None

    def recognize(self, language_code='en-US', hint_phrases=None):
        streaming_config=speech.types.StreamingRecognitionConfig(
            config=self._make_config(language_code, hint_phrases),
            single_utterance=True)

        with Recorder() as recorder:
            chunks = recorder.record(AUDIO_FORMAT,
                                     chunk_duration_sec=0.1,
                                     on_start=self.start_listening,
                                     on_stop=self.stop_listening)

            requests = (speech.types.StreamingRecognizeRequest(audio_content=data) for data in chunks)
            responses = self._client.streaming_recognize(config=streaming_config, requests=requests)

            for response in responses:
                if response.speech_event_type == END_OF_SINGLE_UTTERANCE:
                    recorder.done()

                for result in response.results:
                    if result.is_final:
                        return result.alternatives[0].transcript

        return None

    def start_listening(self):
        from spt.tts import say
        say('start listening')
        logger.info('Start listening.')

    def stop_listening(self):
        logger.info('Stop listening.')
