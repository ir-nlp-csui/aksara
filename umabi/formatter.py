#!/usr/bin/python3

def to_conllu_line_with_range(line_id, surface, n_tokens):
    new_row = ['_'] * 10
    range_id = "{}-{}".format(line_id, line_id + n_tokens - 1)

    # basic info
    new_row[0] = range_id
    new_row[1] = surface

    return '\t'.join(new_row)

def to_conllu_line(line_id, surface, text, **kwargs):
    new_row = ['_'] * 10

    # Split classes
    candidates = text.split("\\n")
    candidates = [cand.split("+") for cand in candidates]

    # Disambiguation, if any (further project)
    appended_lemma = ""
    appended_tags = ""
    appended_features = ""
    ambiguous_features_template = "({} -> {})"

    for cand in candidates:
        appended_lemma += cand[0] + "/"
        appended_tags += cand[1] + "/"
        if len(cand) > 2:
            feats_string = "|".join(cand[2:])
            if len(candidates) > 1:
                feats_string = ambiguous_features_template.format(cand[1], feats_string)
            appended_features += feats_string + "/"
    
    if appended_features == "":
        appended_features += "_/"

    appended_lemma = appended_lemma[:-1]
    appended_tags = appended_tags[:-1]
    appended_features = appended_features[:-1]
    
    candidate = [appended_lemma, appended_tags, appended_features]

    # basic info
    new_row[0] = str(line_id)
    new_row[1] = surface

    # lemma
    new_row[2] = candidate[0]
    
    # surface POS-tag
    new_row[3] = candidate[1]

    # lexical feature
    new_row[5] = candidate[2]

    # misc
    misc_col = ""
    for key, value in kwargs.items():
        if key == 'space_after' and value:
            misc_col += "SpaceAfter=No"
    if misc_col == "": misc_col = "_"
    new_row[9] = misc_col
    
    return '\t'.join(new_row)
