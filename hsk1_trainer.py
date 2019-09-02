AUDIO_DIR = "./HSK1_dict_audio/"
DICT_FILE = "HSK1_dict.txt"
PLAY_BEFORE_TRUE_ANS = False
NUM_WORDS_TO_TRAIN = -1
#NOT_PENALIZE_AFTER_REPEAT_AUDIO = True
SHOW_ZI_MEANING = False

import pygame
import os
import random

class Word(object):
    def __init__(self, record):
        fields = record.strip(" ;\n\t").split("\t")
        assert len(fields) in [3, 6], "ERROR: wrong dict record: \"" + record + "\""
        
        self.pinyin = fields[0]
        self.characters = fields[1]
        if len(fields) == 3:
            self.meaning = fields[2]
        elif len(fields) == 6:
            self.tries_all = fields[2]
            self.last_try = fields[3]
            self.errors_all = fields[4]
            self.meaning = fields[5]
        
        audiofile = self.pinyin.replace(" ", "_") + "___" + self.characters + ".mp3"
        if os.path.exists(AUDIO_DIR + audiofile):
            self.audio_path = AUDIO_DIR + audiofile
        else:
            self.audio_path = None
        
        self.errors = 0
        self.errors_words = []
        
    def play(self):
        if self.audio_path is not None:
            pygame.mixer.init()
            pygame.mixer.music.load(self.audio_path)
            pygame.mixer.music.play()


with open(DICT_FILE, "r", encoding="UTF-8") as f:
    records = [record for record in f.read().strip(" ;\n\t").split("\n")]
dict_words = [Word(record) for record in records]

if NUM_WORDS_TO_TRAIN != -1:
    words = [dict_words.pop(random.randint(0, len(words) - 1)) for _ in range(NUM_WORDS_TO_TRAIN)]
else:
    words, dict_words = dict_words, []


def print_statictics():
    global remain_words, right_ans, wrong_ans, right_ans_1_try
    os.system("cls")
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

# def set_mode_parameters():
# def clear_screen():

def training(words, training_mode=0):
    os.system("cls")
    print("press Enter to start...")
    input()

    # counters
    num_words_error = 0
    num_words_right = 0
    num_words_done = 0
    num_words_remain = len(words)
    
    words_done = []
    words_remain = words
    
    user_input = ""
    
    # main training loop
    while True:
        print_statictics()
        word_index = random.randint(num_words_remain)
        word = words[word_index]
        
        # one word training loop
        while True:                                     
            

        #    if after_repeat_audio:
        #        go_next = True
            if PLAY_BEFORE_TRUE_ANS:
                word.play()
            if SHOW_ZI_MEANING:
                print(word.meaning)
            print(word.characters)
            user_input = input()    
            word.play()
            if user_input == word.pinyin:
                print("Correct!")
                if go_next == True:
                    right_ans += 1
                    if word.wrong_ans == 0:
                        right_ans_1_try += 1
                    done_words.append(words.pop(word_index))
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
                word.wrong_ans += 1
                if inp != "":
                    word.wrong_ans_words.append(inp)
                print("You are wrong! Correct is: " + word.pinyin)
                go_next = False        
            if not SHOW_ZI_MEANING:
                print(word.meaning)
            
            input()
        if (user_input == "!exit") or (num_words_remain == 0):
            break
    #end of main training loop
    
    return words_done + words_remain

done_words.sort(key=lambda word : -word.wrong_ans)
with open ("game_statistics.txt", "w", encoding="UTF-8") as f:
    f.write("word\twrong_answers\terrors\n")
    for word in done_words:
        f.write(word.pinyin + "\t" + word.characters + "\t" + str(word.wrong_ans) + "\t" + str(word.wrong_ans_words) + "\t" + word.meaning + "\n")