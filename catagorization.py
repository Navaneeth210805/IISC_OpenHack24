import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

# Sample prompt
prompt = """
    Narendra Modi: A Charismatic Leader and the Current Prime Minister of India

Narendra Damodardas Modi was born on September 17, 1950, in Vadnagar, Gujarat, India. His early life was marked by humble beginnings as he hailed from a family of grocers. Modi's political journey began in the early 1970s when he joined the Rashtriya Swayamsevak Sangh (RSS), a Hindu nationalist organization. Through his association with the RSS, Modi developed a strong commitment to Hindu values and ideology.

In 1987, Modi became a member of the Bharatiya Janata Party (BJP), India's leading right-wing political party. He quickly rose through the ranks, holding various positions within the party and gaining recognition for his organizational skills and charisma. In 2001, Modi was appointed as the Chief Minister of Gujarat, a state in western India. His tenure as Chief Minister was marked by economic growth and infrastructure development, which earned him praise from some quarters.

However, Modi's reputation was tarnished by the 2002 Gujarat riots, a communal conflict that resulted in the deaths of over 1,000 people, mostly Muslims. Modi was accused of failing to prevent the violence and even of tacitly supporting it. Despite these allegations, Modi remained popular in Gujarat and was re-elected as Chief Minister in 2007 and 2012.

In 2014, Modi led the BJP to a landslide victory in the general elections, becoming the 15th Prime Minister of India. His campaign focused on economic development, national security, and Hindu nationalism. Modi's victory was seen as a watershed moment in Indian politics, marking the end of the Congress Party's dominance and the rise of the BJP as the country's leading political force.

As Prime Minister, Modi has pursued a number of ambitious policies, including economic reforms, infrastructure development, and social welfare programs. He has also taken a tough stance on national security, cracking down on terrorism and promoting India's military capabilities. Modi's tenure has been marked by both successes and challenges, with his popularity fluctuating over the years.

Narendra Modi remains a controversial figure, admired by some and criticized by others. His supporters see him as a strong and decisive leader who has transformed India into a global power. His critics argue that he is authoritarian, divisive, and has undermined India's democratic institutions. Regardless of one's opinion of Modi, there is no doubt that he is one of the most influential and consequential figures in Indian politics today.
"""

# Tokenization and stopword removal
tokens = word_tokenize(prompt)
stop_words = set(stopwords.words('english'))
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

# Part-of-speech tagging
pos_tags = nltk.pos_tag(filtered_tokens)

# Selecting keywords
keywords = []
for token, pos in pos_tags:
    if pos.startswith('NN'):
        keywords.append(token)

# Final selection
print(len(keywords))
print("Keywords:", keywords)

freq = nltk.FreqDist(keywords)
print(freq.most_common(10))

keywords = []
for token, pos in pos_tags:
    if pos == 'NN':
        keywords.append(token)

# Final selection
print(len(keywords))
print("Keywords:", keywords)

freq = nltk.FreqDist(keywords)
print(freq.most_common(10))

nlp = spacy.load("en_core_web_lg")
doc = nlp(prompt)
named_entities = [ent.text for ent in doc.ents]

print(len(named_entities))
print(named_entities)

