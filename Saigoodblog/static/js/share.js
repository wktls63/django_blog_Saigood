// 공유버튼 클릭시에 클립보드로 복사하는 자바스크립트 코드

document.addEventListener("DOMContentLoaded", function () {
    // 공유하기 버튼 클릭 시
    document.getElementById("share_btn").addEventListener("click", function () {
        let postUrl = window.location.href;

        // 클립보드에 복사
        let tempInput = document.createElement("input");
        document.body.appendChild(tempInput);
        tempInput.value = postUrl;
        tempInput.select();
        document.execCommand("copy");
        document.body.removeChild(tempInput);

        // 알림 표시
        alert("포스트 링크가 클립보드에 복사되었습니다");
    });
});