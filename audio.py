import ctypes
import time
from enum import Enum
from random import randint

class WAVEFORMATEX(ctypes.Structure):
    _fields_ = [
        ("wFormatTag", ctypes.c_ushort),
        ("nChannels", ctypes.c_ushort),
        ("nSamplesPerSec", ctypes.c_uint),
        ("nAvgBytesPerSec", ctypes.c_uint),
        ("nBlockAlign", ctypes.c_ushort),
        ("wBitsPerSample", ctypes.c_ushort),
        ("cbSize", ctypes.c_ushort),
    ]

class WAVEHDR(ctypes.Structure):
    _fields_ = [
        ("lpData", ctypes.c_char_p),
        ("dwBufferLength", ctypes.c_uint),
        ("dwBytesRecorded", ctypes.c_uint),
        ("dwUser", ctypes.c_void_p),
        ("dwFlags", ctypes.c_uint),
        ("dwLoops", ctypes.c_uint),
        ("lpNext", ctypes.c_void_p),
        ("reserved", ctypes.c_void_p),
    ]

winmm = ctypes.windll.winmm

class HydrogenSequence(Enum): #audio sequences from hydrogen source code
    SEQ1 = lambda t: ((t & (t >> 8) - (t >> 13 & t)) & ((t & (t >> 8)) - (t >> 13))) ^ ((t >> 8) & t)
    SEQ2 = lambda t: (t - ((t >> 4) & (t >> 8)) & (t >> 12)) - 1
    SEQ3 = lambda t: ((t >> 8 & t >> 4) >> (t >> 16 & t >> 8)) * t
    SEQ4 = lambda t: (t & ((t >> 7) | (t >> 8) | (t >> 16)) ^ t) * t
    SEQ5 = lambda t: (t * t // (1 + ((t >> 9) & (t >> 8)))) & 128
    SEQ6 = lambda t: (t >> 5) | ((t >> 2) * (t >> 5))
    SEQ7 = lambda t: 100 * ((t << 2 | t >> 5 | t ^ 63) & (t << 10 | t >> 11))
    SEQ8 = lambda t: (t // 8) >> ((t >> 9) * t // ((t >> 14) & 3) + 4) if ((t >> 14) & 3) != 0 else (t // 8) >> 0
    SEQ9 = lambda t: 10 * (t & 5 * t | t >> 6 | -6 * t // 7 if t & 32768 else (-9 * t & 100) // 11 if t & 65536 else (-9 * (t & 100)) // 11)
    SEQ10 = lambda t: 10 * ((t >> 7) | (3 * t) | (t >> (t >> 15))) + ((t >> 8) & 5)

class SalinewinSequence(Enum): #audio sequences from salinewin source code
    SEQ1 = lambda t: t & t >> 8
    SEQ2 = lambda t: t >> 5 | (t >> 2) * (t >> 5)
    SEQ3 = lambda t: 2 * (t >> 5 & t) - (t >> 5) + t * (t >> 14 & 14)
    SEQ4 = lambda t: t + (t & t ^ t >> 6) - t * (t >> 9 & (2 if t % 16 else 6) & t >> 9)
    SEQ5 = lambda t: t * (t ^ t + (t >> 15 | 1) ^ (t - 1280 ^ t) >> 10)
    SEQ6 = lambda t: t * ((t // 2 >> 10 | t % 16 * t >> 8) & 8 * t >> 12 & 18) | -(t // 16) + 64
    SEQ6_REMIX = lambda t: t * ((t // 3 >> 20 | t % 32 * t >> 8) & 8 * t >> 12 & 18) | -(t // 16) + 70 #codeflane remix (made for fun :))
    SEQ7 = lambda t: t * (6 if t & 16384 else 5) * (4 - (1 & t >> 8)) >> (3 & t >> 9) | (t | t * 3) >> 5
    SEQ8 = lambda t: t * ((6 if t & 4096 else 16) + (1 & t >> 14)) >> (3 & t >> 8) | t >> (3 if t & 4096 else 4)
    SEQ9 = lambda t: t * (((7 if t % 65536 < 59392 else t & 7) if t & 4096 else 16) ^ (1 & t >> 14)) >> (3 & (-t) >> (2 if t & 2048 else 10))
    SEQ10 = lambda t: t * randint(0, 1000)

class AudioPlayer:
    def __init__(self, seq):
        self.seq = seq

    def _seq(self, count, buf):
        for t in range(count * 2):
            buf[t] = self.seq(t)

    def play(self, count, samples_per_sec=8000):
        nSampleCount = samples_per_sec * count
        nSamplesPerSec = samples_per_sec
        buffer = (ctypes.c_ubyte * (nSampleCount * 2))()
        self._seq(nSampleCount, buffer)

        wf = WAVEFORMATEX()
        wf.wFormatTag = 1
        wf.nChannels = 1
        wf.nSamplesPerSec = nSamplesPerSec
        wf.nBlockAlign = 1
        wf.wBitsPerSample = 8
        wf.nAvgBytesPerSec = nSamplesPerSec
        wf.cbSize = 0

        self.hWaveOut = ctypes.c_void_p()
        winmm.waveOutOpen(ctypes.byref(self.hWaveOut), -1, ctypes.byref(wf), 0, 0, 0)

        self.hdr = WAVEHDR()
        self.hdr.lpData = ctypes.cast(buffer, ctypes.c_char_p)
        self.hdr.dwBufferLength = nSampleCount * 2
        self.hdr.dwFlags = 0

        winmm.waveOutPrepareHeader(self.hWaveOut, ctypes.byref(self.hdr), ctypes.sizeof(self.hdr))
        winmm.waveOutWrite(self.hWaveOut, ctypes.byref(self.hdr), ctypes.sizeof(self.hdr))

        while not (self.hdr.dwFlags & 0x00000001):
            time.sleep(0.01)

        # self.stop()

    def stop(self):
        winmm.waveOutReset(self.hWaveOut)
        winmm.waveOutUnprepareHeader(self.hWaveOut, ctypes.byref(self.hdr), ctypes.sizeof(self.hdr))
        winmm.waveOutClose(self.hWaveOut)
