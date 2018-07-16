def normalize_offsets(offsets: list) -> list:
    """
    Normalize the provided list of offsets by merging or removing some of them
    :param offsets: original offsets as list of tuples generated by pattern matching
    :return: cleaned list of tuples
    """
    sorted_offsets = sorted(offsets, key=lambda tup: tup[0])
    offset_to_keep = list()
    previous_start_offset, previous_end_offset, previous_type_tag = None, None, None

    for current_start_offset, current_end_offset, current_type_tag in sorted_offsets:

        # merge tags which appear as separated but are not really
        if (previous_end_offset is not None) and (previous_end_offset + 2 >= current_start_offset):
            previous_start_offset, previous_end_offset, previous_type_tag = previous_start_offset, \
                                                                            current_end_offset, \
                                                                            tag_priority(current_type_tag,
                                                                                         previous_type_tag)

        if (previous_end_offset is not None) and (previous_end_offset < current_end_offset):
            offset_to_keep.append((previous_start_offset, previous_end_offset, previous_type_tag))

        # keep longest tags when they are one on the other
        if (previous_end_offset is not None) and (previous_end_offset >= current_end_offset):
            current_start_offset, current_end_offset, current_type_tag = previous_start_offset, \
                                                                         previous_end_offset, \
                                                                         tag_priority(current_type_tag,
                                                                                      previous_type_tag)

        if current_end_offset - current_start_offset <= 2:
            current_start_offset, current_end_offset, current_type_tag = previous_start_offset, \
                                                                         previous_end_offset, \
                                                                         previous_type_tag

        previous_start_offset, previous_end_offset, previous_type_tag = (current_start_offset,
                                                                         current_end_offset,
                                                                         current_type_tag)
    if previous_start_offset is not None:
        offset_to_keep.append((previous_start_offset, previous_end_offset, previous_type_tag))
    return offset_to_keep


def tag_priority(tag1: str, tag2: str) -> str:
    """
    Apply some rules to decide which tag to keep when merging 2 offsets
    :param tag1: tag as a string
    :param tag2: tag as a string
    :return: the selected tag
    """
    if tag1 in ["PARTIE_PP", "PARTIE_PM"]:
        return tag2
    else:
        return tag1


def remove_offset_space(text: str, offsets: list):
    """
    If offset doesn't match a word boundary its type is lost
    This function remove the starting and the ending offset, if any
    More info -> https://spacy.io/usage/linguistic-features
    Test code:
    ----
    import spacy
    from spacy.gold import GoldParse
    from spacy.tokens import Doc
    nlp = spacy.blank('fr')
    doc2 = nlp('Who is Chaka Khan popo?')
    gold2 = GoldParse(doc2, entities=[(7, 18, 'PERSON')])
    print(gold2.ner)
    ----
    :param text: original text
    :param offsets: list of original offsets for this text
    :return: list of new offsets fixed
    """
    result = list()
    for start_offset, end_offset, type_name in offsets:
        new_start = start_offset + 1 if text[start_offset].isspace() else start_offset
        # remove 1 because the closing offset is not included in the selection in Python
        new_end = end_offset - 1 if text[end_offset - 1].isspace() else end_offset
        result.append((new_start, new_end, type_name))
    return result
