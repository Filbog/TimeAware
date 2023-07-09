const displayChosenActivity = document.querySelector('#displayChosenActivity');
const submitBtn = document.querySelector('#submitBtn');


submitBtn.onclick = () => {
    const selectedOption = activitySelect.options[activitySelect.selectedIndex];
    selectedActivity = selectedOption.textContent;
    displayChosenActivity.style.display = 'block';
    displayChosenActivity.textContent = selectedActivity;
}