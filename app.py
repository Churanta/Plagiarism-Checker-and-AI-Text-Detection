from flask import Flask, request, render_template
import re
import math
import string

app = Flask("__name__")

# Define a threshold for detecting AI-generated text
ai_generated_threshold = 0.8


def calculate_ai_percentage(text):
    # Remove punctuation and numbers from the text
    text = re.sub(f"[{string.punctuation}0-9]", "", text)

    # Calculate the ratio of unique words to total words
    words = text.lower().split()
    unique_words = set(words)
    unique_ratio = len(unique_words) / len(words)

    # Calculate the AI text percentage
    ai_percentage = (1 - unique_ratio) * 100
    return ai_percentage


@app.route("/")
def loadPage():
    return render_template(
        'index.html', query="", percentage=0, plagiarized_texts=[], ai_text=""
    )


@app.route("/", methods=['POST'])
def detect_plagiarism_and_ai_text():
    try:
        universalSetOfUniqueWords = []
        matchPercentage = 0
        plagiarizedTexts = []

        ####################################################################################################

        inputQuery = request.form['query']
        lowercaseQuery = inputQuery.lower()

        # Replace punctuation by space and split
        queryWordList = re.sub("[^\w]", " ", lowercaseQuery).split()

        for word in queryWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        ####################################################################################################

        fd = open("database1.txt", "r")
        database1 = fd.read().lower()

        # Replace punctuation by space and split
        databaseWordList = re.sub("[^\w]", " ", database1).split()

        for word in databaseWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        ####################################################################################################

        queryTF = []
        databaseTF = []

        for word in universalSetOfUniqueWords:
            queryTfCounter = 0
            databaseTfCounter = 0

            for word2 in queryWordList:
                if word == word2:
                    queryTfCounter += 1
            queryTF.append(queryTfCounter)

            for word2 in databaseWordList:
                if word == word2:
                    databaseTfCounter += 1
            databaseTF.append(databaseTfCounter)

        dotProduct = 0
        for i in range(len(queryTF)):
            dotProduct += queryTF[i] * databaseTF[i]

        queryVectorMagnitude = 0
        for i in range(len(queryTF)):
            queryVectorMagnitude += queryTF[i] ** 2
        queryVectorMagnitude = math.sqrt(queryVectorMagnitude)

        databaseVectorMagnitude = 0
        for i in range(len(databaseTF)):
            databaseVectorMagnitude += databaseTF[i] ** 2
        databaseVectorMagnitude = math.sqrt(databaseVectorMagnitude)

        matchPercentage = (
                dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

        # Identify plagiarized texts
        for word in queryWordList:
            if word in databaseWordList and word not in plagiarizedTexts:
                plagiarizedTexts.append(word)

        output = "%0.02f%% Plagiarism Found" % matchPercentage

        ####################################################################################################

        ai_percentage = calculate_ai_percentage(inputQuery)
        is_ai_text = ai_percentage > ai_generated_threshold

        return render_template(
            'index.html',
            query=inputQuery,
            percentage=matchPercentage,
            output=output,
            plagiarized_texts=plagiarizedTexts,
            ai_text=inputQuery,
            ai_percentage=ai_percentage,
            is_ai_text=is_ai_text
        )
    except Exception as e:
        return "Error occurred: " + str(e)


app.run()
