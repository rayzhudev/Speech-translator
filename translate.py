import whisper, os, sys, googletrans, time
from gtts import gTTS

TRANSCRIBED_TEXT_DIR="transcriptions/" # The directory where transcriptions are stored
TRANSLATED_TEXT_DIR="translations/" # The directory where translations are stored
AUDIO_RECORDINGS_DIR="translated_recordings/" # The directory where translated recordings are stored
language_code="fr"  # The language code for the target language (e.g., "fr" for French)
file_name = ""

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time taken for {func.__name__}: {end-start} seconds")
        return result
    return wrapper

@timer
def main():
    transcribed_file = transcribe(file_name)
    translated_file = translate(transcribed_file)
    speech_file = synthesise_speech(translated_file)
    return

@timer
def transcribe(file_name):
    model = whisper.load_model("base")
    result = model.transcribe(file_name)
    # Remove path and file extension from file name
    _, file_name = os.path.split(file_name)
    file_name, _ = os.path.splitext(file_name)
    transcription = open(TRANSCRIBED_TEXT_DIR+file_name+"_transcribed.md","w")
    transcription.write(result["text"])
    transcription.close()
    return transcription.name

@timer
def translate(file_name):
    # Read the contents of the transcribed file
    with open(file_name, "r") as transcribed_file:
        text = transcribed_file.read()

    # Use the googletrans library to translate the text
    translator = googletrans.Translator()
    translated_text = translator.translate(text, dest=language_code).text

    # Write the translated text to a new file
    _, file_name = os.path.split(file_name)
    file_name, _ = os.path.splitext(file_name)
    translated_file = open(TRANSLATED_TEXT_DIR+file_name+"_translated.md","w")
    translated_file.write(translated_text)
    translated_file.close()
    return translated_file.name

# Change the text to speech to use the voice of the original speaker
@timer
def synthesise_speech(file_name):
    # Read the contents of the translated file
    with open(file_name, "r") as translated_file:
        text = translated_file.read()

    # Use the gTTS library to synthesise speech from the text
    tts = gTTS(text, lang=language_code)

    # Save the synthesised speech to a file
    _, file_name = os.path.split(file_name)
    file_name, _ = os.path.splitext(file_name)
    speech_file = AUDIO_RECORDINGS_DIR+file_name+"_speech.mp3"
    tts.save(speech_file)
    return speech_file

if __name__ == "__main__":
    file_name = sys.argv[1]
    # check if language code exists, otherwise use fr as default
    if len(sys.argv) >= 3:
        language_code = sys.argv[2] 
    main()