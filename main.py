import scientist as sc, sys


scientist = sc.DataScientist(None)
replace = [["\n", " "]]
threads = []
#t = scientist.insert(open("./text.txt", mode='r').read(), "word", replacer=replace, startAsThread=True)
#threads.append(t)
t = scientist.insert(open("./eng.txt", mode='r').read(), "word", replacer=replace)
threads.append(t)
#scientist.waitFinish(threads)
words = scientist.get("word")
word_count = 0
same_words = []
for word in words.copy():
    word = scientist.get(f"word.{word}.self")
    if word is None: continue
    word_count += word.count
    if word.count > 1: same_words.append(word.name)

print("count of different words", len(words))
print("count of words", word_count)
print("same words count", len(same_words))
print("same words", same_words)