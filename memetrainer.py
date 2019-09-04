import os
import time
import copy
import random
import pygame
from collections import defaultdict
import ast
import shutil 

import datetime
DATE = datetime.datetime.now().strftime("%d.%m.%Y")

USER_NAME = "Edgar"
USER_DIR = "./users/" + USER_NAME + "/"
if not os.path.exists(USER_DIR):
    os.mkdir(USER_DIR)
if not os.path.exists(USER_DIR + "dicts"):
    os.mkdir(USER_DIR + "dicts")

DICT_NAME = "HSK1"
if not os.path.exists(USER_DIR + "dicts/" + DICT_NAME + ".csv"):
    if os.path.exists("./dicts/" + DICT_NAME + ".txt"):
        shutil.copyfile("./dicts/" + DICT_NAME + ".txt", USER_DIR + "dicts/" + DICT_NAME + ".csv")
    elif os.path.exists("./dicts/" + DICT_NAME + ".csv"):
        shutil.copyfile("./dicts/" + DICT_NAME + ".csv", USER_DIR + "dicts/" + DICT_NAME + ".csv")
    else:
        print("ERROR: dictionary \"" + DICT_NAME + ".txt\" or \"" + DICT_NAME + ".csv\" does not exist! Put it in \"dicts\" folder")
        exit(1)
DICT_FILE = USER_DIR + "dicts/" + DICT_NAME + ".csv"
AUDIO_DIR = "./dicts/" + DICT_NAME + "_audio/" #"./dicts/HSK1_dict_audio/"


PLAY_BEFORE_INPUT = False
REPEAT_IS_MISTAKE = False
SHOW_MEANING_BEFORE_INPUT = False
NUM_WORDS_TO_TRAIN = None


class Word(object):
    def __init__(self, record):
        fields = record.strip(" ;\n\t").split("\t")
        assert len(fields) in [2, 7], "ERROR(Word): wrong dict record: \"" + record + "\""
        
        self.word = fields[0]
        self.translation = fields[1]
        if len(fields) == 2:
            self.last_try_date   = DATE
            self.quality_percent = int(0)
            self.runs_all_time   = int(0)
            self.errors_all_time = int(0)
            self.error_words     = defaultdict(int)
        elif len(fields) == 7:
            self.last_try_date   = fields[2]
            self.quality_percent = int(fields[3][:-1])
            self.runs_all_time   = int(fields[4])
            self.errors_all_time = int(fields[5])
            self.error_words     = defaultdict(int, ast.literal_eval(fields[6]))
        
        audiofile = self.word.replace(" ", "_").replace(",", "_").replace(".", "_") + ".mp3"
        if (AUDIO_DIR is not None) and (os.path.exists(AUDIO_DIR + audiofile)):
            self.audio_path = AUDIO_DIR + audiofile
        else:
            self.audio_path = None
        
        self.errors_curr = 0
        
    def play(self):
        if self.audio_path is not None:
            pygame.mixer.init()
            pygame.mixer.music.load(self.audio_path)
            pygame.mixer.music.play()

    @property
    def fields(self):
        return [self.word, self.translation, str(self.last_try_date), str(self.quality_percent) + "%",
                str(self.runs_all_time), str(self.errors_all_time),  
                str(sorted(dict(self.error_words).items(), key=lambda v : -v[1]))]
                
    @staticmethod 
    def get_fields_names():
        return ["word", "translation", "last_try_date", "quality_percent",
                "runs_all_time", "errors_all_time", "error_words"]

    def get_record(self):
        return self.fields.join("\t")

