from mycroft import MycroftSkill, intent_file_handler


class Dictat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.dictating = False

    @intent_file_handler('dictat.start.intent')
    def start_dictat(self, message):
        self.dictating = True
        self.speak_dialog('dictat.start')

    @intent_file_handler('dictat.stop.intent')
    def stop_dictat(self, message):
        self.dictating = False
        self.speak_dialog('dictat.stop')

    def stop(self):
        self.stop_dictat()

def create_skill():
    return Dictat()

