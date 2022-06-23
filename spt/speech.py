def get_hints(language_code):
    return None

def locale_language():
    language = "zh-TW" 
    return language

def speech_to_text():
    import argparse
    import logging
    from aiy.board import Board
    from assistant.cloudspeech import CloudSpeechClient

    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    while True:
        text = client.recognize(language_code=args.language,
                                hint_phrases=hints)
        if text is not None:
            break
    return text
