import streamlit as st
from PyPDF2 import PdfReader
import tempfile

corpus = []

def loadCorpus():
    # function to load the dictionary/corpus and store it in a global list
    with open('hindi_corpus.txt', encoding='utf-8') as file:
        for word in file:
            word = word.strip()
            corpus.append(word)

def getLevenshteinDistance(s, t):
    # Function to calculate Levenshtein Distance between two strings
    rows = len(s) + 1
    cols = len(t) + 1
    dist = [[0 for x in range(cols)] for x in range(rows)]

    for i in range(1, rows):
        dist[i][0] = i

    for i in range(1, cols):
        dist[0][i] = i

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row - 1][col] + 1,      # deletion
                                 dist[row][col - 1] + 1,      # insertion
                                 dist[row - 1][col - 1] + cost)  # substitution

    return dist[row][col]

def getCorrectWord(word):
    min_dis = 100
    correct_word = ""
    for s in corpus:
        cur_dis = getLevenshteinDistance(s, word)
        if min_dis > cur_dis:
            min_dis = cur_dis
            correct_word = s
    return correct_word, min_dis

def processPDF(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    corrected_text = []
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        corrected_page = []
        for line in text.split('\n'):
            words = line.strip().split()
            corrected_line = []
            for word in words:
                corrected_word, min_dis = getCorrectWord(word)
                if corrected_word != word:
                    corrected_line.append(f"{word} -> {corrected_word} (Distance: {min_dis})")
                else:
                    corrected_line.append(word)
            corrected_page.append(' '.join(corrected_line))
        corrected_text.append('\n'.join(corrected_page))
    return '\n\n'.join(corrected_text)

def main():
    st.title("PDF Text Correction App")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        st.write("File Uploaded!")
        corrected_text = processPDF(uploaded_file)
        st.text_area("Corrected Text", value=corrected_text, height=400)

        if st.button("Save as Text"):
            with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
                temp_file.write(corrected_text)
                st.write("Text saved as:", temp_file.name)

if __name__ == "__main__":
    loadCorpus()
    main()
