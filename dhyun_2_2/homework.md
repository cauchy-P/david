# 1. Run without Debugging vs Start Debugging
**Run without debugging** (Ctrl+F5) 옵션은 실행속도 향상을 위해 디버거 없이 앱을 실행하게 한다. 통합 터미널(Integrated Terminal)에 결과가 출력된다.

반면 **Start Debugging** (F5) 옵션은 디버거가 프로세스에 붙어서 앱을 실행하는 옵션이다. 중단점(Breakpoint)을 지원하며 변수, 콜 스택, 스레드를 실시간으로 검사할 수 있다. 디버그 콘솔(Debug Console)에 결과가 출력된다.
# 2. Flask는 무엇이며 어떤 역할을 맡는가?
Flask의 공식 문서에 의하면, Flask는 "경량 WSGI 웹 어플리케이션 프레임워크이다".<sup>[1](https://flask.palletsprojects.com/en/stable/)</sup> 문장 그대로 읽으면 어려우니, 단어 하나하나를 정의내린 후 합쳐서 이해해 본다.

*경량(lightweight):* 다른 툴이나 라이브러리를 요구하지 않음.

*WSGI(Web Server Gateway Interface, 위스키라 발음):* 웹서버와 파이썬 앱이 통신하기 위한 프로토콜.<sup>[2](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface)</sup>

*웹 어플리케이션(Web app):* 인터넷 브라우저를 통해 이용할 수 있는 응용 소프트웨어.

*프레임워크(Framework):* 소기의 목적을 달성하거나 복잡한 문제를 해결하고 서술하는 데 사용되는 기본 개념 구조<sup>[3](https://en.wikipedia.org/wiki/Software_framework)</sup>

Flask는 간단한 웹 사이트나 소규모 API, 웹 서비스를 만드는 데에 특화되어 있다.

# 3. 0.0.0.0으로 설정 시 의미와 장단점
## 의미
운영체제의 모든 IP 주소에 대해 "모든 주소에서 들어오는 요청"을 수신하겠다는 뜻이다.
## 장점
단순하다. 동일 프로세스로 인터페이스에 모두 대응할 수 있다.
## 단점
외부에서 접근할 수 있고, 방화벽으로 차단하지 않으면 공개 서비스가 된다.

# 4. 127.0.0.1 접속 vs 내부 IP 접속 차이
| 비교 | 127.0.0.1 | 내부IP |
|--- |  ---        | ---  |
|역할  | 자기 자신에게 트래픽이 돌아옴 | 같은 Subnet의 다른 장치와 통신하기 위한 주소 |
|OSI 계층 | 스위치/라우터 경유 X | 스위치/라우터 경유 |
| 지연 | ~0ms | 실제 네트워크 구간에 따라 달라짐
| 보안 | 외부 노출 없음 | 동일망 사용자는 접근 가능 |

# 5. 포트 번호의 의미와 기본 충돌 시 해결 방안

## 포트의 의미
커뮤니케이션 종단점으로, 프로세스나 네트워크 서비스를 식별하는 논리적 구성물.<sup>[4](https://en.wikipedia.org/wiki/Port_(computer_networking))</sup>
## 포트번호의 의미
각 포트는 포트 번호로 구분되며, 0에서 65535까지의 정수값을 지닌다.


0번에서 1023번까지의 포트번호는 well-known으로 관리자 권한을 필요로 한다.
## 포트 충돌
두 프로세스가 동일 포트를 열려고 할 때 일어난다. 포트 번호를 변경함이 가장 단순한 해결책이다.

