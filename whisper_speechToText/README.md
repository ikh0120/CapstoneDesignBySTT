Capstone Design 음성인식 프로그램 정리

실행 방법: 터미널에서 하위 코드 작성하기
	경로이동
	cd C:/Users/User
	가상환경 실행
	./CapstoneDesign/Scripts/activate
	실행파일이 있는 경로로 이동
	cd CapstoneDesign/whisper_speechToText/whisper_real_time
	파일 store_info_ui.py 실행하기
	python store_info_ui.py	

self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
	이 코드는 프로그램을 실행했을 때 맨 위로 가게 하는 코드이다. 
	발표 때 프로그램 ui를 최상단에 유지하려면 주석처리한 이 코드를 키고
	아닐때는 <windows>를 활용한 창의 위치 및 크기를 조절하는 단축키가 안먹히기에
	웬만하면 주석처리
	그리고 직접 이  3가지 버튼은 누를 수 있음 
	발표할 때 직접 누르면서 처리하기
	이 코드를 주석처리한 위치는
	<Ctrl> + f로 텍스트 찾기를 실행한 후 “발표”라는 텍스트를 검색하면
	이렇게 뜨는데 이 코드를 주석 해제하면 ui를 최상단 고정 가능함
 
 ![image](https://github.com/user-attachments/assets/953c957b-2888-4f25-861a-7bc6ba9deb1b)


초기화면

![image](https://github.com/user-attachments/assets/71bece07-b138-4837-ba9c-7f324fc6abbd)

똑똑이라고 마이크에 말을 하게 될 시 google web speech API로 stt를 실행하며
해당 똑똑이라는 speech가 text로 변환됨 

하지만 변환된 텍스트는 질문 밑의 텍스트 박스에 안찍히고 
이 때 active_mode 변수는 초기값 False에서 True로 바뀌며
if active_mode == False:
   프로그램 동작 안함;
else:
   프로그램 동작;
“음성 인식 결과가 여기에 표시됩니다.”라는 안내문이 출력됨

이후 대부분의 질문은 질문 후 똑똑이라는 speech로 활성화 후 실행해야지만
response.wav 음성파일이 실행됨

프로그램의 동작을 제어하는 코드를 넣은 이유:
   제어하지 않으면 모든 소리에 대해 stt를 수행하고 tts 번역을 하기 때문
   
![image](https://github.com/user-attachments/assets/6b312ba6-7200-4804-b656-a9363773aacb)

0-0. 과자종류: 
	스윙칩, 빼빼로, 허니버터칩, 프링글스, 칙촉, 꼬북칩, 오사쯔, ABC 초코쿠키, 콘초, 	콘칩, 다이제, 포카칩

예시 질문과 답변들
1-0. 모든 상품 종류
1-1. 웬만하면 가게에 존재하는 상품의 종류를 다 모르기에 상품의 모든 종류를 알려주는 코드
	질문	질문에 들어가야 되는 stt로 변환한 텍스트
		(“무엇” or “뭐” or “어떤” or “상품” or “정보” or “종류”)
		and not으로 밑에서 바로 위의 코드가 인식되었을 때 반응을 안함
		("높" or "많" or "비싼" or "낮" or "적" or "싼")
		ex) 매장에 뭐가 있어?
	답변	매장에는 (과자종류들 싹 다 나열)이 있습니다. 
		해당 상품들의 위치, 가격 혹은 상품들의 상세한 정보를 여쭤보세요.
 
2-0 가격과 영양 정보를 바탕으로 가장 높은 값, 가장 낮은 값을 가진 상품을 출력하는 코드
2-1. 상품의 가격, 칼로리, 탄수화물, 단백질, 지방이 가장 많은 상품을 찾아주는 코드
	질문	질문에 들어가야 되는 stt로 변환한 텍스트
		(“높” or “많” or “비싼”)
		and 
		((“가격” or “비싼”) or “칼로리” or “탄수화물” or “단백질” or “지방” )
		ex) 가장 비싼 상품이 뭐에요?
	답변	가장 높은 가격을 가진 상품은 프링글스이며,
		가격은 2000원입니다.

2-2. 상품의 가격, 칼로리, 탄수화물, 단백질, 지방이 가장 적은 상품을 찾아주는 코드
	질문	질문에 들어가야 되는 stt로 변환한 텍스트
		(“낮”, “적”, “싼”)
		and
		((“가격” or “싼”) or “칼로리” or “탄수화물” or “단백질” or “지방” )
		ex) 가장 싼 상품이 뭐에요?
	답변	가장 낮은 가격을 가진 상품은 칙촉, 콘초이며,
		가격은 1000원입니다.

2-3. (“높” or “많”)만 포함되어 있고 영양성분, 가격 비싼이 포함되어있지 않을 경우
	답변	성분을 다시 말씀해주세요.
		예를 들어 '가장 높은 칼로리를 가진 식품이 무엇인가요?'라고 말씀해주세요.

2-4. (“낮” or “적”)만 포함되어 있고 영양성분, 가격 비싼이 포함되어있지 않을 경우
	답변	성분을 다시 말씀해주세요.
		예를 들어 '가장 높은 칼로리를 가진 식품이 무엇인가요?'라고 말씀해주세요.

