import whisper, os, sys

AUDIO_RECORDINGS_DIR="recordings/"
TRANSCRIBED_TEXT_DIR="transcriptions/"
file_name = ""

def main():
    transcribed_file = transcribe(file_name)
    translated_file = translate(transcribed_file)
    speech_file = synthesise_speech(translated_file)
    return

def transcribe(file_name):
    model = whisper.load_model("base")
    result = model.transcribe(file_name)
    _, file_name = os.path.split(file_name)
    file_name, _ = os.path.splitext(file_name)
    transcription = open(TRANSCRIBED_TEXT_DIR+file_name+"_transcribed.md","w")
    transcription.write(result["text"])
    transcription.close()
    return transcription

def translate(file_name):
    return

def synthesise_speech(file_name):
    return

if __name__ == "__main__":
    if not sys.argv[1] == None:
        file_name = sys.argv[1]
    main()