class WordChinese(Word):
    def __init__(self, record):
        fields = record.strip(" ;\n\t").split("\t")
        assert len(fields) in [3, 8], "ERROR: wrong dict record: \"" + record + "\""
        
        self.pinyin = fields[0]
        self.characters = fields[1]
        if len(fields) == 3:
            self.last_try_date   = DATE
            self.quality_percent = int(0)
            self.runs_all_time   = int(0)
            self.errors_all_time = int(0)
            self.error_words     = defaultdict(int)
            self.meaning         = fields[2]
        elif len(fields) == 8:
            self.last_try_date   = fields[2]
            self.quality_percent = int(fields[3][:-1])
            self.runs_all_time   = int(fields[4])
            self.errors_all_time = int(fields[5])
            self.error_words     = defaultdict(int, ast.literal_eval(fields[6]))
            self.meaning         = fields[7]
        
        audiofile = self.pinyin.replace(" ", "_") + "___" + self.characters + ".mp3"
        if os.path.exists(AUDIO_DIR + audiofile):
            self.audio_path = AUDIO_DIR + audiofile
        else:
            self.audio_path = None
        
        self.errors_curr = 0
        
    def play(self):
        if self.audio_path is not None:
            pygame.mixer.init()
            pygame.mixer.music.load(self.audio_path)
            pygame.mixer.music.play()


    @property
    def fields(self):
        return [self.pinyin, self.characters, str(self.last_try_date), str(self.quality_percent) + "%",
                str(self.runs_all_time), str(self.errors_all_time),  
                str(dict(sorted(dict(self.error_words).items(), key=lambda v : -v[1]))), self.meaning]
                
    @staticmethod 
    def get_fields_names():
        return ["pinyin", "characters", "last_try_date", "quality_percent",
                "runs_all_time", "errors_all_time", "error_words", "meaning"]

    def get_record(self):
        return "\t".join(self.fields)

def clear_screen():
    os.system("cls")

def do_nothing():
    pass

def train_word(word):
    status = ""
    user_mistook = False

    while status == "":                                     
        word.play() if PLAY_BEFORE_INPUT else do_nothing()
        print(word.meaning) if SHOW_MEANING_BEFORE_INPUT else do_nothing()
        print(word.characters)
        user_input = input()    
        word.play()
        
        if user_input == word.pinyin:
            print("Correct!")
            status = "done" if not user_mistook else "error"
        elif user_input == "!repeat": # word for repeat audio 
            user_mistook = user_mistook or REPEAT_IS_MISTAKE
            continue
        elif user_input in ["!next", "!remove", "!exit"]:
            status = user_input[1:]
            break
        else:
            print("You are wrong! Correct is: " + word.pinyin)
            user_mistook = True
            word.errors_curr += 1
            if user_input != "":
                word.error_words[user_input] += 1
            
        print(word.meaning) if not SHOW_MEANING_BEFORE_INPUT else do_nothing()
        input()
        clear_screen()
    # end of word loop
    
    # update word statistics
    word.runs_all_time += 1
    if status == "done": 
        word.last_try_date = DATE
    else:
        word.errors_all_time += 1
        
    if word.errors_curr == 0:
        word.quality_percent = (100 * (round((word.runs_all_time-word.errors_all_time) * word.quality_percent) + 1)) // (word.runs_all_time)
    else:
        word.quality_percent = (100 * (round((word.runs_all_time-word.errors_all_time) * word.quality_percent)    )) // (word.runs_all_time)
    
    
    train_word_result = {
        "status" : status,
    }
    return train_word_result

