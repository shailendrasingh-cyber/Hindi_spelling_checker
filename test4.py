import streamlit as st

# Function to load the corpus
def load_corpus():
    with open('hindi_corpus.txt', encoding='utf-8') as file:
        corpus = [word.strip() for word in file]
    return corpus

# Function to calculate Levenshtein Distance
def levenshtein_distance(s, t):
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
                                  dist[row - 1][col - 1] + cost) # substitution

    return dist[row][col]

# Function to get correct word
def get_correct_word(word, corpus):
    min_dis = 100
    correct_word = ""
    for s in corpus:
        cur_dis = levenshtein_distance(s, word)
        if min_dis > cur_dis:
            min_dis = cur_dis
            correct_word = s
    return correct_word

# Function to process input text
def process_input_text(input_text, corpus):
    corrected_text = []
    lines = input_text.split('\n')
    for line_num, line in enumerate(lines, start=1):
        words = line.strip().split()
        corrected_line = []
        for word_num, word in enumerate(words, start=1):
            if word not in corpus:
                corrected = get_correct_word(word, corpus)
                corrected_line.append(f"At Line: {line_num} Word No. {word_num}: {word} -> {corrected}")
            else:
                corrected_line.append(word)
        corrected_text.append(' '.join(corrected_line))
    return '\n'.join(corrected_text)

# Streamlit App
def main():
    st.title("Spell Checker")

    # Upload input text file
    uploaded_file = st.file_uploader("Upload a text file", type=['txt'])
    if uploaded_file is not None:
        input_text = uploaded_file.getvalue().decode("utf-8")
        
        # Load corpus
        corpus = load_corpus()

        # Process input text
        corrected_text = process_input_text(input_text, corpus)

        # Display corrected text
        st.subheader("Corrected Text")
        st.text_area("Corrected Text", value=corrected_text, height=300)

        # Offer download option for corrected text
        st.subheader("Download Corrected Text")
        st.download_button(
            label="Download Corrected Text",
            data=corrected_text.encode('utf-8'),
            file_name="corrected_text.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
