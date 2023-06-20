import os

# todo(warn): guess language id from filenames
# the ids should be lowercased!!
KNOWN_LANG_IDS = {'ar', 'bg', 'ca', 'zh', 'hr', 'cs', 'da', 'nl', 'en', 'et', 'fi', 'fr', 'de', 'he', 'hi', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'no', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'es', 'sv', 'uk'}
def guess_language_id(file_path):
    bname = os.path.basename(file_path)
    lang_id = str.lower(bname[:2])
    # assert lang_id in KNOWN_LANG_IDS, "Unknown lang id %s from path %s" % (lang_id, file_path)
    if lang_id not in KNOWN_LANG_IDS:
        print(("Warning: Unknown lang id %s from path %s" % (lang_id, file_path)))
    return lang_id

def lang_specific_word(word, lang_id):
    if lang_id:
        # assert lang_id in KNOWN_LANG_IDS, "Unknown lang id %s" % (lang_id, )
        return "!%s_%s" % (lang_id, word)
    else:
        return word

# backoff to DEFAULT_LANG
DEFAULT_LANG_ID = "en"
ALREADY_PREFIX = "!en_"

def default_lang_specific_word(word):
    return lang_specific_word(word, DEFAULT_LANG_ID)

def get_word_index_with_spec(alphabet, word, lang_id):
    # if already prefixed (maybe by outside pre-processor, then go with it)
    if word.startswith(ALREADY_PREFIX):
        return alphabet.get_index(word)
    #
    prefixed_word = lang_specific_word(word, lang_id=lang_id)
    if prefixed_word in alphabet.instance2index:
        return alphabet.get_index(prefixed_word)
    else:
        # try to get the English(default) word's index and later its embedding
        prefixed_word = default_lang_specific_word(word)
        return alphabet.get_index(prefixed_word)
