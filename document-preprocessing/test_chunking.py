from chunking import chunk_fixed_size


# Перекрытие чанков
def test_chunks_with_overlap():
    tokens = ["a", "b", "c", "d", "e"]
    result = chunk_fixed_size(tokens, chunk_size=3, overlap_size=1)
    assert result == [["a", "b", "c"], ["c", "d", "e"]]


# Пустой список
def test_empty_tokens():
    result = chunk_fixed_size([], chunk_size=3, overlap_size=1)
    assert result == []


# Токенов меньше чанка
def test_tokens_less_than_chunk_size():
    tokens = ["a", "b"]
    result = chunk_fixed_size(tokens, chunk_size=3, overlap_size=1)
    assert result == [["a", "b"]]