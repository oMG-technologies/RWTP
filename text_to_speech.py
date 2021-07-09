import os


class TextToSpeech():
    def __init__(self, id, word, target_language):
        self.id = id
        self.word = word
        self.target_language = target_language

    def convert(self):
        from google.cloud import texttospeech

        ''' Synthesizes speech from the input string of text or ssml.

            Note: ssml must be well-formed according to:
                https://www.w3.org/TR/speech-synthesis/
        '''

        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(
            text=self.word)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.target_language,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with
        # the selected voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        filename = '{}_{}.mp3'.format(self.id, self.word)
        path_to_file = os.path.join(
            os.path.dirname(__file__), 'media', filename)
        with open(path_to_file, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "{}"'.format(path_to_file))


TextToSpeech(1, 'environment', 'en-US').convert()
