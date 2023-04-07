# Sound playing library for weather station

import time
import threading
import vlc
import gtts

import state

class SoundPlayer():

    def __init__(self):
        SoundPlayer.instance = vlc.Instance('--aout=alsa')
        SoundPlayer.player = SoundPlayer.instance.media_player_new()
        SoundPlayer.bbChimes = SoundPlayer.instance.media_new('/home/njt/Documents/rpi/rpi-weather/big_ben_hour.mp3')
        SoundPlayer.bbHourly = SoundPlayer.instance.media_new('/home/njt/Documents/rpi/rpi-weather/big_ben_chimes.mp3')
        SoundPlayer.player.audio_set_volume(100)
        SoundPlayer.playSoundThread = None
        SoundPlayer.playTextThread = None

    def threadedPlayBBChimes(self, num):
       # Create and start-up the thread to do the sound playing
       SoundPlayer.playSoundThread = threading.Thread(
               target = self.playChimes,
               args=(num,),
               daemon=True)
       SoundPlayer.playSoundThread.start()

    def threadedPlayBBChimesWait(self):
        SoundPlayer.playSoundThread.join()

    def threadedPlayText(self, text):
       # Create and start-up the thread to do the sound playing
       SoundPlayer.playTextThread = threading.Thread(
               target = self.playText,
               args=(text,),
               daemon=True)
       SoundPlayer.playTextThread.start()

    def threadedPlayTextWait(self):
        SoundPlayer.playTextThread.join()

    def playText(self, text):
        SoundPlayer.player.stop()

        if state.soundsOn == False:
            return

        tts = gtts.gTTS(text=text, lang='en', tld='co.uk')
        tts.save('/home/njt/Documents/rpi/rpi-weather/tmp.mp3')

        time.sleep(2)

        if state.switchedToMode8:
            state.switchedToMode8 = False
            return
        if state.soundsOn == False:
            return

        ttsMedia = SoundPlayer.instance.media_new('/home/njt/Documents/rpi/rpi-weather/tmp.mp3')
        SoundPlayer.player.set_media(ttsMedia)
        SoundPlayer.player.set_position(0.0)
        SoundPlayer.player.play()
        while SoundPlayer.player.get_state() != 6:
            time.sleep(0.1)

    def playChimes(self, num):

        if state.soundsOn == False:
            return

        # Stop any sound that may be playing
        SoundPlayer.player.stop()

        # Set up and play the chimes
        SoundPlayer.player.set_media(SoundPlayer.bbHourly)
        SoundPlayer.player.set_position(0.0)
        SoundPlayer.player.play()
        while SoundPlayer.player.get_state() != 6:
            time.sleep(0.1)

        SoundPlayer.player.set_media(SoundPlayer.bbChimes)
        for i in range(num):
            SoundPlayer.player.set_position(0.0)
            SoundPlayer.player.play()
            while SoundPlayer.player.get_state() != 6:
                time.sleep(0.1)
            SoundPlayer.player.stop()
        SoundPlayer.player.stop()

# Main for testing
if __name__ == "__main__":
    state.soundsOn = True
    soundPlayer = SoundPlayer()

    soundPlayer.playText("Hello World")
    print("Playing")
    soundPlayer.playText("Today the weather will be Partly cloudy throughout the day with rain. The high will be 11.7 degrees and the low will be 7.4 degrees. There is a 100.0% chance of rain with a depth of 3.5mm.")

    print("Finished")

