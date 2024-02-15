import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

# Sample prompt
prompt = "Who is Virat Kohli"

# Tokenization and stopword removal
tokens = word_tokenize(prompt)
stop_words = set(stopwords.words('english'))
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

# Part-of-speech tagging
pos_tags = nltk.pos_tag(filtered_tokens)

# Named entity recognition
nlp = spacy.load("en_core_web_lg")
doc = nlp(prompt)
named_entities = [ent.text for ent in doc.ents]

print(len(named_entities))
print(named_entities)

# Selecting keywords
keywords = []
for token, pos in pos_tags:
    if (pos.startswith('NN') or pos.startswith('CD') or token in named_entities) and token not in keywords:
        keywords.append(token)

# Final selection
print(len(keywords))
print("Keywords:", keywords)

