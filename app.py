from flask import Flask, request, render_template
import re
import math
import string

app = Flask("__name__")

# Define thresholds for detecting AI-generated text and plagiarism
ai_generated_threshold = 0.8
ai_detection_threshold = 10  # AI Text detection threshold
plagiarism_threshold = 10  # Plagiarism detection threshold


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
    return render_template('index.html')


@app.route("/", methods=['POST'])
def detect_plagiarism_and_ai_text():
    try:
        inputQuery = request.form['query']
        lowercaseQuery = inputQuery.lower()

        # Replace punctuation by space and split
        queryWordList = re.sub("[^\w]", " ", lowercaseQuery).split()

        universalSetOfUniqueWords = list(set(queryWordList))

        fd = open("database1.txt", "r")
        database1 = fd.read().lower()

        # Replace punctuation by space and split
        databaseWordList = re.sub("[^\w]", " ", database1).split()

        universalSetOfUniqueWords += list(set(databaseWordList) - set(universalSetOfUniqueWords))

        queryTF = []
        databaseTF = []

        for word in universalSetOfUniqueWords:
            queryTfCounter = queryWordList.count(word)
            databaseTfCounter = databaseWordList.count(word)
            queryTF.append(queryTfCounter)
            databaseTF.append(databaseTfCounter)

        dotProduct = sum(queryTF[i] * databaseTF[i] for i in range(len(queryTF)))

        queryVectorMagnitude = math.sqrt(sum(tf ** 2 for tf in queryTF))
        databaseVectorMagnitude = math.sqrt(sum(tf ** 2 for tf in databaseTF))

        matchPercentage = (dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

        # Identify plagiarized texts
        plagiarizedTexts = list(set(queryWordList) & set(databaseWordList))

        output = ""
        plagiarism_status = ""

        if matchPercentage >= plagiarism_threshold:
            plagiarism_status = "Plagiarism Detected"
        elif matchPercentage > 0:
            plagiarism_status = "Limited Plagiarism"

        ai_percentage = calculate_ai_percentage(inputQuery)
        is_ai_text = ai_percentage > ai_generated_threshold
        ai_text_detected = ai_percentage > ai_detection_threshold

        return render_template(
            'index.html',
            query=inputQuery,
            percentage=matchPercentage,
            output=output,
            plagiarized_texts=plagiarizedTexts,
            ai_text=inputQuery,
            ai_percentage=ai_percentage,
            is_ai_text=is_ai_text,
            ai_text_detected=ai_text_detected,
            plagiarism_status=plagiarism_status
        )
    except Exception as e:
        return "Error occurred: " + str(e)


if __name__ == "__main__":
    app.run()
