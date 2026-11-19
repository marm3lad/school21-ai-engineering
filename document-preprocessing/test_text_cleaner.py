from text_cleaner import normalize_whitespace, remove_special_characters, normalize_case, clean_text

def test_normalize_whitespace():
    assert normalize_whitespace("") == ""
    assert normalize_whitespace("  \n\n   hello    \n  world\n\n\n") == "hello world"

def test_remove_special_characters():
    assert remove_special_characters("09:00 и 09:05 🔐одновременно. 🔐🔐  #$%^&*()") == "09 00 и 09 05 одновременно."
    assert remove_special_characters("09:00 и 09:05 одновременно. 🔐  #$%^&*()", keep_punctuation=False) == "09 00 и 09 05 одновременно"
    assert remove_special_characters("") == ""

def test_normalize_case():
    assert normalize_case("HELLO world") == "hello world"
    assert normalize_case("HELLO world", lower=False) == "HELLO world"
    assert normalize_case("") == ""

def test_clean_text():
    assert clean_text("") == ""
    assert clean_text("  \n\n   hello    \n  world\n\n\n") == "hello world"
    assert clean_text("09:00 и 09:05 одновременно. 🔐  #$%^&*()", keep_punctuation=False) == "09 00 и 09 05 одновременно"
    assert clean_text("HELLO world", lower=False) == "HELLO world"