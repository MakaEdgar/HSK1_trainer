AUDIO_DIR = "./dicts/HSK1_dict_audio/"
DICT_FILE = "./dicts/HSK1_dict.txt"
PLAY_BEFORE_TRUE_ANS = False
NUM_WORDS_TO_TRAIN = None
#NOT_PENALIZE_AFTER_REPEAT_AUDIO = True
SHOW_ZI_MEANING = False


import os
import time
import copy
import random
import pygame
from collections import defaultdict

class Word(object):
    def __init__(self, record):
        fields = record.strip(" ;\n\t").split("\t")
        assert len(fields) in [3, 6], "ERROR: wrong dict record: \"" + record + "\""
        
        self.word = fields[0]
		self.translation = fields[1]
        if len(fields) == 2:
			self.last_try_date   = None # TODO: ADD DATE
			self.quality_percent = 0
            self.runs_all_time   = 0
            self.errors_all_time = 0
			self.error_words     = defaultdict(0)
        elif len(fields) == 6:
            self.last_try_date   = fields[2]
			self.quality_percent = fields[3]
            self.runs_all_time   = fields[4]
            self.errors_all_time = fields[5]
			self.error_words     = HHHHHHHHHHHHHHHHHHHHHHHHHHHH
        
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
		return [self.pinyin, self.characters, self.last_try_date, str(self.quality_percent) + "%",
				self.runs_all_time, self.errors_all_time, self.meaning]
				
	@property
	def fields_names(self):
		return ["pinyin", "characters", "last_try_date", "quality_percent",
				"runs_all_time", "errors_all_time", "meaning"]

	def get_record(self):
		return self.fields.join("\t")

class Word(object):
    def __init__(self, record):
        fields = record.strip(" ;\n\t").split("\t")
        assert len(fields) in [3, 7], "ERROR: wrong dict record: \"" + record + "\""
        
        self.pinyin = fields[0]
        self.characters = fields[1]
        if len(fields) == 3:
			self.last_try_date   = None # TODO: ADD DATE
			self.quality_percent = 0
            self.runs_all_time   = 0
            self.errors_all_time = 0
			self.meaning         = fields[2]
        elif len(fields) == 7:
            self.last_try_date   = fields[2]
			self.quality_percent = fields[3]
            self.runs_all_time   = fields[4]
            self.errors_all_time = fields[5]
            self.meaning         = fields[6]
        
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


	@property
	def fields(self):
		return [self.pinyin, self.characters, self.last_try_date, self.quality_percent,
				self.runs_all_time, self.errors_all_time, self.meaning]
				
	@property
	def fields_names(self):
		return ["pinyin", "characters", "last_try_date", "quality_percent",
				"runs_all_time", "errors_all_time", "meaning"]

	def get_record(self):
		return self.fields.join("\t")



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

def train_word(self, word, training_mode=0):
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
		# end of word loop
 


def train(words, **kwargs):
    os.system("cls")
    print("press Enter to start...")
    input()

    # counters
    num_words_error = 0
    num_words_right = 0
    num_words_done = 0
    num_words_removed = 0	
    num_words_remain = len(words)
    
    words_remain, words_done, words_removed  = words, [], []
     
    # main training loop
    while num_words_remain > 0:
        print_statictics()
        word_index = random.randint(num_words_remain) 
		train_word_result = train_word(words[word_index], **kwargs)
		
		if train_word_result["status"] == "done":
			num_words_right  += 1
			num_words_done   += 1
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
        
    #end of main training loop
	train_result = {
		"words_done" : words_done,
		"words_remain" : words_remain,
		"words_removed" : words_removed,		
		"num_words_error" : num_words_error,
		"num_words_right" : num_words_right,
		"num_words_removed" : num_words_removed,
	}
    return train_result

def main():
	with open(DICT_FILE, "r", encoding="UTF-8") as f:
		dict_records = [record for record in f.read().strip(" ;\n\t").split("\n") if (record.strip()[0] != "#")]
	dict_words = [Word(record) for record in dict_records]

	if NUM_WORDS_TO_TRAIN is not None:
		words = random.sample(dict_words, NUM_WORDS_TO_TRAIN)
	else:
		words = dict_words 
	
	# main dictionary training
	train_result = train(words)
	dict_words.sort(key=lambda word:(word.quality_percent, -word.errors_all_time))
	with open(DICT_FILE, "w", encoding="UTF-8") as f:
		f.write("word\twrong_answers\terrors\n")
		for word in done_words:
			f.write(word.get_record() + "\n")
			
# run this script
main()