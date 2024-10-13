import sys
import os
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from gtts import gTTS

# snacks_info 딕셔너리
snacks_info = {     # location: 상품의 위치/price: 가격/calories: 칼로리/carbs: 탄수화물/protein: 단백질/fat: 지방
    "스윙칩":       {"location": "A열 11번째 라인", "price": 1500, "calories": 500, "carbs": 50, "protein": 4, "fat": 30},
    "빼빼로":       {"location": "A열 13번째 라인", "price": 1200, "calories": 330, "carbs": 40, "protein": 3, "fat": 15},
    "허니버터칩":   {"location": "B열 3번째 라인",  "price": 1800, "calories": 455, "carbs": 50, "protein": 6, "fat": 25},
    "프링글스":     {"location": "B열 16번째 라인", "price": 2000, "calories": 520, "carbs": 60, "protein": 5, "fat": 28},
    "칙촉":         {"location": "C열 9번째 라인",  "price": 1000, "calories": 350, "carbs": 40, "protein": 6, "fat": 18},
    "꼬북칩":       {"location": "C열 17번째 라인", "price": 1700, "calories": 480, "carbs": 55, "protein": 4, "fat": 27},
    "오사쯔":       {"location": "D열 6번째 라인",  "price": 1400, "calories": 410, "carbs": 50, "protein": 2, "fat": 20},
    "ABC 초코쿠키": {"location": "D열 22번째 라인", "price": 1200, "calories": 320, "carbs": 30, "protein": 3, "fat": 16},
    "콘초":         {"location": "E열 2번째 라인",  "price": 1000, "calories": 300, "carbs": 40, "protein": 2, "fat": 12},
    "콘칩":         {"location": "E열 12번째 라인", "price": 1100, "calories": 425, "carbs": 50, "protein": 5, "fat": 22},
    "다이제":       {"location": "F열 3번째 라인",  "price": 1600, "calories": 450, "carbs": 50, "protein": 6, "fat": 25},
    "포카칩":       {"location": "F열 7번째 라인",  "price": 1300, "calories": 480, "carbs": 50, "protein": 4, "fat": 26}
}

# 음성 인식 스레드 구현
class SpeechRecognitionThread(QThread):
    recognized = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.stop_flag = False

    def run(self):
        while not self.stop_flag:
            try:
                with sr.Microphone() as source:
                    print("음성 인식 대기 중...")
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=25)
                    recognized_text = self.recognizer.recognize_google(audio, language='ko')
                    print(f"인식된 텍스트: \n\t{recognized_text}\n\n")
                    self.recognized.emit(recognized_text)
            except sr.UnknownValueError:
                print("음성을 인식하지 못했습니다.")
            except sr.RequestError as e:
                print(f"음성 인식 서비스에 문제가 발생했습니다: {e}")
            except sr.WaitTimeoutError:
                print("대기 시간이 초과되었습니다. 다시 음성 인식을 시도합니다.")
                continue  # 대기 시간 초과 시 다시 음성 인식 시도

    def stop(self):
        self.stop_flag = True

