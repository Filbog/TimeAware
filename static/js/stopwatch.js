let stopwatchInterval;
let selectedActivity;
let activityId;
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
finishBtn.style.display = 'none';

const displayChosenActivity = document.querySelector('#displayChosenActivity');
const activitySelect = document.querySelector('#activityToTrack');

let appendSeconds = document.querySelector('#seconds');
let appendMinutes = document.querySelector('#minutes');
let appendHours = document.querySelector('#hours');


function getStartTime() { 
    startTime = Date.now();
    startTime = new Date(startTime);    
    startTime = startTime.toISOString().slice(0, 19).replace('T', ' ');

}

function finishStopwatch() {
    // getting the end time
    endTime = Date.now();
    endTime = new Date(endTime);    
    endTime = endTime.toISOString().slice(0, 19).replace('T', ' ');

    const data = {
        duration: duration,
        start_time: startTime,
        end_time: endTime,
        activity: selectedActivity,
        user_activity_id: activityId
    };

    // fetch('/save-tracked-activity-data', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify(data)
    // })
    // .then(function(response) {
    //     if (response.ok) {
    //         console.log('Data sent successfully');
    //         return response.text()
    //     } else {
    //         console.error('Error sending data:', response.status);
    //         throw new Error('Error sending data');
    //     }   
    // })
    // .then(function(data){
    //     // console.log('Response:', data)
    //     // location.reload();
    // })
    // .catch(function(error) {
    //     // Handle the error
    //     console.error('An error occurred:', error)
    // });
    //set values to a sneaky form
    document.getElementById("durationInput").value = duration;
    document.getElementById("activityInput").value = selectedActivity;
    document.getElementById("startTimeInput").value = startTime;
    document.getElementById("endTimeInput").value = endTime;
    document.getElementById("userActivityIdInput").value = activityId;
    console.log(endTime)
    console.log(startTime)

    // Submit the form, this line basically "click" on the hidden 'submit' button upon finishing the count
    document.getElementById("submitFormButton").click();
    
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
    const selectedOption = activitySelect.options[activitySelect.selectedIndex];
    selectedActivity = selectedOption.textContent;
    activityId = selectedOption.value;
    displayChosenActivity.textContent = selectedActivity;
    displayChosenActivity.style.display = 'block';
    activitySelect.style.display = 'none';

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
}

