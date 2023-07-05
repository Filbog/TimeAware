let stopwatchInterval;
let selectedActivity = '';
let startTime;
let endTime;
let duration = 0;
let seconds = 0;
let minutes = 0;
let hours = 0;

const startBtn = document.querySelector('#start');
const finishBtn = document.querySelector('#finish');
const pauseBtn = document.querySelector('#pause');

// Hide the pause and finish buttons initially
pauseBtn.style.display = 'none';
finishBtn.style.display = 'none'

const activitySelect = document.querySelector('#activityToTrack');
const chosenActivity = document.querySelector('#chosenActivity');

let appendSeconds = document.querySelector('#seconds');
let appendMinutes = document.querySelector('#minutes');
let appendHours = document.querySelector('#hours');


function getStartTime() { 
    startTime = Date.now();
    startTime = new Date(startTime);    
    startTime = startTime.toLocaleString();

}

function finishStopwatch() {
    // getting the end time
    endTime = Date.now();
    endTime = new Date(endTime);    
    endTime = endTime.toLocaleString();

    const data = {
        duration: duration,
        startTime: startTime,
        endTime: endTime,
        activity: selectedActivity
    }
    
}

const updateStopwatch = () => {
    duration++;
    seconds++;
    if(seconds < 60){
        appendSeconds.innerHTML = String(seconds).padStart(2, '0')
    } else {
        seconds = 0;
        appendSeconds.innerHTML = String(seconds).padStart(2, '0')
        minutes++;
        
    }

    if(minutes < 60){
        appendMinutes.innerHTML = String(minutes).padStart(2, '0');
    } else {
        minutes = 0;
        hours ++;
        appendHours.innerHTML = String(hours).padStart(2, '0');
    }

}

startBtn.onclick = () => {
    if(duration === 0){
        getStartTime();
    }
    //hiding the dropdown and showing only the chosen activity
    selectedActivity = activitySelect.value;
    chosenActivity.textContent = selectedActivity;
    activitySelect.style.display = 'none';
    chosenActivity.style.display = 'block';

    //show/hide buttons
    pauseBtn.style.display = 'inline-block';
    finishBtn.style.display = 'inline-block';
    startBtn.style.display = 'none';

    // actually starting/re-starting the timer
    clearInterval(stopwatchInterval)
    stopwatchInterval = setInterval(updateStopwatch, 1000);
}

pauseBtn.onclick = () => {
    clearInterval(stopwatchInterval)

    //show/hide buttons
    startBtn.style.display = 'inline-block';
    pauseBtn.style.display = 'none';
}

finishBtn.onclick = () => {
    finishStopwatch();
    clearInterval(stopwatchInterval)
    console.log(duration)
}

