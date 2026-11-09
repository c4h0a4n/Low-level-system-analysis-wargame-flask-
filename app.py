#!/usr/bin/env python3 //리눅스야 셰뱅이니까 직접 실행하지말고 usr/bin/env에서 python3를 찾아서 실행해
import subprocess #파이썬아 내가 리눅스랑 대화 할 수 있는 전화기(도구,subprocess)줄게
from flask import Flask, request, render_template #flask라는 도구(가상서버)에서 Flask,request,render_template를 가져온다

APP = Flask(__name__)#flask라는 서버를 생성 후 __name__에서 이 파일이 불러올 파일인지 아니면 여기서 실행하는 파일인지 판단 후 app라는 변수에 집어넣는다

@APP.route('/', methods=['GET', 'POST'])# 데코레이터로 이 코드가 일반코드로 실행 안하고 플라스크 라우팅 테이블에 등록한 후 root의 경로로 들어오는 GET과 POST방식으로만 들어 올 수있게 만든다.
def index(): # index라는 함수 생성
    if request.method == 'POST':# 만일 요청 받은 방법이 POST방식이라면 아래코드 실행
        user_input = request.form.get('user_input')# user_input 이라는 변수를 만들고 ,POST방식으로 보낸 data가 user_input(key)와 일치하면 그 키의 짝을 data를 변수에 넣어라
        cmd = f'echo $({user_input})' # cmd라는 변수를 생성 후 user_input 리눅스 쉘 명령어로서 우선 실행후 echo로 출력할 문자를 담음
        if 'flag' in cmd: # 만일 'flag'가 cmd라는 변수 안에있다면 아래의 코드 실행 
            return render_template('index.html', result='No!')# 레지스터에 값을 반환하는데 template 파일 안에서 index.html파일을 찾아서 연결시키고 result = NO 값을 반환하여 html 파일에 반환할 수 있도록함

        try:# 일단 코드를 실행시켜봐 만일 오류가 난다면 except로 가
            output = subprocess.check_output(['/bin/sh', '-c', cmd], timeout=5)# subprocess(전화기)가 output이라는 변수 안에 셸의 확인 이후의 출력을 받는데 그 출력이 bin파일안에있는sh파일(셸 파일)을 실행하는데 cmd 를 문자가 아닌 변수로서 입력된 코드를 실행하고 5초 안에 작업을 끝내지 못하면 kill(추방)하는 명령을 집어넣는다
            return render_template('index.html', result=output.decode('utf-8'))# template폴더 안 index.html파일을 파이썬과 분리하여 실행하는데 html파일을 불러와서 엔진을 넣은 후 result칸에 utf-8의 규격에 맞게 문자열로 디코딩(변환)한 값을 result에저장한 걸 html파일에 반환함
        except subprocess.TimeoutExpired:#subprocess는 파이썬과 커널과 대화하도록 하는 전화기인데 수신자(파이썬)이 응답이 없어 TimeoutExpired 경고가 뜨는 순간 여기로 와서 아래의 코드를 실행 해
            return render_template('index.html', result='Timeout')# index.html파일을 찾아,엔진속에 있는 result빈칸에 Timeout을 넣어 html으로 반환함
        except subprocess.CalledProcessError:# 파이썬과 커널과 수신을 마쳤는데 그 수신이 CalledProcessError오류라면 아래의 코드로 가
            return render_template('index.html', result='Error')# index.html의 엔진에있는 result를 Error로바꾼 값을 반환함

    return render_template('index.html')#template안에있는 index.html파일을 파이썬과 별개로 독립된 메모리에서 엔진을 거친 후 파일을 반환한다

if __name__ == '__main__': #만일 불려가는 파일이 아닌 직접 실행되는 파일이라면 아래의 코드 실행
    APP.run(host='0.0.0.0', port=8000)#플라스크 운영을 시작하는데, 특정 트레픽이 아닌 어느 주소로 들어오되 8000포트로 들어오게금 만든다 

    # 느낀점:아직 첫 워 게임이라 개념을 얼추 정리했다는 부분에서 왜? 인가를 찾아가며 공부하고 싶었지만 아직 배경 지식이 매우 많이 부족하다는것과, 블랙박스가 있음에도 불구하고 100% 해결을 하지 못하고 넘어갔다는 점에서 후회감을 느겼습니다.
    #       AI 복붙은 일절 하지 않았으며, AI를 오로지 검증의 수단으로 독학을 하며 도구로서, 과외 선생님으로써  질문에 질문에 질문을하며 사용했습니다. 그 부분에 대해서는 뿌듯함을 느겼습니다.
    

