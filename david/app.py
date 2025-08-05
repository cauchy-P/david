from flask import Flask, render_template, request
from gtts import gTTS
import base64
from io import BytesIO
import socket
app = Flask(__name__)

# 유효한 언어 목록 (보너스: lang 검증)
VALID_LANGUAGES = ['ko', 'en', 'ja', 'es']
@app.route('/')
def home():
    if app.debug:
        hostname = '컴퓨터(인스턴스) : ' + socket.gethostname()
    else:
        hostname = ' '

    return render_template('index.html', computername=hostname)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        lang = request.form.get('lang', 'ko')  # 기본 ko
        
        # 보너스: lang 유효성 검증
        if lang not in VALID_LANGUAGES:
            return render_template('index.html', error='유효하지 않은 언어입니다. ko, en, ja, es 중 선택하세요.')
        
        # 예외 처리: 빈 텍스트
        if not input_text.strip():
            return render_template('index.html', error='텍스트를 입력하세요.')
        
        try:
            # TTS 변환
            tts = gTTS(text=input_text, lang=lang)
            
            # 메모리에 MP3 저장 (파일로 저장하지 않음)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # base64 인코딩
            audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
            
            # 보너스: 입력 로그 저장
            with open('input_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(f"Text: {input_text}, Lang: {lang}\n")
            
            return render_template('index.html', audio=audio_base64)
        
        except Exception as e:
            # gTTS 실패 등 예외 처리
            return render_template('index.html', error=f'오류 발생: {str(e)}')
    
    # GET: 폼 렌더링
    return render_template('index.html')

@app.route("/test2")
def test2():
    return render_template('test2.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
