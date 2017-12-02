from __future__ import division
import boto3
import nltk
from nltk.stem.snowball import SnowballStemmer
from project.NLP.profanity_filter.profanity import contains_profanity

dynamodb = boto3.resource('dynamodb')
dataset_table = dynamodb.Table('cc414-nb-nlp-dataset')

stemmer = SnowballStemmer("english")

training_data = []


def add_training_data():
    global training_data
    if not training_data:
        response = dataset_table.scan()
        training_data = response['Items']


add_training_data()

corpus_words = {}
class_words = {}
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    class_words[c] = []


for data in training_data:
    for word in nltk.word_tokenize(data['sentence']):
        if word not in ["?", "'s"]:
            stemmed_word = stemmer.stem(word.lower())
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1
            class_words[data['class']].append(stemmed_word)


def calculate_class_score(sentence, class_name):
    score = 0
    for word in nltk.word_tokenize(sentence):
        if stemmer.stem(word.lower()) in class_words[class_name]:
            score += 1
    return score


def calculate_class_score_commonality(sentence, class_name):
    score = 0
    for word in nltk.word_tokenize(sentence):
        if stemmer.stem(word.lower()) in class_words[class_name]:
            score += (1 / corpus_words[stemmer.stem(word.lower())])
    return score


def classify(sentence):
    high_class = None
    high_score = 0
    classResults = []
    for c in class_words.keys():
        score = calculate_class_score_commonality(sentence, c)
        classResults.append({'keyword': c, 'score': score})
        if score > high_score:
            high_class = c
            high_score = score
    print("Highest:", high_class, high_score)
    for i in classResults:
        print(i)
    return classResults


maxScores = {}


def calculateMaxScores():
    for data in training_data:
        score = calculate_class_score_commonality(data['sentence'], data['class'])
        if (data['class'] not in maxScores.keys()):
            maxScores[data['class']] = ([score])
        else:
            maxScores[data['class']].append(score)


calculateMaxScores()


def compareMaxPoints(result):
    scores = maxScores[result['keyword']]
    if scores:
        maxScore = sum(scores) / len(scores)
    else:
        return 0
    return maxScore


def removeConceptWord(concept, sentence):
    newSentence = sentence.replace(concept, '')
    return newSentence


def get_answer_feedback(concept, sentence):
    # return 'Mock feedback.'
    if not contains_profanity(sentence):
        sentence = removeConceptWord(concept, sentence)
        concept = concept.lower()
        results = classify(sentence)
        orderedScores = []
        appropiateResult = None

        for i in results:
            orderedScores.append(i['score'])
            if (concept == i['keyword']):
                appropiateResult = i
                print("success: ", concept, "was found with", i['score'])

        orderedScores.sort(reverse=True)
        # Result is not in the class keywords
        if (appropiateResult is None):
            return ("Don't think that answer is correct")
            # return PossibleResults.NOT_THE_SAME
        maxScore = compareMaxPoints(appropiateResult)
        # result was the highest scoring class
        if (appropiateResult['score'] == 0):
            return ("No information found related to this sentence.")
            # return PossibleResults.NOT_THE_SAME
        if (orderedScores[0] == appropiateResult['score']):
            if (appropiateResult['score'] > maxScore / 2):
                return ("Seems like a good answer.")
                # return PossibleResults.SUCCESSFUL
            else:
                return ("You're in the right path but try to be more specific.")
                # return PossibleResults.AMBIGUOUS
        # Result isnt the highest scoring class
        if (appropiateResult['score'] > maxScore / 2):
            difference = orderedScores[0] - orderedScores[len(orderedScores) - 1]
            intervals = difference / len(orderedScores)
            if (maxScore - intervals * 2 > appropiateResult['score']):
                print("Very likely you're correct")
                # return PossibleResults.SUCCESSFUL
            else:
                return ("Ambiguous answer, might be mixing the answer with another concept.")
                # return PossibleResults.AMBIGUOUS
        return ("Not even close to the answer")
        # return PossibleResults.NOT_THE_SAME
    else:
        return 'Answer contains profanity.'


def grade_answer(concept, sentence):
    # return [True, 1]
    if contains_profanity(sentence):
        return [False, 0]
    sentence = removeConceptWord(concept, sentence)
    concept = concept.lower()
    results = classify(sentence)
    orderedScores = []
    appropiateResult = None

    for i in results:
        orderedScores.append(i['score'])
        if (concept == i['keyword']):
            appropiateResult = i
    orderedScores.sort(reverse=True)
    # Result is not in the class keywords
    if (appropiateResult is None):
        return [False, 0]
    maxScore = compareMaxPoints(appropiateResult)
    # result was the highest scoring class
    if (appropiateResult['score'] == 0):
        return [False, 0]
    if (orderedScores[0] == appropiateResult['score']):
        if (appropiateResult['score'] > maxScore / 2):
            return [True, 1]
        else:
            return [True, appropiateResult['score'] / maxScore]
    # Result isnt the highest scoring class
    if (appropiateResult['score'] > maxScore / 2):
        difference = orderedScores[0] - orderedScores[len(orderedScores) - 1]
        intervals = difference / len(orderedScores)
        if (maxScore - intervals * 2 > appropiateResult['score']):
            return [True, appropiateResult['score'] / maxScore]
        else:
            return [False, appropiateResult['score'] / maxScore]
    return [False, 0]
