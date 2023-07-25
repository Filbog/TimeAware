const deleteActivityBtn = document.getElementById("deleteActivityBtn");
const selectActivity = document.getElementById("select-activity");

deleteActivityBtn.addEventListener("click", () => {
    const selectedActivity = selectActivity.value;
    if (!selectedActivity) {
        alert("Please select an activity to delete.");
        return;
    }

    const confirmation = confirm(
        `Are you sure you want to delete the activity: ${selectedActivity}?`
    );

    if (confirmation) {
        fetch(`/delete-activity/${selectedActivity}`, { method: "POST" })
            .then((response) => response.json())
            .then((data) => {
                alert(data.message); // Show a success message from Flask
                window.location.reload(); // Refresh the page after deletion
            })
            .catch((error) => {
                console.error("Error deleting activity:", error);
                alert("An error occurred while deleting the activity.");
            });
    }
});