from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
try:
    from mycroft.skills.audioservice import AudioService
except:
    from mycroft.util import play_mp3
    AudioService = None
from bs4 import BeautifulSoup
import requests


__author__ = 'mmeyer'

LOGGER = getLogger(__name__)


DLF_URL = 'http://st01.dlf.de/dlf/01/128/mp3/stream.mp3'
DRADIO_URL = 'http://st02.dlf.de/dlf/02/128/mp3/stream.mp3'
NOVA_URL = 'http://st03.dlf.de/dlf/03/128/mp3/stream.mp3'


class DlfSkill(MycroftSkill):
    def __init__(self):
        super(DlfSkill, self).__init__(name="DlfSkill")
        self.audioservice = None

    def initialize(self):
        if AudioService:
            self.audioservice = AudioService(self.emitter)

        whatson_dlf_intent = IntentBuilder("WhatsonDlfIntent").\
                         require("WhatsonKeyword").\
                         require("DlfKeyword").build()
        self.register_intent(whatson_dlf_intent, self.handle_whatson_dlf_intent)

        whatson_dradio_intent = IntentBuilder("WhatsonDradioIntent").\
                                require("WhatsonKeyword").\
                                require("DradioKeyword").build()
        self.register_intent(whatson_dradio_intent,
                             self.handle_whatson_dradio_intent)

        whatson_nova_intent = IntentBuilder("WhatsonNovaIntent").\
                              require("WhatsonKeyword").\
                              require("NovaKeyword").build()
        self.register_intent(whatson_nova_intent,
                             self.handle_whatson_nova_intent)

        dlf_intent = IntentBuilder("DlfIntent").\
                     require("DlfKeyword").require("PlayKeyword").build()
        self.register_intent(dlf_intent, self.handle_dlf_intent)

        dradio_intent = IntentBuilder("DradioIntent").\
                        require("DradioKeyword").require("PlayKeyword").build()
        self.register_intent(dradio_intent, self.handle_dradio_intent)

        nova_intent = IntentBuilder("NovaIntent").\
                      require("NovaKeyword").require("PlayKeyword").build()
        self.register_intent(nova_intent, self.handle_nova_intent)

    def handle_whatson_dlf_intent(self, message):
        r = requests.get('http://www.deutschlandfunk.de')
        soup = BeautifulSoup(r.text)
        for el in soup.find_all(id='dlf-player-jetzt-im-radio'):
            for a_el in el.find_all('a'):
                self.speak_dialog("currently",
                                  { "station": "dlf", "title": a_el.string})

    def handle_whatson_dradio_intent(self, message):
        r = requests.get('http://www.deutschlandfunkkultur.de/')
        soup = BeautifulSoup(r.text)
        for el in soup.find_all(id='drk-player-jetzt-im-radio'):
            for a_el in el.find_all('a'):
                self.speak_dialog("currently",
                                  { "station": "dlf culture", "title": a_el.string})

    def handle_whatson_nova_intent(self, message):
        r = requests.get('https://www.deutschlandfunknova.de/actions/dradio/playlist/onair')
        j = r.json()
        
        self.speak_dialog("currently",
                          {"station": "dlf nova", "title": j['show']['title']})

    def handle_dlf_intent(self, message):
        if self.audioservice:
            self.audioservice.play(DLF_URL, message.data['utterance'])
        else:
            self.process = play_mp3(DLF_URL)

    def handle_dradio_intent(self, message):
        if self.audioservice:
            self.audioservice.play(DRADIO_URL, message.data['utterance'])
        else:
            self.process = play_mp3(DRADIO_URL)

    def handle_nova_intent(self, message):
        if self.audioservice:
            self.audioservice.play(NOVA_URL, message.data['utterance'])
        else:
            self.process = play_mp3(NOVA_URL)

    def stop(self):
        pass


def create_skill():
    return DlfSkill()
