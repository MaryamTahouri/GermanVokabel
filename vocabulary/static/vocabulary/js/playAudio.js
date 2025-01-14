function playAudio(audioUrl) {
    if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.play()
            .then(() => console.log("Audio is playing:", audioUrl))
            .catch((error) => console.error("Error playing audio:", error));
    } else {
        console.error("No audio file provided.");
    }
}
