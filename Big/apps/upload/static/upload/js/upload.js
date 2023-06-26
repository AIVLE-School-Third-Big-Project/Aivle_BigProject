function uploadFiles() {
    var input = document.getElementById("files");
    var files = input.files;

    var uploadedFilesDiv = document.getElementById("uploadedFiles");
    uploadedFilesDiv.innerHTML = ""; // 기존 업로드 파일 정보 초기화

    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var fileInfo = document.createElement("p");

        var downloadLink = document.createElement("a");
        downloadLink.href = URL.createObjectURL(file); // 파일 다운로드 URL 생성
        downloadLink.textContent = file.name; // 파일 이름을 링크 텍스트로 설정
        downloadLink.download = file.name; // 다운로드 시 파일명으로 저장
        fileInfo.appendChild(downloadLink);

        uploadedFilesDiv.appendChild(fileInfo);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // 이벤트 핸들러 등록
    var fileInput = document.getElementById("files");
    fileInput.addEventListener("change", uploadFiles);

    var submitBtn = document.getElementById("submit-btn");
    submitBtn.addEventListener("click", function() {
        // 새 창 또는 팝업에서 업로드 파일 목록 표시
        var newWindow = window.open("", "_blank");
        newWindow.document.write("<h1>업로드된 파일 목록</h1>");
        newWindow.document.write(document.getElementById("uploadedFiles").innerHTML);
        newWindow.document.close();
    });
});
