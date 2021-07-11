import os
from google.cloud import texttospeech


class TextToSpeech():
    def get_pronunciation(
            self,
            id: str,
            word: str,
            target_language: str) -> str:
        '''Synthesizes speech from the input string of text or ssml.

            Note: ssml must be well-formed according to:
                https://www.w3.org/TR/speech-synthesis/

        Parameters
        ----------
        id : int
            unique integer for each translated word
        word : str
            an English word to be translated
        target_language : str
            the same code as the one used for translation - here just
            for organization of uploaded files
            e.g. 'en-US' or 'pl'

        Returns
        -------
        str
            [description]
        '''

        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(
            text=word)

        # Build the voice request, select the language code (e.g. "en-US") and
        # the ssml voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code=target_language,
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
        import unicodedata
        normalized_word_bytes = unicodedata.normalize(
            'NFKD', word).encode('ascii', 'ignore')
        normalized_word = normalized_word_bytes.decode('utf-8')
        filename = '{}_{}.mp3'.format(id, normalized_word)
        dirname = os.path.join(
            os.path.dirname(__file__), 'media', target_language)

        # create a language dir if necessary
        if not os.path.isdir((dirname)):
            os.makedirs(dirname)
        path_to_file = os.path.join(dirname, filename)
        with open(path_to_file, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "{}"'.format(path_to_file))
        return path_to_file