def train(words):
    clear_screen()
    print("press Enter to start...")
    input()

    # counters
    num_words_run = 0
    num_words_done = 0
    num_words_error = 0
    num_words_right = 0
    num_words_removed = 0
    num_words_remembered = 0
    num_words_remain = len(words)
    quality_percent = 0
    points = 0
    
    words_remain, words_done, words_removed  = words, [], []
    
    start_time = datetime.datetime.now()
    # main training loop starts
    while num_words_remain > 0:
    # print statistics
        clear_screen() 
        print("Done:", num_words_done, 
              "Errors:", num_words_error,
              "Quality:", str(quality_percent)+"%",
              "Correct:", num_words_remembered,
              "Points:", points,
              "\tRemain:", num_words_remain, "\n")

     # train one word until it's will be written correctly
        word_index = random.randint(0, num_words_remain-1)
        word = words[word_index]
        num_words_run += 1 if (word.errors_curr == 0) else 0
        train_word_result = train_word(word)


     # update counters
        if train_word_result["status"] == "done":
            num_words_right  += 1
            num_words_done   += 1
            num_words_remembered += 1 if (words[word_index].errors_curr == 0) else 0
            num_words_remain -= 1
            words_done.append(words_remain.pop(word_index))
        elif train_word_result["status"] == "error":
            num_words_right += 1
            num_words_error += 1
        elif train_word_result["status"] == "remove":
            num_words_remain  -= 1
            num_words_removed += 1
            words_removed.append(words_remain.pop(word_index))
        elif train_word_result["status"] == "next":
            pass
        elif (train_word_result["status"] == "exit"):
            break
        else:
            assert False, "no match for train_word_result[\"status\"]=\"" + train_word_result["status"] + "\""
            
        # update statistics
        points = (80 * num_words_remembered + 20 * num_words_done - 50 * num_words_error) #-sum([word.errors_curr for word in words])
        quality_percent = 0 if (num_words_done == 0) else (100 * num_words_remembered) // num_words_run
    #end of main training loop
    
    end_time = datetime.datetime.now()
    hours = str((end_time - start_time).seconds // 3600) + "h"
    mins = str(((end_time - start_time).seconds % 3600 + 59) // 60) + "m"
    
    train_result = {
        "num_words_done" : num_words_done,
        "num_words_error" : num_words_error,
        "num_words_right" : num_words_right,
        "num_words_removed" : num_words_removed,
        "num_words_remembered" : num_words_remembered,
        "quality_percent" : quality_percent,
        "points" : points,
        "words_done" : words_done,
        "words_remain" : words_remain,
        "words_removed" : words_removed,
        "time" : (hours + mins) if (hours != "0h") else mins
    }
    
    return train_result

def main():
    DICT_WORD_CLASS = WordChinese
# load words from dictionary
#    try: 
    with open(DICT_FILE, "r", encoding="UTF-8") as f:
        dict_records = [record for record in f.read().strip(" ;\n\t").split("\n") if (record.strip()[0] != "#")]
    dict_words = [DICT_WORD_CLASS(record) for record in dict_records]
#    except:
#        print("Cannot open dictionary \"" + DICT_FILE + "\"")
#        exit(1)

    if NUM_WORDS_TO_TRAIN is not None:
        words = random.sample(dict_words, NUM_WORDS_TO_TRAIN)
    else:
        words = [word for word in dict_words]
    
# train words
    train_result = train(words)
    
# update dictionary after training
    dict_words.sort(key=lambda word:(word.quality_percent, -word.runs_all_time))
    with open(DICT_FILE, "w", encoding="UTF-8") as f:
        f.write("# " + "\t".join(DICT_WORD_CLASS.get_fields_names()) + "\n")
        for word in dict_words:
            f.write(word.get_record() + "\n")

# add training to history
    train_stats = [DATE, 
                  DICT_FILE[DICT_FILE.rfind("/")+1 : DICT_FILE.rfind(".")],
                  str(train_result["num_words_done"]) + "/" + str(len(dict_words)),
                  str(train_result["points"]),
                  str(train_result["quality_percent"]) + "%",
                  str(train_result["num_words_remembered"]),
                  str(train_result["num_words_error"]),
                  train_result["time"],
                  "speed",
                  ]
    if not os.path.exists(USER_DIR + "history.csv"):
        with open(USER_DIR + "history.csv", "w", encoding="UTF-8") as f:
            f.write("date\tdict\twords\tpts\tqual\trem\terr\ttime\tspeed, sym/min\tcomment\n")
    with open(USER_DIR + "history.csv", "a", encoding="UTF-8") as f:
        f.write("\t".join(train_stats) + "\n")


# run this script
main()
