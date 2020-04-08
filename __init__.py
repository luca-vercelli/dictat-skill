from mycroft import MycroftSkill, intent_file_handler, intent_handler
from os import system
from adapt.intent import IntentBuilder
from mycroft.skills.context import adds_context, removes_context
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel


#
# Conflicting intents: Timer Skill "inizia a parlare" / "inizia un dettato"
#

class Dictat(CommonPlaySkill):
    def __init__(self):
        CommonPlaySkill.__init__(self)
        self.dictating = False

    @intent_file_handler('dictat.start.intent')
    @adds_context('DoingDictation')
    def start_dictation(self, message):
        self.log.info("Here start_dictation")
        self.dictating = True
        self.speak_dialog('dictat.start')
        
        for (name, _) in self.intent_service:
            self.log.info("name=" + str(name))

    @intent_file_handler('dictat.stop.intent')
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
        # TODO self.type_text(message)
        self.log.info("Dictating: " + str(message.data["utterance"]))

    def stop(self):
        self.log.info("Here stop()")
        if self.dictating:
            self.dictating = False
            self.speak_dialog('dictat.stop')

    def type_text(text):
        os.system("xvkbd", "--text", text)

    def CPS_match_query_phrase(self, phrase):
        self.log.info("Here CPS_match_query_phrase")
        if self.dictating:
            # shouldnt be here 
            return(phrase, CPSMatchLevel.EXACT)
        elif phrase == "dictate" or phrase == "dictating": #BLEAH
            return(phrase, CPSMatchLevel.EXACT)
        else:
            return None

    def CPS_start(self, phrase, data):
        self.log.info("Here CPS_start")
        if self.dictating:
            # shouldnt be here 
            # TODO self.type_text(phrase)
            self.log.info("Dictating: " + str(phrase))
        else:
            self.dictating = True
            self.set_context('DoingDictation')

def create_skill():
    return Dictat()

