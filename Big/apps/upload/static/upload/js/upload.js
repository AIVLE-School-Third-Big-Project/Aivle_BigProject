function handleFileUpload() {
    var input = document.getElementById("files");
    var files = input.files;
    var uploadedFilesDiv = document.getElementById("uploadedFiles");
    uploadedFilesDiv.innerHTML = ""; // 이전에 업로드된 파일 정보 초기화

    if (files.length === 0) {
        var placeholderText = document.createElement("p");
        placeholderText.textContent = "업로드 할 동영상을 선택해주세요 (.mp4)";
        uploadedFilesDiv.appendChild(placeholderText);
    } 
    
    else {
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            var fileName = file.name;

            var fileInfo = document.createElement("p");
            fileInfo.textContent = fileName;

            uploadedFilesDiv.appendChild(fileInfo);
        }
    }
}

document.getElementById("files").addEventListener("change", handleFileUpload);
