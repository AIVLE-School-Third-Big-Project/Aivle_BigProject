document.addEventListener('DOMContentLoaded', function() {
    // Submit 버튼 클릭 시 실행되는 함수
    function handleFormSubmit(event) {
        event.preventDefault(); // 기본 동작 방지

        // 폼 데이터 가져오기
        var id = document.getElementById('id').value;
        var pw = document.getElementById('pw').value;

        // json으로 변환
        var jsonData = JSON.stringify({ "id": id, "pw": pw });
        var csrfToken = getCookie('csrftoken');

        // AJAX
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/login/submit/", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader('X-CSRFToken', csrfToken);

        xhr.onreadystatechange = function() {
            // console.log(xhr.readyState, xhr.status)
            if (xhr.readyState === 4) {
                // console.log(xhr.responseText)
                var response = JSON.parse(xhr.responseText); // 서버에서 응답한 JSON 파싱

                if (xhr.status === 201) { // 로그인 성공시
                    console.log("login success");
                    
                    if(response.redirect_url) {
                        window.location.href = response.redirect_url; // 파싱한 URL로 이동
                    }
                } 
                
                else if (xhr.status >= 400) { // 로그인 실패시
                    console.log("login failed");

                    // 오류 경고창
                    if (response.message == 'INVALID_PASSWORD') // 비밀번호 오류
                        alert("잘못된 패스워드 입니다.\n" + response.count + "회 실패")
                    else if (response.message == 'KEY_ERROR') 
                        alert("KEY ERROR");
                    else if (response.message == 'VALUE_ERROR') 
                        alert("사번은 숫자로 입력해주세요.");
                    else if (response.message == 'USER_NOT_FOUND') // ID가 없을 경우
                        alert("없는 ID 입니다.")
                    else if (response.message == 'ACCOUNT_LOCKED') // ID가 없을 경우
                        alert("5회 이상 비밀번호 입력 실패로 계정이 잠겼습니다.\n잠시 후 다시 시도해주세요.")
                    
                }
            }
        };
        xhr.send(jsonData);
    }

    // Submit 버튼 클릭 시 handleFormSubmit 함수 실행
    document.getElementById('login-form').addEventListener('submit', handleFormSubmit);
});
