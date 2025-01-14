function playVideo(videoUrl) {
    const videoPopup = window.open(videoUrl, "_blank", "width=800,height=600");
    if (videoPopup) {
        videoPopup.focus();
    } else {
        alert("Pop-ups are blocked! Please allow pop-ups for this site.");
    }
}
