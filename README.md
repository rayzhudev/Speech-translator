### Speech Translator

This is a program which takes audio files and translates them to speech in another language. It does this by transcribing, then translating, then synthesising to speech.

### How to use
1. Install the required libraries.
```
pip install whisper googletrans gtts
```

2. Add your audio recordings you wish to translate to the recordings folder. Language codes can be found here https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

Then run the command
```
python translate.py recordings/YOUR_FILE_PATH LANGUAGE_CODE
```


e.g. To translate the file "Against Imperialism" to French, run the command

```
python translate.py recordings/Against\ Imperialism.wma  fr
```
3. Wait for the program to run, the final result will be placed in `translated_recordings/`.
