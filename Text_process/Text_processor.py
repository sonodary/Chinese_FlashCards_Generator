import jieba
import re
import pandas as pd
import os

current_directory = os.getcwd()

# This function takes two inputs:
# Name of the file that contains Chinese text (without txt)
# File of dictionary
# The text will be cut into words and create a csv file that contains
# the vocabulary, translation, and pinyin based on the words in the text file.
# Prerequisite: the package jieba needs to be installed


def process(file_name, dictionary):
    with open(f"{current_directory}/Customized_words/{file_name}.txt") as file:
        lines = file.read()
        # Split the chunk of sentences into a sentence
        split = re.split('。|, |，|! |\n |？', lines)

    vocabulary = []
    translation = []
    pinyin = []

    # Loop over a list of sentences
    for sentence in split:
        # Cut each list of sentence into a list of words
        cut_result = jieba.lcut(sentence)
        # Loop over a list of words
        for word in cut_result:
            # Add vocabulary, translation, and pinyin to each list
            if word in dictionary:
                vocabulary.append(word)
                translation_unlisted = '\n'.join(dictionary[word]["english"])
                translation.append(translation_unlisted)
                pinyin.append(dictionary[word]["pinyin"])

    # Create a dictionary based on the lists
    vocab_dict = {"Vocabulary": vocabulary, "Translation": translation, "Pinyin": pinyin}
    df = pd.DataFrame(vocab_dict)
    # Save as a csv file
    df.to_csv(f'{current_directory}/Customized_words/{file_name}.csv', index=False)




