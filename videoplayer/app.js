const episodesList = document.querySelector("#episode-list");
const videoPlayer = document.querySelector("#player");
const subtitles = document.querySelector("#subtitles");
let episodes = {};

fetch("/episodes.json")
  .then(async res => {
    episodes = await res.json();
    const episodeNodes = episodes.map(episode => {
      const option = document.createElement("option");
      option.appendChild(document.createTextNode(episode));
      return option;
    });
    episodeNodes.forEach(element => episodesList.appendChild(element), this);
  });

videoPlayer.setAttribute("src", "videos/House.Of.Cards.S01E01.720p.BluRay.x265.mp4");
subtitles.setAttribute("src", "videos/subtitles/HOC.S01E01.vtt");

function playPause() {
  if(videoPlayer.paused || videoPlayer.ended)
    videoPlayer.play();
  else
    videoPlayer.pause();
}

function goFullScreen() {
  if (videoPlayer.requestFullscreen)
    videoPlayer.requestFullscreen();
  else
    videoPlayer.webkitRequestFullscreen(); // Damn it Chrome
}