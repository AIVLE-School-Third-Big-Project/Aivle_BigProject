document.addEventListener('DOMContentLoaded', function() {
    // 공지사항 Submit 버튼 클릭 시 실행되는 함수
    function handleFormSubmit(event) {
        event.preventDefault(); // 기본 동작 방지

        // 폼 데이터 가져오기
        var title = document.getElementById('title').value;
        var content = document.getElementById('content').value;
        var name = document.getElementById('name').value;
        var created = document.getElementById('created').value;
        
        // json으로 변환
        var jsonData = JSON.stringify({ "title": title, "content": content, "name":name, "created": created });

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/main/notice/write/submit/", true);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                var response = JSON.parse(xhr.responseText); // 서버에서 응답한 JSON 파싱
                console.log(xhr.responseText);
                console.log(xhr.readyState, xhr.status);
                
                if (xhr.status === 201) { // 등록 성공시
                    console.log("register success");
                    if (response.redirect_url) {
                        console.log(response.redirect_url); // 파싱한 URL 확인
                        alert("공지사항이 등록되었습니다.");
                        window.location.href = response.redirect_url; // 파싱한 URL로 이동
                    }
                } 
                else if (xhr.status === 400) { // 등록 실패시
                    console.log("register failed");
        
                    // 오류 경고창
                    if (response.message == 'KEY_ERROR') // 입력 칸 X
                        alert("KEY KEY_ERROR");
                    else if (response.message == 'JSON_DECODE_ERROR') // ?가 없을 경우
                        alert("JSON_DECODE_ERROR")       
                }
            }
        };
        xhr.send(jsonData);
    }
    
    // 공지사항 Submit 버튼 클릭 이벤트 등록
    document.getElementById('notice-write').addEventListener('submit', handleFormSubmit);

});