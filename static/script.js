// Fetch prediction
// TODO

// Functions for animations
// TODO

// Functions for showing the music on the DOM
// TODO
const play_btn = document.querySelector("#play");
const prev_btn = document.querySelector("#pre");
const next_btn = document.querySelector("#next");
const title = document.querySelector("#title");
const artist = document.querySelector("#artist")
const slider = document.querySelector("#slider");
const song = document.querySelector("#song");

let is_playing = true;
let song_index = 0;


function play_pause() {
    if (playing) {
        play.src = "../static/img/pause.png"
        song.play();
        playing = false;
    } else {
        play.src = "../static/img/play.png"
        song.pause();
        playing = true;
    }
}

function next_song() {
    song_index++;
    if (song_index < 0) {
        song_index = 1;
    };
    song.src = songs[song_index];
    artist = artist[song_index];
    title = title[song_index];
    playing = true;
    play_pause();
}

function updateProgressValue() {
    slider.max = song.duration;
    slider.value = song.currentTime;
    document.querySelector('.currentTime').innerHTML = (formatTime(Math.floor(song.currentTime)));
    if (document.querySelector('.durationTime').innerHTML === "NaN:NaN") {
        document.querySelector('.durationTime').innerHTML = "0:00";
    } else {
        document.querySelector('.durationTime').innerHTML = (formatTime(Math.floor(song.duration)));
    }
};

setInterval(updateProgressValue, 500);

function change_progress_bar() {
    song.currentTime = progressBar.value;
}