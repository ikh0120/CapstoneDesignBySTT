import subprocess
import sounddevice as sd
import numpy as np
import os
import time

from scipy.io.wavfile import write


# 녹음할 샘플링 주파수와 시간
fs = 44100  # 샘플링 주파수
duration = 5  # 녹음 시간 (초)
output_dir = 'C:/Users/User/CapstoneDesign/whisper_speechToText/whisper_real_time/mic_test_dir'  # 저장할 디렉토리 절대 경로
output_file = os.path.join(output_dir, 'test_audio.wav')  # 파일 이름 포함한 경로 생성

# 파일을 저장할 디렉토리가 존재하는지 확인하고 없으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 마이크로부터 오디오 데이터 녹음
print("5초 녹음할거니까 5초동안 마이크 테스트 시작해\n")
audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()  # 녹음 완료될 때까지 대기

# 녹음된 데이터를 WAV 파c일로 저장
write(output_file, fs, audio_data)

print(f"파일 저장 위치\n\t{os.path.abspath(output_file)}")

# 저장된 파일을 재생
print("\n\n이제 곧 입력된 녹음 파일 재생 할게\n\n")
time.sleep(3)
subprocess.run(['start', output_file], shell=True)