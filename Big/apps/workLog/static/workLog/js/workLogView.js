document.addEventListener("DOMContentLoaded", function() {
    // 게시글 삭제
    function deleteBoard() {
        if (confirm("정말로 삭제하시겠습니까?")) {
            var xhr = new XMLHttpRequest();
            var board_id = document.getElementById("delete-btn").getAttribute("data-board-id");
            var csrfToken = getCookie('csrftoken');
            
            xhr.open("POST", "/main/workLog/view/delete/" + board_id + "/");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.setRequestHeader('X-CSRFToken', csrfToken);

            xhr.onload = function() {
                if (xhr.status === 204)  // 삭제 성공
                    location.href = "/main/workLog/";
                else { // 삭제 실패
                    alert("이미 삭제된 게시글 입니다");
                }
            };
            xhr.send();
        }
    }


    document.getElementById("delete-btn").addEventListener("click", deleteBoard);
});