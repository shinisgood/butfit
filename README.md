# 버핏서울 기술 문제 
> 수업 예약관리 사이트 구축 & 배포하기


# 요구 사항 명세서

django + DRF 를 사용해서 아래의 요구사항을 구현해 주세요.
요구사항에 정의되지 않는 것들은 자유롭게 구성하시면 됩니다.


## 방법
- 관리자 페이지로 모든 데이터를 등록/수정/삭제 가능해야 합니다.
> 관리자 페이지 생성 완료
- DRF로 1~5번까지의 API를 구현하여 테스트할 수 있는 환경을 제공해 주십시요.(swagger or postman)
> postman invitation 메일로 전달드리겠습니다. 또한 json file로 전달드리겠습니다.
- 구현한 API 기반으로 되도록 많은 케이스의 테스트 코드를 작성해 주십시요. 
> 유저 크레딧 구매 테스트 코드작성
- UI는 구현하지 않으셔도 됩니다.
- 해당 프로젝트의 ReadMe를 작성해 주세요.(관리자사이트에 접근 가능한 아이디와 패스워드 포함)
> 서버 접속하여, git clone까지 해 놓았습니다
> 가상환경 세팅 및 DB구축은 하지 못하였습니다.
- 완료시 main branch에 푸쉬 하시고 완료라는 제목의 @limdongkyu 를 멘션하는 이슈를 하나 등록해 주세요.


## 선택적 과제
- username을 phone_number로 설정하기.

> **USERNAME_FIELD 를 phone_number두고, phone_number 필드를 unique=True 까지 하여 회원가입까지는 완료 
> **하지만 로그인 시 email, password, phone_number 값을 보냈을 때 아래와 같은 에러가 나왔고, 로그인 과정 커스터 마이징을 통해 phone_number을 따로 받아서 처리하면 될 것으로 예상됌. (시간상 스킵)
> {"non_field_errors": [ "Unable to log in with provided credentials."]}

## 과제
1. **수업** 셋탕하기(관리자)

    - 필수 속성
        - 장소, 수업종류, 수업 가격(크레딧), 수업 정원, 수업 날짜, 수업의 시작/종료시간

    
2. **크레딧** 구매 하기(유저)

    - 필수 속성
        - 유저, 크레딧(원), 사용 가능 기간
    - 정책
        - 10만원 미만 1개월
        > **구매 크레딧을 유져의 잔액에 추가 했을 때 그 총액이 10만원 미만이면 사용 가능기간(use_days) 30일

        - 10만원 이상 ~ 20만원 미만 2개월
        > **구매 크레딧을 유져의 잔액에 추가 했을 때 그 총액이 10만원 이상 20만원 미만 이면사용 가능기간(use_days) 60일

        - 20만원 이상 ~ 30만원 미만 3개월
        > - **구매 크레딧을 유져의 잔액에 추가 했을 때 그 총액이 20만원 이상 30만원 미만 이면 사용 가능기간(use_days) 90일

        - 30만원 이상 4개월
        > **구매 크레딧을 유져의 잔액에 추가 했을 때 그 총액이 30만원 이상이면 사용 가능기간(use_days) 120일



3. **수업 예약** 하기(유저)

    - 정책
        - 같은 수업(날짜, 시간, 종류, 장소)에 같은 유저는 중복 예약 불가
        > reservation 테이블 내 course 와 user 을 찾고, is_canceled가 False시 이미 예약한 수업임을 알림(에러처리)



4. 수업 **예약 취소** 하기(유저)

    - 정책(시간기준 X, 날짜 기준)
        - 수업 시작 기준 3일전 크레딧 전액 환불
        > 현재날짜+3일 이 수업날짜보다 클때 전액 환불

        - 수업 시간 기준 1일전 크레딧 50% 환불
        > 현재날짜+1일 이 수업날짜보다 클때 50% 환불

        - 수업 당일 취소 불가
        > **현재날짜가 수업날짜가 동일 할때 환불 불가


5. 수업 **예약 리스트** 보기(유저)

    - 자신이 예약 + 취소 된 리스트를 확인 할수 있고 그에 따른 크레딧 차감 금액과 잔여 크레딧을 확인 할수 있어야 합니다.
    > **is_canceled로 취소&예약 리스트 확인 가능
    > 크래딧 차감 및 잔여 확인 가능



6. 수업 **예약 현황** 보기(관리자 페이지)

    - 특정 기간 별 셋팅한 수업의 예약 현황을 확인할 수 있어야 합니다.
    > -**쿼리 파람스 start_date&end_date로   특정날짜 선택가능

    - 특정 기간 별 셋탕한 수업의 크레딧 차감 금액을 확인할 수 있어야 합니다.
    > **크레딧 차감 금액 확인 가능
    > 특정 날짜의 총 예약 건수, 취소건 수, 실 예약건 수, 총 크레딧 노출

    
## 배포
###구현한 코드 배포하기

    AWS ubuntu 18.04 vm 인스턴스 존재 합니다.
    이메일로 접속 방법 및 pem 파일은 첨부해 드렸습니다.


### 배포시 참고 사항

    필수 사항
    - Webserver: nginx
    - WSGI: gunicorn
    - Python3

    선택 사항
    - Docker
    - DB: PostgreSQL
    - CI/CD
