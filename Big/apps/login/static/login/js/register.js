document.addEventListener('DOMContentLoaded', function() {
    // 회원가입 Submit 버튼 클릭 시 실행되는 함수
    function handleFormSubmit(event) {
        event.preventDefault(); // 기본 동작 방지

        // 폼 데이터 가져오기
        var name = document.getElementById('name').value;
        var id = document.getElementById('id').value;
        var pw = document.getElementById('pw').value;
        var pwVerify = document.getElementById('pw-verify').value
        var region = document.getElementById('region').value;
        var category = document.getElementById('category').value;

        var csrfToken = getCookie('csrftoken');

        // json으로 변환
        var jsonData = JSON.stringify({"name": name, "id": id, "pw": pw, "pw-verify":pwVerify, 
                                        "region": region, "category": category });

        // AJAX
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/register/submit/", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader('X-CSRFToken', csrfToken);

        xhr.onreadystatechange = function() {
            // console.log(xhr.readyState, xhr.status)
            
            if (xhr.readyState === 4) {
                console.log(xhr.responseText)
                var response = JSON.parse(xhr.responseText); // 서버에서 응답한 JSON 파싱

                if (xhr.status === 201) { // 로그인 성공시
                    console.log("register success");
                    
                    if(response.redirect_url) {
                        alert('가입이 완료되었습니다')
                        window.location.href = response.redirect_url; // 파싱한 URL로 이동
                    }
                } 
                
                else if (xhr.status === 400) { // 회원가입 실패시
                    console.log("register failed");

                    // 오류 경고창
                    if (response.message == 'INVALID_PASSWORD') // 비밀번호 오류
                        alert("패스워드는 8글자 이상 25글자 이하 입니다")
                    else if (response.message == 'INVALID_PASSWORD_VERIFY') // 비밀번호 확인 일치 X
                        alert("비밀번호 확인이 일치하지 않습니다")
                    else if (response.message == 'KEY_ERROR') // 입력 칸 X
                        alert("KEY KEY_ERROR");
                    else if (response.message == 'JSON_DECODE_ERROR') // ID가 없을 경우
                        alert("JSON_DECODE_ERROR")       
                }
            }
        };
        xhr.send(jsonData);
    }
    // 회원가입 Submit 버튼 클릭 이벤트 등록
    document.getElementById('register-form').addEventListener('submit', handleFormSubmit);

    // 아이디 중복 검사
    function checkIdDuplication() {
        var id = document.getElementById('id').value;
        var csrfToken = getCookie('csrftoken');

        var jsonData = JSON.stringify({ "id": id });

        // AJAX
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/register/id_inspection/", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader('X-CSRFToken', csrfToken);

        xhr.onreadystatechange = function() {
            // console.log(xhr.readyState, xhr.status)

            if (xhr.readyState === 4) {
                console.log(xhr.responseText)
                var response = JSON.parse(xhr.responseText);

                // 중복 ID 없음
                if (xhr.status == 201 && response.message == 'SUCCESS') {
                    // 아이디 에러 텍스트칸 
                    document.getElementById('id-error').style.color = 'green';
                    document.getElementById('id-error').textContent = '사용가능';

                    document.getElementById('register-submit').disabled = false; // 회원가입 버튼 활성화
                    document.getElementById('id').disabled = true; // 아이디 입력칸 비활성화
                }

                // 중복 ID 있음
                else if (xhr.status == 400 && response.message == 'ALREADY_EXISTS') 
                    document.getElementById('id-error').textContent = '이미 사용 중인 아이디입니다';
            }
        };
        
        xhr.send(jsonData);
    }
    
    // 아이디 중복검사 버튼 클릭 시 이벤트 리스너 등록
    document.getElementById('check-id-btn').addEventListener('click', checkIdDuplication);


    // 비밀번호 일치 여부 확인 함수
    var passwordField = document.getElementById('pw');
    var passwordVerifyField = document.getElementById('pw-verify');

    // 입력 필드 변경 시 실시간 비밀번호 일치 여부 확인
    passwordField.addEventListener('input', validatePasswordMatch);
    passwordVerifyField.addEventListener('input', validatePasswordMatch);

    // 비밀번호, 비밀번호 확인
    function validatePasswordMatch() {

        var password = passwordField.value;
        var passwordVerify = passwordVerifyField.value;

        if (password === passwordVerify) {
            passwordField.style.borderColor = 'blue';
            passwordVerifyField.style.borderColor = 'blue';
            document.getElementById('pw-error').textContent = '';
        } 
        
        else {
            passwordField.style.borderColor = 'red';
            passwordVerifyField.style.borderColor = 'red';
            document.getElementById('pw-error').textContent = '비밀번호가 일치하지 않습니다';
        }
    }
    
});