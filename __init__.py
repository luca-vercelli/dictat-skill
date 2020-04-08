from mycroft import MycroftSkill, intent_file_handler, intent_handler
from os import system
from adapt.intent import IntentBuilder
from mycroft.skills.context import adds_context, removes_context
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel

class Dictat(CommonPlaySkill):
    def __init__(self):
        CommonPlaySkill.__init__(self)
        self.dictating = False

    @intent_file_handler('dictat.start.intent')
    @adds_context('DoingDictation')
    def start_dictation(self, message):
        self.dictating = True
        self.speak_dialog('dictat.start')

    @intent_file_handler('dictat.stop.intent')
    @removes_context('DoingDictation')
    def stop_dictation(self, message):
        if self.dictating:
            self.dictating = False
            self.speak_dialog('dictat.stop')
        else:
            self.log.info("Should speak: I'm not doing any dictatation") #TODO

    @intent_handler(IntentBuilder('dictat').require('DoingDictation'))
    def handle_free_text(self, message):
        # should check for dictat.stop.intent
        # self.type_text(message)
        self.log.info("Dictating: " + str(message))

    def stop(self):
        if self.dictating:
            self.dictating = False
            self.speak_dialog('dictat.stop')

    def type_text(text):
        os.system("xvkbd", "--text", text)

    def CPS_match_query_phrase(self, phrase):
        if self.dictating:
            # shouldnt be here 
            return(phrase, CPSMatchLevel.EXACT)
        elif phrase == "dictate" or phrase == "dictating": #BLEAH
            return(phrase, CPSMatchLevel.EXACT)
        else:
            return None

    def CPS_start(self, phrase, data):
        if self.dictating:
            # shouldnt be here 
            self.type_text(phrase)
        else:
            self.dictating = True
            self.set_context('DoingDictation')

def create_skill():
    return Dictat()

