# VocabLevel
This is a simple but efficient method to approximately calculate the users' vocabulary level. 

## How it works?
It is based on the subtitles of the Friends series, although it can be easily extended to other corpuses. After some simple pre-processing steps, the unique words are sorted according to their frequencies. Then, a binary search approach is adopted to find the vocabulary level of the users. This approach is based on the following simple rules:
If the user knows the meaning of a word w, it is likely that she/he also knows the meaning of more frequent words.

Although these rules are not completely true, they are approximately acceptable. Anyway, these simple rules help us to obtain a very efficient method which only needs ```log_2(n)```, so for example with a list of 10000 words you would need to answer about 13 questions.
