document.addEventListener("DOMContentLoaded", function() {
    // 파일 트리 노드를 접기/펼치기 위한 이벤트 핸들러 추가
    var nodes = document.querySelectorAll(".node");
    for (var i = 0; i < nodes.length; i++) {
        nodes[i].addEventListener("click", toggleNode);
    }
});

function toggleNode(event) {
    // 클릭한 노드의 자식 노드를 토글
    event.stopPropagation();
    var node = event.currentTarget;
    var children = node.querySelectorAll(".node");
    for (var i = 0; i < children.length; i++) {
        if (children[i].style.display === "none") {
            children[i].style.display = "block";
        } else {
            children[i].style.display = "none";
        }
    }
}
