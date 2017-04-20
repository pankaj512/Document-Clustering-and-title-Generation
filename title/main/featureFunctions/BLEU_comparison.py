# -*- coding: utf-8 -*-
from nltk.translate.bleu_score import sentence_bleu as bleu


# Human evaluations of machine translation outputs require considerable effort and are expensive.
# Human evaluations can take days or even weeks to finish so a new scoring system was developed to
# automate this process of evaluation. This method is commonly referred to as BLEU Score

def get_bleu_score(candidate_text, full_text, N=3):
    all_words = []
    for line in full_text:
        words = line.split()  # word/pos-tag pair
        for word in words:
            word = word.rsplit('/', 1)[0]
            all_words.append(word)

    weight = 1.0 / N
    bleu_score = 0.0
    candidate_seq = candidate_text.split()
    candidate_seq = [word.rsplit('/', 1)[0] for word in candidate_seq]

    for index in range(len(candidate_seq) - 2):
        bleu_score += bleu([all_words], candidate_seq[index: index + 3], [weight])

    return bleu_score
