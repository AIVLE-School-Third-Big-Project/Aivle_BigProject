document.addEventListener('DOMContentLoaded', function() {
    // Submit 버튼 클릭 시 실행되는 함수
    function handleFormSubmit(event) {
        event.preventDefault(); // 기본 동작 방지

        // 폼 데이터 가져오기
        var day = document.getElementById('day').value;
        var in_time = document.getElementById('in_time').value;
        var out_time = document.getElementById('out_time').value;
        var start = document.getElementById('start').value;
        var end = document.getElementById('end').value;
        var work_type = document.getElementById('work_type').value;
        var contents = document.getElementById('contents').value;
        

        // json으로 변환
        var jsonData = JSON.stringify({ "day": day, "in_time": in_time, "out_time" : out_time,
                                        "start" : start, "end" : end, "work_type" : work_type, "contents" : contents});

        // AJAX
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "  request/", true);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function() {
            console.log(xhr.readyState, xhr.status)
            if (xhr.readyState === 4) {
                console.log(xhr.responseText)
                var response = JSON.parse(xhr.responseText); // 서버에서 응답한 JSON 파싱

                if (xhr.status === 201) { // DB INSERT 성공
                    console.log("insert success");
                    alert('일지 작성 완료')
                } 
                
                else if (xhr.status === 400) { // DB INSERT 실패
                    console.log("insert failed");

                    // 오류 경고창
                    if (response.message == 'JSON_DECODE_ERROR')
                        alert("JSON DECODE ERROR")
                    else if (response.message == 'TYPE_ERROR') 
                        alert("KEY ERROR");
                    else if (response.message == 'VALUE_ERROR') 
                        alert("VALUE ERROR")
                    
                }
            }
        };
        xhr.send(jsonData);
    }

    // Submit 버튼 클릭 시 handleFormSubmit 함수 실행
    document.getElementById('work-log-wirte-form').addEventListener('submit', handleFormSubmit);
});