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
    appended_misc = ""

    for cand in candidates:
        appended_lemma += cand[0] + "/"
        appended_tags += cand[1] + "/"
        if len(cand) > 2:
            # making sure the features are sorted
            misc = "Morf="
            feats_list = sorted([element.split("=") for element in cand[2:]])
            prepref = [element[1] for element in feats_list if element[0] == "Prepref"]
            pref = [element[1] for element in feats_list if element[0] == "Pref"]
            stem = [element[1] for element in feats_list if element[0] == "Stem"]
            suff = [element[1] for element in feats_list if element[0] == "Suff"]
            if prepref != []:
                misc += "".join(prepref)
                misc += "+"
            if pref != []:
                misc += "".join(pref)
                misc += "+"
            misc += cand[0]
            if stem != []:
                misc += "<" + "".join(stem) + ">"
            else:
                misc += "<X>"
            if suff != []:
                misc += "+"
                misc += "".join(suff)
            misc += "_" + cand[1]

            for key, value in kwargs.items():
                if key == 'space_after' and value:
                    misc += "|SpaceAfter=No"
            if misc == "": misc = "_"
            appended_misc += misc + "/"

            feats_string = "|".join("=".join(element) for element in feats_list if element[0] not in ["Prepref", "Pref", "Stem", "Suff"])
            if len(candidates) > 1:
                feats_string = ambiguous_features_template.format(cand[1], feats_string)
            appended_features += feats_string + "/"
        else:
            misc = "Morf="
            misc += cand[0]
            misc += "<X>"
            misc += "_" + cand[1]
            appended_misc += misc + "/"

    
    if appended_features == "":
        appended_features += "_/"

    appended_lemma = appended_lemma[:-1]
    appended_tags = appended_tags[:-1]
    appended_features = appended_features[:-1]
    appended_misc = appended_misc[:-1]

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
    new_row[9] = appended_misc

    return '\t'.join(new_row)
