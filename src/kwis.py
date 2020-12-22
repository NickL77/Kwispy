import os
import pyaudio
import time

import numpy as np

from rnnoise import RNNoise

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 480

class Kwispy():

    def __init__(self):

        print('a')
        self.audio = pyaudio.PyAudio()
        print('b')
        self.denoiser = RNNoise()
        print('c')

    def start(self):
        
        self.stream = self.audio.open(format=FORMAT, \
                    channels=CHANNELS, \
                    rate=RATE, \
                    input=True, \
                    output=True, \
                    stream_callback=self._denoise_callback, \
                    frames_per_buffer=CHUNK)

        sink_id = self._get_virtsink_id()
        self.stream.start_stream()

        stream_index = self._get_stream_index()
        os.popen("pactl move-sink-input {} {}".format(stream_index, sink_id))

        while True:
            time.sleep(30)

        # self.stream.stop_stream()
        # self.stream.close()

    def _denoise_callback(self, in_data, frame_count, time_info, status):

        denoised_frame = self.denoiser.process_frame(in_data)[1]
        return (denoised_frame, pyaudio.paContinue)

    def _get_virtsink_id(self):

        output = os.popen("pactl list short sinks")

        for line in output.readlines():
            info = line.split("\t")
            if info[1] == "virtsink":
                return int(info[0])

        raise RuntimeError

    def _get_stream_index(self):

        output = os.popen("pacmd list-sink-inputs")

        index = 0
        index_pid = 0
        py_pid = int(os.getpid())

        for line in output.readlines():
            line = line.strip()
            if line.startswith("index:"):
                index = int(line[7:])

            s, e = 0, 0
            if line.startswith("application.process.id"):
                for i, c in enumerate(line):
                    if c == "\"":
                        if not s:
                            s = i
                        else:
                            e = i
                            break
                assert s and e
                index_pid = int(line[s + 1:e])

            if index_pid == py_pid:
                return(index)
            
        raise RuntimeError

kwispy = Kwispy()
kwispy.start()
