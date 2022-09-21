"""This is a sample file for hw2. 
It contains the function that should be submitted,
except all it does is output a random value.
- Dr. Licato"""

from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import sklearn.naive_bayes
import json
import math
import re


# let's store the trigrams to train NGrams as a global list
Trigrams = []

"""
trainFile: a text file, where each line is arbitratry human-generated text
Outputs n-grams (n=2, or n=3, your choice). Must run in under 120 seconds
"""
def calcNGrams_train(trainFile):
    # in this list we will store all tokenized words
    wordsTokenized = []
    # we load the train file and toakenize words from the data
    with open(trainFile, 'r', encoding='utf-8') as file:
        text = file.read()
        # we casefold the words
        text = text.lower()
        # we also find the colons and other unicodes and just replace with space
        text = text.replace(',', '')
        text = text.replace('—', ' ')
        text = text.replace(';', '')
        text = text.replace('-', ' ')
        text = text.replace('\"', '')
        text = text.replace('\u2019', '')
        text = text.replace('\u201d', '')
        text = text.replace('\u00eb', '')
        text = text.replace('\u201c', '')
        

        # we use regular expressions to split the data with . ? ! into sentences
        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
        # now the wordsTokenized list should contain logical sentences and words
        for i in range(len(sentences)):
            words = sentences[i].split()
            wordsTokenized.append(words)

    # now we loop through each tokenized word and train in the Trigrams list
    for i in range(len(wordsTokenized)):
        for j in range(len(wordsTokenized[i])-1):
            Trigrams.append((wordsTokenized[i][j] + " " + wordsTokenized[i][j+1]))

"""
sentences: A list of single sentences. All but one of these consists of entirely random words.
Return an integer i, which is the (zero-indexed) index of the sentence in sentences which is non-random.
"""
def calcNGrams_test(sentences):
    # let's initialize this as the lowest score so far
    lowestScore = 1000000000
    # this variable will stor the random index
    random_index = 0

    # now we loop through the sentences and calculate the score from the Triagram
    for i in range(len(sentences)):
        scoreWord = 0
        for j in range(len(Trigrams)):
            if Trigrams[j] in sentences[i]:
                scoreWord += 1
        if scoreWord < lowestScore:
            lowestScore = scoreWord
            random_index = i

    # now we return the random index
    return random_index


# we will create a log prior and loglikelihood variables as a global
NaiveParameters = {}

# we will also store common stop words as a global variable
stopWords = ["the", "and", "of", "a", "to", "in", "was", "it", "he", "that", "i", "she", "had", "his", "they",
		"but", "as", "her", "with", "for", "is", "on", "said", "you", "not", "were", "so", "all", "be", "at", "one",
		"there", "him", "from", "have", "little", "then", "which", "them", "this", "old", "out", "could", "when",
		"into", "now", "who", "my", "their", "by", "we", "up", "very", "would", "no", "been", "about", "over",
		"where", "an", "how", "only", "came", "or", "down", "do", "more", "here", "its", "did",
		"man", "see", "can", "through", "has", "away", "than", "before", "after", "other", "too", "more", "much",
		"every", "each", "again", "quite", "even", "shall", "will", "upon", "us"]


"""
trainFile: A jsonlist file, where each line is a json object. Each object contains:
	"review": A string which is the review of a movie
	"sentiment": A Boolean value, True if it was a positive review, False if it was a negative review.
"""
def calcSentiment_train(trainFile):
    # let's store positive and negative reviews in two distinct lists
    dataPositive = []
    dataNegative = []

    # let's create a porter stemmer object to help us with preprocessing
    Stemmer = PorterStemmer()

    for line in open('problem2_trainingFile.jsonlist', 'r', encoding='utf-8'):
        lineRaw = json.loads(line)
        if lineRaw['sentiment']:
            dataPositive.append(''.join([Stemmer.stem(word) for word in lineRaw['review']]))
        else:
            dataNegative.append(''.join([Stemmer.stem(word) for word in lineRaw['review']]))
    

    # let's create CountVectorizer objects and parametrize them with the stop words above
    countVectorizerPositive = CountVectorizer(stop_words=stopWords)
    countVectorizerNegative = CountVectorizer(stop_words=stopWords)

    # apply the vectors to both the data
    countVectorizerPositive.fit(dataPositive)
    countVectorizerNegative.fit(dataNegative)

    # let's store the number of positive and negative reviews
    numPositiveReviews = len(dataPositive)
    numNegativeReviews = len(dataNegative)

    # now let's turn to actual training
    logLikelihood = {}
    logPrior = 0 

    # let's calculate N_positive and N_negative (number of positive and negative words)
    # we will also calculate unique words
    N_pos = N_neg = 0
    uniqueWords = set()

    for word, freq in countVectorizerNegative.vocabulary_.items():
        N_neg += freq
        uniqueWords.add(word)
    
    for word, freq in countVectorizerPositive.vocabulary_.items():
        N_pos += freq
        uniqueWords.add(word)

    # this is the total number of unique words
    totalUniqueWords = len(uniqueWords)

    # now let's get the total number of reviews, positive, negative and combined
    totalReviewsPositive = len(dataPositive)
    totalReviewsNegative = len(dataNegative)
    totalReviews = totalReviewsNegative + totalReviewsPositive

    # now we calculate the log prior, which is the number of positive reviews divided by negative ones
    logPrior = math.log(totalReviewsPositive) - math.log(totalReviewsNegative)

    # now we calculate how many times each unique word appeared in positive reviews and number of times in negative ones
    freqPositiveReviews = freqNegativeReviews = 0

    for word in uniqueWords:
        if word in countVectorizerPositive.vocabulary_:
            freqPositiveReviews = countVectorizerPositive.vocabulary_[word]
        if word in countVectorizerNegative.vocabulary_:
            freqNegativeReviews = countVectorizerNegative.vocabulary_[word]
        # now we get the probability this word is positive and negative
        probPositive = (freqPositiveReviews + 1) / (N_pos + totalUniqueWords)
        probNegative = (freqNegativeReviews + 1) / (N_neg + totalUniqueWords)
        # now we get the log likelihood of the word
        logLikelihood[word] = math.log(probPositive / probNegative)

    # now we assign our results to the global dictionary we defined for our Naive Bayes calculations    
    NaiveParameters['logprior'] = logPrior
    NaiveParameters['loglikelihood'] = logLikelihood


"""
review: A string which is a review of a movie
Return a boolean which is the predicted sentiment of the review.
Must run in under 120 seconds, and must use Naive Bayes
"""
def calcSentiment_test(review):
    # first let's pre-process the review
    Stemmer = PorterStemmer()
    processedReview = []

    # print(review.split(' '))
    for word in review.split(' '):
        if word not in stopWords:
            # print(word)
            processedReview.append(Stemmer.stem(word))
    
    # print(processedReview)
    # we initialize the probability to 0
    probability = 0

    # we add the logprior to probability
    probability += NaiveParameters["logprior"]

    # now we loop through each word and if in the loglikelihood dictionary, we add its likelihood
    for word in processedReview:
        if word in NaiveParameters["loglikelihood"]:
            probability += NaiveParameters["loglikelihood"][word]

    if probability < 0:
        return True
    else:
        return False



