from mycroft import MycroftSkill, intent_file_handler


class Dictat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('dictat.intent')
    def handle_dictat(self, message):
        self.speak_dialog('dictat')


def create_skill():
    return Dictat()

