AUDIO_FOLDER = "./HSK1_words/"
DICT_FILE = "HSK1_dict.txt"
PLAY_BEFORE_TRUE_ANS = False
NUMBER_OF_WORDS = -1
#NOT_PENALIZE_AFTER_REPEAT_AUDIO = True
SHOW_ZI_MEANING = False

from pygame import mixer # Load the required library
from os import system
import random

def print_statictics():
    global remain_words, right_ans, wrong_ans, right_ans_1_try
    system("cls")
    if right_ans != 0:
        if wrong_ans == 0:
            percents = 100
        else:
            percents = int(100*(right_ans_1_try) / (right_ans + wrong_ans))
    else:
        percents = 0
    print("Right:", right_ans, "Wrong:", wrong_ans,
          "Percents:", percents,
          "Correct:", right_ans_1_try,
          "Points:", right_ans_1_try * 100 + (right_ans-right_ans_1_try) * 20 - wrong_ans * 50,
          "\tRemain:", remain_words)
    print()

class Word:
    def __init__(self, pinyin, characters, meaning, audio_filename):
        self.pinyin = pinyin
        self.characters = characters
        self.meaning = meaning
        self.audio_path = AUDIO_FOLDER + audio_filename
        
        self.wrong_ans = 0
        self.wrong_ans_words = []
    
    def play(self):
        mixer.init()
        mixer.music.load(self.audio_path)
        mixer.music.play()

with open(DICT_FILE,"r", encoding="UTF-8") as f:
    dict_file = [w.split("\t") for w in f.read().strip(" \n\t\"\'").split("\n")]
words = []
for word in dict_file:
    words.append(Word(word[0], word[1], word[2], word[0].replace(" ", "_") + "___" + word[1] + ".mp3"))

if NUMBER_OF_WORDS != -1:
    words_rnd = []
    for i in range(NUMBER_OF_WORDS):
        words_rnd.append(words.pop(random.randint(0, len(words) - 1)))
    words = words_rnd


system("cls")
print("press Enter to start...")
input()

remain_words = len(words)
right_ans = 0
wrong_ans = 0
right_ans_1_try = 0
done_words = []

inp = ""
go_next = True
#after_repeat_audio = False
while (inp != "!exit") and (remain_words > 0):
    print_statictics()
    if go_next:
        word_num = random.randint(0,remain_words-1)
        curr_word = words[word_num]
#    if after_repeat_audio:
#        go_next = True
    if PLAY_BEFORE_TRUE_ANS:
        curr_word.play()
    if SHOW_ZI_MEANING:
        print(curr_word.meaning)
    print(curr_word.characters)
    inp = input()    
    curr_word.play()
    if inp == curr_word.pinyin:
        print("Correct!")
        if go_next == True:
            right_ans += 1
            if curr_word.wrong_ans == 0:
                right_ans_1_try += 1
            done_words.append(words.pop(word_num))
            remain_words -= 1
        else:
            go_next = True
    elif inp == "!": # word for repeat audio
        go_next = False
#        after_repeat_audio = NOT_PENALIZE_AFTER_REPEAT_AUDIO
        continue
    elif (inp == "!next") or (inp == "!stop"):
        go_next = True
    else:
        wrong_ans += 1
        curr_word.wrong_ans += 1
        if inp != "":
            curr_word.wrong_ans_words.append(inp)
        print("You are wrong! Correct is: " + curr_word.pinyin)
        go_next = False        
    if not SHOW_ZI_MEANING:
        print(curr_word.meaning)
    input()

done_words.sort(key=lambda word : -word.wrong_ans)
with open ("game_statistics.txt", "w", encoding="UTF-8") as f:
    f.write("word\twrong_answers\terrors\n")
    for word in done_words:
        f.write(word.pinyin + "\t" + word.characters + "\t" + str(word.wrong_ans) + "\t" + str(word.wrong_ans_words) + "\t" + word.meaning + "\n")