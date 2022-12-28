import whisper, os, sys, googletrans, time
from gtts import gTTS

RECORDINGS_DIR="recordings/" # The directory where audio files to be converted are stored
TRANSCRIBED_TEXT_DIR="transcriptions/" # The directory where transcriptions are stored
TRANSLATED_TEXT_DIR="translations/" # The directory where translations are stored
AUDIO_RECORDINGS_DIR="translated_recordings/" # The directory where translated recordings are stored

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time taken for {func.__name__}: {end-start} seconds")
        return result
    return wrapper

@timer
def main(file_name, language_code):
    # skip steps if the file already exists
    _, file_name = os.path.split(file_name)
    file_name, file_ext = os.path.splitext(file_name)
    if not os.path.exists(TRANSCRIBED_TEXT_DIR + file_name + "_transcribed.md"):
        transcribe(RECORDINGS_DIR + file_name + file_ext, file_name)
    if not os.path.exists(TRANSLATED_TEXT_DIR + file_name + "_translated.md"):
        translate(TRANSCRIBED_TEXT_DIR + file_name + "_transcribed.md", file_name, language_code)
    if not os.path.exists(AUDIO_RECORDINGS_DIR + file_name + "_translated_audio.mp3"):
        synthesise_speech(TRANSLATED_TEXT_DIR + file_name + "_translated.md", file_name, language_code)
    return

@timer
def transcribe(file_path, output_file):
    print("Starting transcription")
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    transcription = open(TRANSCRIBED_TEXT_DIR+output_file+"_transcribed.md","w")
    transcription.write(result["text"])
    transcription.close()
    return

@timer
def translate(file_path, output_file, language_code):
    print("Starting translation")
    # Read the contents of the transcribed file
    with open(file_path, "r") as transcribed_file:
        text = transcribed_file.read()

    # Use the googletrans library to translate the text
    translator = googletrans.Translator()
    translated_text = translator.translate(text, dest=language_code).text

    translated_file = open(TRANSLATED_TEXT_DIR+output_file+"_translated.md","w")
    translated_file.write(translated_text)
    translated_file.close()
    return

# Change the text to speech to use the voice of the original speaker
@timer
def synthesise_speech(file_path, output_file, language_code):
    print("Starting speech synthesis")
    # Read the contents of the translated file
    with open(file_path, "r") as translated_file:
        text = translated_file.read()

    # Use the gTTS library to synthesise speech from the text
    tts = gTTS(text, lang=language_code)

    speech_file = AUDIO_RECORDINGS_DIR+output_file+"_translated_audio.mp3"
    tts.save(speech_file)
    return

if __name__ == "__main__":
    file_name = sys.argv[1]
    # check if language code exists, otherwise use fr as default
    if len(sys.argv) >= 3:
        language_code = sys.argv[2]
    else:
        language_code = "fr"
    main(file_name, language_code)