class App(QWidget):
    def __init__(self):
        super().__init__()
        # 창을 맨 앞으로 유지시키는 코드 
        # 하지만 <windows> -> 같은 단축키 사용이 불편하기에 발표 때 키기
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.title = 'Store Information By SMART'
        self.initUI()
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.recognized.connect(self.on_recognized)
        self.speech_thread.start()
        self.active_mode = False

    def initUI(self):
        self.setWindowTitle(self.title)

        self.label_question_title = QLabel('질문', self)
        self.label_question_title.setStyleSheet("""
            QLabel {
                font-size: 100px;
                color: #333;
                font-weight: bold;
            }
        """)

        self.label_question = QLabel("궁금하신 점이 있으시다면 '똑똑'이라고 노크하신 뒤 시작해주세요. ", self)
        # self.label_question.setAlignment(Qt.AlignTop) /# 텍스트 상단 배치
        self.label_question.setWordWrap(True)
        self.label_question.setStyleSheet("""
            QLabel {
                font-size: 70px;
                color: #333;
                background-color: #E8F5E9;
                padding: 20%;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-bottom: 20px;
            }
        """)

        self.label_answer_title = QLabel('답변', self)
        self.label_answer_title.setStyleSheet("""
            QLabel {
                font-size: 100px;
                color: #333;
                font-weight: bold;
            }
        """)

        self.label_answer = QLabel('여기에 답변이 표시됩니다.', self)
        # self.label_answer.setAlignment(Qt.AlignTop) # 텍스트 상단 배치
        self.label_answer.setWordWrap(True)
        self.label_answer.setStyleSheet("""
            QLabel {
                font-size: 70px;
                color: #333;
                background-color: #FFF3E0;
                padding: 20%;
                border: 2px solid #FF9800;
                border-radius: 8px;
                margin-bottom: 20px;
            }
        """)

        self.button_exit = QPushButton('프로그램 종료', self)
        self.button_exit.setFixedHeight(50)
        self.button_exit.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 20px;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """)

        self.button_exit.clicked.connect(self.on_click_exit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_exit)

        layout = QVBoxLayout()
        layout.addWidget(self.label_question_title)
        layout.addWidget(self.label_question)
        layout.addWidget(self.label_answer_title)
        layout.addWidget(self.label_answer)
        layout.addLayout(button_layout)

                # 각 요소에 비율 설정
        layout.setStretch(0, 2)  # 질문 라벨의 비율
        layout.setStretch(1, 4)  # 초록색 텍스트 박스의 비율
        layout.setStretch(2, 2)  # 답변 라벨의 비율
        layout.setStretch(3, 4)  # 주황색 텍스트 박스의 비율

        self.setLayout(layout)
        self.showMaximized()
        self.setStyleSheet("""
            QWidget {
                background-color: #F4F4F4;
            }
        """)

    def on_recognized(self, recognized_text):
        # "똑똑"이라는 단어가 입력된 경우
        if "똑똑" in recognized_text:
            self.label_question.setText("음성 인식 결과가 여기에 표시됩니다. ")  # "똑똑"이라고 인식된 텍스트 표시
            self.label_answer.setText("안녕하세요. \n궁금하신 점이 있으시다면 말씀해주세요. ")
            self.play_response("안녕하세요. 궁금하신 점이 있으시다면 말씀해주세요. ")
            self.active_mode = True  # 질문을 받을 준비 상태로 전환
        elif self.active_mode:
            # active_mode가 True일 때만 질문에 대해 응답
            self.label_question.setText(f"{recognized_text}")
            response_text, activate_question = transcribe_and_respond(self, recognized_text)
            self.label_answer.setText(f"{response_text}")
            self.play_response(response_text)
            self.active_mode = activate_question
        else:
            # 아무 작업도 수행하지 않고 대기
            print("똑똑 노크해주세요. ")

    def play_response(self, text):
        try:
            print(f"답변 텍스트: \n\t{text}\n\n")

            tts = gTTS(text=text, lang='ko')
            tts.save('response.wav')

            os.system(f"start /min {os.path.join(os.getcwd(), 'response.wav')}")
        except Exception as e:
            self.label_answer.setText(f"TTS 오류: {e}")

    def on_click_exit(self):
        self.speech_thread.stop()
        sys.exit()

# 음성인식 및 TTS 로직 구현
def transcribe_and_respond(self, text):
    if ("무엇" in text or "뭐" in text or "어떤" in text or "상품" in text or "정보" in text or "종류" in text) and not ("높" in text or "많" in text or "비싼" in text or "낮" in text or "적" in text or "싼" in text):
        # snacks_info에서 키 값들만 가져와서 리스트로 변환
        items = ', '.join(snacks_info.keys())
        response = f"매장에는 {items}이 있습니다. \n해당 상품들의 위치, 가격 혹은 상품들의 상세한 정보를 여쭤보세요.  "
        return response, True

    if "높" in text or "많" in text or "비싼" in text:
        max_price = 0.0
        max_calories = 0.0
        max_carbs = 0.0
        max_protein = 0.0
        max_fat = 0.0
        max_price_snack = ""
        max_calories_snack = ""
        max_carbs_snack = ""
        max_protein_snack = ""
        max_fat_snack = ""

        # 최대값 찾기
        for snack_name, info in snacks_info.items():
            if "가격" in text or "비싼" in text:
                if max_price < info['price']:
                    max_price = info["price"]
                    max_price_snack = snack_name
                elif max_price == info['price']:
                    max_price_snack += "," + snack_name
            if "칼로리" in text:
                if max_calories < info['calories']:
                    max_calories = info["calories"]
                    max_calories_snack = snack_name
                elif max_calories == info['calories']:
                    max_calories_snack += "," + snack_name
            if "탄수화물" in text:
                if max_carbs < info['carbs']:
                    max_carbs = info["carbs"]
                    max_carbs_snack = snack_name
                elif max_carbs == info['carbs']:
                    max_carbs_snack += "," + snack_name
            if "단백질" in text:
                if max_protein < info['protein']:
                    max_protein = info["protein"]
                    max_protein_snack = snack_name
                elif max_protein == info['protein']:
                    max_protein_snack += "," + snack_name
            if "지방" in text:
                if max_fat < info['fat']:
                    max_fat = info["fat"]
                    max_fat_snack = snack_name
                elif max_fat == info['fat']:
                    max_fat_snack += "," + snack_name

        # 조건에 따른 결과 출력
        if "가격" in text or "비싼" in text:
            return f"가장 높은 가격을 가진 상품은 {max_price_snack}이며, \n가격은 {max_price}원입니다.", True
        elif "칼로리" in text:
            return f"가장 높은 칼로리를 가진 상품은 {max_calories_snack}이며, \n칼로리는 {max_calories}kcal입니다.", True
        elif "탄수화물" in text:
            return f"가장 높은 탄수화물을 가진 상품은 {max_carbs_snack}이며, \n탄수화물은 {max_carbs}g입니다.", True
        elif "단백질" in text:
            return f"가장 높은 단백질을 가진 상품은 {max_protein_snack}이며, \n단백질은 {max_protein}g입니다.", True
        elif "지방" in text:
            return f"가장 높은 지방을 가진 상품은 {max_fat_snack}이며, \n지방은 {max_fat}g입니다.", True
        else:
            return "성분을 다시 말씀해주세요. \n예를 들어 '가장 높은 칼로리를 가진 식품이 무엇인가요?'라고 말씀해주세요. ", True

    if ("낮" in text or "적" in text or "싼" in text) and "비싼" not in text:
        # 최소값 초기화
        min_price = float('inf')
        min_calories = float('inf')
        min_carbs = float('inf')
        min_protein = float('inf')
        min_fat = float('inf')
        min_price_snack = ""
        min_calories_snack = ""
        min_carbs_snack = ""
        min_protein_snack = ""
        min_fat_snack = ""

        # 최소값 찾기
        for snack_name, info in snacks_info.items():
            if "가격" in text or ("싼" in text and "비싼" not in text):
                if min_price > info['price']:
                    min_price = info["price"]
                    min_price_snack = snack_name
                elif min_price == info['price']:
                    min_price_snack += "," + snack_name
            if "칼로리" in text:
                if min_calories > info['calories']:
                    min_calories = info["calories"]
                    min_calories_snack = snack_name
                elif min_calories == info['calories']:
                    min_calories_snack += "," + snack_name
            if "탄수화물" in text:
                if min_carbs > info['carbs']:
                    min_carbs = info["carbs"]
                    min_carbs_snack = snack_name
                elif min_carbs == info['carbs']:
                    min_carbs_snack += "," + snack_name
            if "단백질" in text:
                if min_protein > info['protein']:
                    min_protein = info["protein"]
                    min_protein_snack = snack_name
                elif min_protein == info['protein']:
                    min_protein_snack += "," + snack_name
            if "지방" in text:
                if min_fat > info['fat']:
                    min_fat = info["fat"]
                    min_fat_snack = snack_name
                elif min_fat == info['fat']:
                    min_fat_snack += "," + snack_name

        # 조건에 따른 결과 출력
        if "가격" in text or ("싼" in text and "비싼" not in text):
            return f"가장 낮은 가격을 가진 상품은 {min_price_snack}이며, \n가격은 {min_price}원입니다.", True
        elif "칼로리" in text:
            return f"가장 낮은 칼로리를 가진 상품은 {min_calories_snack}이며, \n칼로리는 {min_calories}kcal입니다.", True
        elif "탄수화물" in text:
            return f"가장 낮은 탄수화물을 가진 상품은 {min_carbs_snack}이며, \n탄수화물은 {min_carbs}g입니다.", True
        elif "단백질" in text:
            return f"가장 낮은 단백질을 가진 상품은 {min_protein_snack}이며, \n단백질은 {min_protein}g입니다.", True
        elif "지방" in text:
            return f"가장 낮은 지방을 가진 상품은 {min_fat_snack}이며, \n지방은 {min_fat}g입니다.", True
        else:
            return "성분을 다시 말씀해주세요. \n예를 들어 '가장 낮은 칼로리를 가진 식품이 무엇인가요?'라고 말씀해주세요.", True



    for snack_name, info in snacks_info.items():
        activate_question = False;
        if snack_name in text:
            requested_info = []

            notOneMoreTime = True
            if "위치" in text or "어디" in text or "어딨어" in text:
                requested_info.append(f"위치는 {info['location']}")
            if "가격" in text or "얼마" in text:
                requested_info.append(f"가격은 {info['price']}원")

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
            if requested_info:
                response = f"{snack_name}의 {', '.join(requested_info)}입니다. \n또 다른 궁금하신 점이 있으시다면 다시 한 번 '똑똑'이라고 노크해주세요. "
            else:
                return f"{snack_name}에 대한 요청하신 정보가 없습니다. /n 다시 한 번 말씀해주세요. ", True
            return response, False
    return "말씀하신 상품을 찾을 수 없습니다. \n다시 한 번 '똑똑'이라고 노크해주세요. ", False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
