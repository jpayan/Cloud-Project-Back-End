import boto3
import nltk
from nltk.stem.snowball import SnowballStemmer
from project.NLP.profanity_filter.profanity import contains_profanity

dynamodb = boto3.resource('dynamodb')
dataset_table = dynamodb.Table('cc414-nb-nlp-dataset')

stemmer = SnowballStemmer('english')

training_data = []
corpus_words = {}
class_words = {}
max_scores = {}


def add_training_data():
    global training_data
    if not training_data:
        response = dataset_table.scan()
        training_data = response['Items']


def set_class_words():
    global training_data
    global class_words

    add_training_data()
    classes = list(set([a['class'] for a in training_data]))
    for cls in classes:
        class_words[cls] = []


def stem_words():
    global training_data
    global corpus_words
    global class_words

    set_class_words()
    for data in training_data:
        for word in nltk.word_tokenize(data['sentence']):
            if word not in ['?', '\'s']:
                stemmed_word = stemmer.stem(word.lower())
                if stemmed_word not in corpus_words:
                    corpus_words[stemmed_word] = 1
                else:
                    corpus_words[stemmed_word] += 1
                class_words[data['class']].append(stemmed_word)


def calculate_class_score_commonality(sentence, class_name):
    global class_words
    global corpus_words

    score = 0
    for word in nltk.word_tokenize(sentence):
        if stemmer.stem(word.lower()) in class_words[class_name]:
            score += (1 / corpus_words[stemmer.stem(word.lower())])
    return score


def get_highest_score_class(sentence):
    global class_words

    stem_words()

    high_score = 0
    class_results = []
    for cls in class_words.keys():
        score = calculate_class_score_commonality(sentence, cls)
        class_results.append({'keyword': cls, 'score': score})
        if score > high_score:
            high_score = score
    print(class_results)
    return class_results


def get_scores_by_class_sentences():
    global max_scores
    global training_data

    for data in training_data:
        score = calculate_class_score_commonality(data['sentence'], data['class'])
        if data['class'] not in max_scores.keys():
            max_scores[data['class']] = [score]
        else:
            max_scores[data['class']].append(score)


def compare_max_points(result):
    global max_scores

    get_scores_by_class_sentences()

    scores = max_scores[result['keyword']]
    if scores:
        max_score = sum(scores) / len(scores)
    else:
        return 0
    return max_score


def remove_concept_word(concept, answer):
    new_sentence = answer\
        .replace(concept, '')
    return new_sentence


def get_answer_feedback(concept, answer):
    result = ''

    if not contains_profanity(answer):
        answer = remove_concept_word(concept, answer)
        concept = concept.lower()
        results = get_highest_score_class(answer)
        ordered_scores = []
        appropriate_result = None

        for res in results:
            ordered_scores.append(res['score'])
            if concept == res['keyword']:
                appropriate_result = res

        ordered_scores.sort(reverse=True)

        if appropriate_result is None:
            result = 'Don\'t think that answer is correct.'
        else:
            max_score = compare_max_points(appropriate_result)
            if appropriate_result['score'] == 0:
                result = 'No information found related to this answer.'
            elif ordered_scores[0] == appropriate_result['score']:
                if appropriate_result['score'] > max_score / 2:
                    result = 'Seems like a good answer.'
                else:
                    result = 'You\'re in the right path but try to be more specific.'
            elif appropriate_result['score'] > max_score / 2:
                difference = ordered_scores[0] - ordered_scores[len(ordered_scores) - 1]
                intervals = difference / len(ordered_scores)
                if max_score - intervals * 2 > appropriate_result['score']:
                    result = 'Very likely you\'re correct.'
                else:
                    result = 'Ambiguous answer, might be mixing the answer with another concept.'
            else:
                result = 'Not even close to the answer.'
    else:
        result = 'Answer contains profanity.'
    return result


def grade_answer(concept, answer):
    result = []

    if not contains_profanity(answer):
        answer = remove_concept_word(concept, answer)
        concept = concept.lower()
        results = get_highest_score_class(answer)
        ordered_scores = []
        appropriate_result = None

        for res in results:
            ordered_scores.append(res['score'])
            if concept == res['keyword']:
                appropriate_result = res

        ordered_scores.sort(reverse=True)

        if appropriate_result is None:
            result = [False, 1]
        else:
            max_score = compare_max_points(appropriate_result)
            if appropriate_result['score'] == 0:
                result = [False, 1]
            elif ordered_scores[0] == appropriate_result['score']:
                if appropriate_result['score'] > max_score / 2:
                    result = [True, 1]
                else:
                    result = [True, appropriate_result['score'] / max_score]
            elif appropriate_result['score'] > max_score / 2:
                difference = ordered_scores[0] - ordered_scores[len(ordered_scores) - 1]
                intervals = difference / len(ordered_scores)

                if max_score - intervals * 2 > appropriate_result['score']:
                    result = [True, appropriate_result['score'] / max_score]
                else:
                    result = [False, appropriate_result['score'] / max_score]
            else:
                result = [False, 0]
    else:
        result = [False, 0]
    return result
