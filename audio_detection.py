from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer, player_for, from_file
import player
import sys
import wave
from thread import *
from pynput import keyboard
import datetime 
import os
from pydub import AudioSegment
from gui import *
from argparse import ArgumentParser
from gui import *

parser = ArgumentParser()
parser.add_argument("-g", "--gui", dest="gui",
                    help="Display Graphic Interface", action='store_true')

parser.add_argument("-f", "--folder", dest="folder",
                    help="Display Graphic Interface", default='playlist/')

parser.add_argument("-t", "--threshold", dest="threshold",
                    help="Audio Detection Threshold", default=51)

args = parser.parse_args()

play_folder = args.folder

energy_threshold = int(args.threshold)

useGui = args.gui

print('play_folder', play_folder)
print('useGui', useGui)

class AudioDetection:
  def __init__(self, _useGui):
    # parametros de áudio
    max_length = 1000000
    max_interval = 12000
    max_continuous_silence = 500
    min_length = 150
    
    self.sample_rate = 48000
    self.asource = ADSFactory.ads(record=True, max_time = max_length, sampling_rate = self.sample_rate)

    self.sample_width = self.asource.get_sample_width()
    self.channels = self.asource.get_channels()
    # START VALIDATOR
    self.validator = AudioEnergyValidator(sample_width=self.sample_width, energy_threshold = energy_threshold)
    self.tokenizer = StreamTokenizer(validator=self.validator, min_length=min_length, max_length=max_length, max_continuous_silence=max_continuous_silence)

    self.audio_folder = 'recordings/' + '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now()) + '/'
    if not os.path.exists(os.path.dirname(self.audio_folder)):
      try:
          os.makedirs(os.path.dirname(self.audio_folder))
      except OSError as exc: # Guard against race condition
          if exc.errno != errno.EEXIST:
              raiseRec
    os.chmod('recordings', 0o777)
    os.chmod(self.audio_folder, 0o777)
    self.MODE = 'ECHO'

    self.useGui = _useGui

    if self.useGui:
      root = Tk()
      self.display = GUI(root, True)
      self.display.display_image()

  def start(self):
    self.listener = keyboard.Listener(
      on_press=self.on_press,
      on_release=self.on_release)
    self.listener.start()
    self.listen()

  def listen(self):
    ## abrir microfone
    self.asource.open()
    print("\n  ** Listening!!!")      
    ## começar tokenizer
    self.tokenizer.tokenize(self.asource, callback=self.onDetection)
    self.asource.close()

  def on_press(self, key):
    return ''

  def on_release(self, key):
    if hasattr(key, 'char'):
      if key.char == 'e':
        self.MODE = 'ECHO'
        print('set mode to', self.MODE)
      if key.char == 'r':
        self.MODE = 'RANDOM'
        print('set mode to', self.MODE)
      if key.char == 'q':
        self.asource.close()
        sys.exit(0)

  def onDetection(self, data, start, end):
    name = "{0}-{1}".format(start, end) + '.wav'
    print(name)
    filename = self.savefile(data, start, end)
    print('current mode', self.MODE)
    if self.MODE == 'RANDOM':
      randomfile = player.getRandomFile(play_folder)
      player.play(randomfile)
    if self.MODE == 'ECHO':
      player.play(filename)
    self.display.display_image()
    print("finished playing")

  def savefile(self, data, start, end):
    name = "{0}-{1}".format(start, end) + '.wav'
    filename = self.audio_folder + name

    # save wav file
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(self.channels)
    waveFile.setsampwidth(self.sample_width)
    waveFile.setframerate(self.sample_rate)
    waveFile.writeframes(b''.join(data))
    waveFile.close()

    # normalize volume
    sound = AudioSegment.from_file(filename, "wav")
    normalized_sound = self.match_target_amplitude(sound, -15.0)
    with_fade = normalized_sound.fade_in(200).fade_out(200)
    with_fade.export(filename, format="wav")
    
    print('audio saved at', filename)
    return filename

  def match_target_amplitude(self, sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)
    
ad = AudioDetection(useGui)
ad.start()