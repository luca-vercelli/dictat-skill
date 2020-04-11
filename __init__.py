from mycroft import MycroftSkill, intent_file_handler, intent_handler
from os import system
from adapt.intent import IntentBuilder
from mycroft.skills.context import adds_context, removes_context
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
import os


#
# Conflicting intents: Timer Skill "inizia a parlare" / "inizia un dettato"
#

class Dictat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.dictating = False

    #@intent_file_handler('dictat.start.intent')
    @intent_handler(IntentBuilder('StartDictationIntent').require('StartKeyword').require('DictationKeyword'))
    @adds_context('DoingDictation')
    def start_dictation(self, message):
        self.log.info("Here start_dictation")
        self.dictating = True
        self.speak_dialog('dictat.start', expect_response=True)
        
        for (name, _) in self.intent_service:
            self.log.info("name=" + str(name))

    #@intent_file_handler('dictat.stop.intent')
    @intent_handler(IntentBuilder('StopDictationIntent').require('StopKeyword').require('DictationKeyword'))
    @removes_context('DoingDictation')
    def stop_dictation(self, message):
        self.log.info("Here stop_dictation")
        if self.dictating:
            self.dictating = False
            self.speak_dialog('dictat.stop')
        else:
            self.speak_dialog('dictat.none')

    @intent_handler(IntentBuilder('dictat').require('DoingDictation'))
    def handle_free_text(self, message):
        self.log.info("Here handle_free_text")
        # should check for dictat.stop.intent
        self.type_text(message)
        self.log.info("Dictating: " + str(message.data["utterance"]))

    def stop(self):
        self.log.info("Here stop()")
        if self.dictating:
            self.dictating = False
            self.speak_dialog('dictat.stop')

    def converse(self, utterances, lang="en-us"):
        # see https://github.com/JarbasAl/skill-dictation/blob/master/__init__.py
        self.log.info("Here converse() utterances=" + str(utterances) + " lang=" + str(lang))
        if self.dictating:
            if utterances:
                # keep intents working without dictation keyword being needed
                self.set_context('DoingDictation')
                if self.voc_matches('StopKeyword'):
                    return False
                    # the stop_dictation() or stop() handlers should be triggered
                self.log.info("Dictating (via converse): " + utterances[0])
                self.type_text(utterances[0])
            self.speak("", expect_response=True)
            return True

    def type_text(self, text):
        if text:
            os.system('xte "' + str(text) + '"')

# if this were a CommonPlaySkill:
#
#    def CPS_match_query_phrase(self, phrase):
#        self.log.info("Here CPS_match_query_phrase")
#        if self.dictating:
#            # shouldnt be here 
#            return(phrase, CPSMatchLevel.EXACT)
#        elif phrase == "dictate" or phrase == "dictating": #BLEAH
#            return(phrase, CPSMatchLevel.EXACT)
#        else:
#            return None
#
#    def CPS_start(self, phrase, data):
#        self.log.info("Here CPS_start")
#        if self.dictating:
#            self.type_text(phrase)
#            self.log.info("Dictating: " + str(phrase))
#        else:
#            self.dictating = True
#            self.set_context('DoingDictation')

def create_skill():
    return Dictat()

