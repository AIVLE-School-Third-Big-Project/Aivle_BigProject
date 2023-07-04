console.log("일단 js들어왔음")
const video = document.querySelector('.viewer');
const timeElements = document.querySelectorAll('.time');
const logItems = document.querySelectorAll('.logItem');

timeElements.forEach((timeElement) => {
    timeElement.addEventListener('click', (event) => {
      // 클릭된 시간을 가져옴
        const clickedTime = event.target.textContent;
      
      // 이벤트 동작
        console.log('클릭된 시간:', clickedTime);

        video.currentTime = parseInt(clickedTime)*1;

    });
});