2-5. 칼로리, 탄수화물, 지방, 단백질의 함량을 물어봤을 때 같을 경우 
	A 상품과 B 상품의 함량이 같다면 같은 함량의 상품들의 이름과 상품정보가 같이 출력됨

3-0. 상품 상세정보를 출력하는 코드
	질문	상품의 상세정보를 물어봄
		상품 정보(snacks_info 딕셔너리의 키) 
		and
		상품 정보의 상세 정보(상품 정보의 하위 딕셔너리의 키)
		ex) 포카칩의 위치와 칼로리 좀 알려줘
	답변	포카칩의 위치는 F열 7번째 라인, 칼로리는 480kcal입니다.
		또 다른 궁금하신 점이 있으시다면 다시 한 번 '똑똑'이라고 노크해주세요.
	
	질문 	포카칩의 가격과 영양성분 및 칼로리 좀 알려줘

	답변	포카칩의 가격은 1300원, 칼로리는 480kcal이며, 
		탄수화물은 50g, 단백질은 4g, 지방은 26g입니다.
		또 다른 궁금하신 점이 있으시다면 다시 한 번 '똑똑'이라고 노크해주세요.

	딕셔너리의 키 중 calories(칼로리), carbs(탄수화물), protein(단백질), fat(지방)을 
	영양성분으로 해당 코드 내에서 묶었고 
	STT 처리한 뒤 if문을 돌렸을 때 영양성분이 존재하고 calories(칼로리), carbs(탄수화물), 
	protein(단백질), fat(지방)이 존재할 때 4가지 영양성분이 중복되기에 
	영양성분이 입력되었을 때
	notOneMoreTime = True로 설정, 
	영양성분이 입력되지 않았을 때 
	notOneMoreTime = False로 설정하여 중복된 답변이 나오지 않게 만들었음

	.gitignore 파일이란
		git에 업로드 하기 싫은 파일 혹은 폴더를 적으면 안올라감
		그래서 Include/, Lib/, Scripts/, share/, pyvenv.cfg 파일이 안올라간거
		이 네개의 폴더와 하나의 파일은 CapstoneDesign 가상환경을 만들 때 자동으로 생긴 것이므로 없어도 됨
	
	mic_test_dir/mic_test.py 실행 시 5초동안 음성녹음을 진행할 수 있으며 
		mic_test_dir/test_audio.wav에 저장되고
		mic_test_dir/test_audio.wav가 실행된다. 
		이 파일은 마이크 테스트를 진행하는 파일이며 
		마이크가 음성(소리)을 잘 받아오는지 테스트를 하기 위해 만들었다. 
	
	**처음에는 폴더 이름에 나와있다 싶이 Google Web Speech Api** 말고
	**Real Time Whisper를 사용하였다. **
	중도 포기한 whisper 파일
	whisper_speechToText\whisper_real_time\transcribe_demo.py를 실행했을 때 whisper가 동작하며
	whisper를 실행하려면 ./CapstoneDesign/Scripts/activate를 C:Users/User 경로에서 실행하면 (CapstoneDesign)이라는 가상환경에 접속되고 경로를 C:Users/User/CapstoneDesign/whisper_speechToText/whisper_real_time 경로로 변경한 뒤 python transcribe_demo.py --model (모델명)) --non_english로 실행하면 된다. 
	여기서 모델명은 tiny, base, small, medium, large 순서로 무거워지고 커지며 그만큼 정확도가 늘어나지만 성능이 좋아지는 대신 느리게 실행된다. 
	따라서 본인은 small 모델을 사용하였다. 
	whisper는 느리고 정확하게 stt로 변환한 텍스트로 찍어내지 못함
	하지만 whisper는Ggoogle Web Speech API처럼 한 두 줄 씩 받는 것이 아니고, 
	한번에 30초씩 받을 수 있다. 

	본인은 Real-Time Whisper를 통해 Speech를 Text로 변환하는 STT(SpeechToText) 기법을 사용하였으며
	변환한 텍스트를 transcription.txt 파일에 저장한 후 조건문을 거쳐 텍스트를 전처리 후
	TTS(Text To Speech)를 사용하여 음성파일을 저장 후 출력했다. 

	하지만 Google Web Speech API를 발견한 뒤 stt를 더 빠르고 정확하게 해내는 것을 보고 
	Real-Time Whisper에서 Google Web Speech API로 변경했으며 
	이 API를 사용 후 질문들의 목록 및 UI 설계까지 완료했다. 
	
	중요 프로그램들의 경로
	1. 마이크 테스트
		실행파일
			whisper_speechToText/whisper_real_time/mic_test_dir/mic_text.py
		출력 wav 파일
			whisper_speechToText/whisper_real_time/mic_test_dir/test_audio.wav

	2. 최종 실행 파일
		실행파일
			whisper_speechToText/whisper_real_time/store_info_ui.py
		출력되는 wav 파일
			whisper_speechToText/whisper_real_time/response.wav

	3. google web speech API를 사용하기 전의 real-time whisper로 만들던 파일
		실행 파일 
			whisper_speechToText/whisper_real_time/transcribe_demo.py
		출력되는 wav 파일
			whisper_speechToText/whisper_real_time/response.wav

	
