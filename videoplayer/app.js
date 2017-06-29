const episodesList = document.querySelector("#episode-list");
const videoPlayer = document.querySelector("#player");
const subtitles = document.querySelector("#subtitles");
const skipButton = document.querySelector("#skipIntro");
const progressIndicator = document.querySelector("#progressIndicator");
let episodes = {};

let metadata = {};
let duration = 0;

loadEpisodeInfo("/ep1.json");

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

videoPlayer.addEventListener("loadedmetadata", videoMetaData => {
  const videoDuration = document.querySelector("#videoDuration");

  duration = videoMetaData.srcElement.duration;
  videoDuration.innerHTML = formatSeconds(duration);
  addProgressBarHighlight(metadata.intro, duration);
});

videoPlayer.addEventListener("timeupdate", event => {
  const currentTime = document.querySelector("#currentTime");

  const timestamp = convertMsToSeconds(event.timeStamp);
  currentTime.innerHTML = formatSeconds(timestamp);
  const deltaToStart = timestamp - parseInt(metadata.intro.start);
  const deltaToEnd = timestamp - parseInt(metadata.intro.end);
  if (deltaToStart > 0 && deltaToStart < 5) {
    skipButton.style.opacity = 1;
  }
  else if (deltaToEnd > 0 && deltaToEnd < 5) {
    skipButton.style.opacity = 0;
  }

  progressIndicator.style.left = String(100 * timestamp / videoPlayer.duration).replace(",", ".") + "%";
  console.log(String(100 * timestamp / videoPlayer.duration) + "%");

});

skipButton.addEventListener("click", () => {
  videoPlayer.currentTime = parseInt(metadata.intro.end);
  skipButton.style.opacity = 0;
});

function loadEpisodeInfo(episodeJSONPath) {
  fetch(episodeJSONPath)
    .then(async res => {
      const episodeInfo = await res.json();

      videoPlayer.setAttribute("src", episodeInfo.src);
      subtitles.setAttribute("src", episodeInfo.subtitles);
      metadata = episodeInfo;
    });
}

function addProgressBarHighlight(highlightTimestamps, totalDuration) {
  const progressBarHighlights = document.querySelector("#progress-bar-highlights");
  const highlight = document.createElement("span");
  highlight.style.width = String(Math.round(((parseInt(highlightTimestamps.end) - parseInt(highlightTimestamps.start)) / totalDuration) * 100)) + "%";
  highlight.style.left = String(Math.round(100 * parseInt(highlightTimestamps.start) / totalDuration)) + "%";
  progressBarHighlights.appendChild(highlight);
}

function convertMsToSeconds(timeInMs) {
  return Math.floor(timeInMs / 1000);
}

function formatSeconds(timeInSec) {
  const date = new Date(null);
  date.setSeconds(timeInSec);
  return date.toISOString().substr(11, 8);
}

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