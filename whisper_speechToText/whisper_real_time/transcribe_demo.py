import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch
from gtts import gTTS
from queue import Queue
from time import sleep
from sys import platform

# 가상환경 키는 법
##  C:\Users\User 이 경로에서
##  .\CapstoneDesign\Scripts\activate
# 경로
##  (CapstoneDesign) PS C:\Users\User\CapstoneDesign\whisper_speechToText\whisper_real_time>
# transcribe_demo.py 실행방법
##  위의 경로에서 python transcribe_demo.py --model small --non_english

# 과자 정보 딕셔너리
snacks_info = {
    "스윙칩": {"location": "A열 11번째 라인", "price": 1500, "calories": 500, "carbs": 50, "protein": 4, "fat": 30},
    "빼빼로": {"location": "A열 13번째 라인", "price": 1200, "calories": 300, "carbs": 45, "protein": 3, "fat": 15},
    "허니버터칩": {"location": "B열 3번째 라인", "price": 1800, "calories": 450, "carbs": 55, "protein": 3, "fat": 25},
    "프링글스": {"location": "B열 16번째 라인", "price": 2000, "calories": 520, "carbs": 60, "protein": 5, "fat": 28},
    "칙촉": {"location": "C열 9번째 라인", "price": 1000, "calories": 350, "carbs": 40, "protein": 2, "fat": 18},
    "꼬북칩": {"location": "C열 17번째 라인", "price": 1700, "calories": 480, "carbs": 52, "protein": 4, "fat": 27},
    "오사쯔": {"location": "D열 6번째 라인", "price": 1400, "calories": 410, "carbs": 50, "protein": 2, "fat": 20},
    "ABC 초코쿠키": {"location": "D열 22번째 라인", "price": 1200, "calories": 320, "carbs": 38, "protein": 3, "fat": 16},
    "콘초": {"location": "E열 2번째 라인", "price": 1000, "calories": 300, "carbs": 40, "protein": 2, "fat": 12},
    "콘칩": {"location": "E열 12번째 라인", "price": 1100, "calories": 420, "carbs": 50, "protein": 5, "fat": 22},
    "다이제": {"location": "F열 3번째 라인", "price": 1600, "calories": 450, "carbs": 55, "protein": 6, "fat": 25},
    "포카칩": {"location": "F열 7번째 라인", "price": 1300, "calories": 480, "carbs": 53, "protein": 4, "fat": 26}
}

# 음성인식 및 TTS 로직 구현
def transcribe_and_respond(text):
    # 텍스트에서 과자 이름과 속성 추출
    for snack_name, info in snacks_info.items():
        if snack_name in text:  # 사용자가 과자 이름을 언급했을 때
            # 요청된 속성들을 분석
            requested_info = []

            # 영양성분이라는 문자열이 입력되지 않았을 때
            notOneMoreTime = True
            
            if "영양 성분" in text or "영양성분" in text:
                calories = info["calories"]
                carbs = info["carbs"]
                protein = info["protein"]
                fat = info["fat"]
                requested_info.append(f"칼로리는 {calories}kcal이며, 탄수화물은 {carbs}g, 단백질은 {protein}g, 지방은 {fat}g")
                notOneMoreTime = False

            if notOneMoreTime:
                if "칼로리" in text:
                    requested_info.append(f"칼로리는 {info['calories']}kcal")
                if "탄수화물" in text:
                    requested_info.append(f"탄수화물은 {info['carbs']}g")
                if "단백질" in text:
                    requested_info.append(f"단백질은 {info['protein']}g")
                if "지방" in text:
                    requested_info.append(f"지방은 {info['fat']}g")

            if "위치" in text or "어디" in text or "어딨어" in text or "찾아줘" in text or "주세요" in text:
                requested_info.append(f"위치는 {info['location']}")
            if "가격" in text or "얼마" in text:
                requested_info.append(f"가격은 {info['price']}원")



            # 요청된 정보가 있을 경우 응답 생성
            if requested_info:
                response = f"{snack_name}의 {', '.join(requested_info)}입니다."
            else:
                response = f"{snack_name}에 대한 요청하신 정보가 없습니다."

            return response
    return "말씀하신 상품을 찾을 수 없습니다. \n다시 한 번 말씀해주세요!"

# TTS를 통해 음성 출력
def text_to_speech(text):
    tts = gTTS(text=text, lang='ko')
    tts.save("response.wav")
    os.system("start response.wav")  # 윈도우 환경에서 오디오 파일 재생

def main():
    # Whisper 모델 및 STT 설정
    model = whisper.load_model("small")
    recorder = sr.Recognizer()
    source = sr.Microphone(sample_rate=16000)

    with source:
        recorder.adjust_for_ambient_noise(source)

    while True:
        print("음성을 입력하세요...\n")
        with source:
            print('음성인식 시작')
            audio = recorder.listen(source)
            print('음성인식 끝')
        # 음성을 Whisper로 텍스트로 변환
        audio_data = np.frombuffer(audio.get_raw_data(), np.int16).astype(np.float32) / 32768.0  # numpy 배열로 변환
        print('전처리 시작')
        result = model.transcribe(audio_data)
        text = result['text']

        print(f"\t인식된 텍스트: {text}")

        # 인식된 텍스트에 따라 응답 생성
        response = transcribe_and_respond(text)
        print(f"\t응답: {response}")

        # TTS로 응답 출력
        text_to_speech(response)

if __name__ == "__main__":
    main()
