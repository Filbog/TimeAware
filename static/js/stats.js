document.addEventListener("DOMContentLoaded", function() {
    
    const periodInDays = document.getElementById('periodInDays');
    const statisticsData = document.getElementById("statistics-data");
    const addActivityButton = document.getElementById('addActivityButton');
    const generateStatisticsButton = document.getElementById('generateStatisticsButton');
    const maxActivities = 2; // Changed to 2 for maximum two additional activities
    const additionalSelectActivityMenu = document.getElementById('additionalSelectActivityMenu');
    let activityCounter = 1;
    let myChart = null;

    addActivityButton.addEventListener('click', () => {
        if (activityCounter < maxActivities) {
            fetch("/get-activity-options")
                .then(response => response.json())
                .then(data => {
                    console.log(data.activity_options);
                    activityCounter++;
                    const activityOptions = data.activity_options;
                    const additionalSelectMenu = document.createElement('select');
                    additionalSelectMenu.className = 'form-select';
                    additionalSelectMenu.name = 'activity';
                    additionalSelectMenu.id = 'activityName' + activityCounter; // Use activityCounter as part of the ID
                    // additionalSelectMenu.addEventListener("change", fetchStatistics);
    
                    for (const option of activityOptions) {
                            const optionElement = document.createElement('option');
                            optionElement.textContent = option.name;
                            optionElement.className = 'option-' + option.type;
                            additionalSelectMenu.appendChild(optionElement);
                    }
    
                    additionalSelectActivityMenu.appendChild(additionalSelectMenu);
                })
                .catch(error => console.log(error))
        }
    });
    

    generateStatisticsButton.addEventListener('click', () => {
        fetchStatistics();
    });

    function fetchStatistics() {
        const selectedPeriod = periodInDays.value;
    
        // Initialize the array for selected activities
        const allSelectedActivities = [];
    
        // Loop through all additional select menus and add their selected values to the array
        for (let i = 1; i <= activityCounter; i++) {
            const additionalSelectMenu = document.getElementById('activityName' + i);
            allSelectedActivities.push(additionalSelectMenu.value);
        }
    
        fetch(`/get-statistics?activity=${allSelectedActivities.join(',')}&period=${selectedPeriod}`)
            .then(response => response.json())
            .then(data => {
                statisticsData.innerHTML = `
                    <h5>Total duration for the selected period: ${data.total_duration}</h5>
                    <!-- You can include other statistics data here as needed -->
                `;
                console.log(data);
                updateChart(data);
            })
            .catch(error => console.log(error));
    }
    
    
    function updateChart(data) {
        if (myChart) {
            myChart.destroy();
        }
    
        const ctx = document.getElementById("myChart").getContext("2d");
        const labels = Object.keys(data.daily_durations);
        const datasets = [];
    
        // Check if the necessary data properties are present
        if (data.daily_durations && data.activity_names) {
            // Loop through each selected activity and create a dataset for it
            for (let i = 0; i < data.activity_names.length; i++) {
                const activity = data.activity_names[i];
                const dataPoints = labels.map(date => data.daily_durations[date][activity] || 0);
    
                const backgroundColor = i === 0 ? "rgba(54, 162, 235, 0.5)" : "rgba(148, 0, 211, 0.5)";
                const borderColor = i === 0 ? "rgba(54, 162, 235, 1)" : "rgba(148, 0, 211, 1)";
    
                datasets.push({
                    label: activity,
                    data: dataPoints,
                    backgroundColor: backgroundColor,
                    borderColor: borderColor,
                    borderWidth: 1,
                });
            }
        }
    
        myChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: datasets,
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Duration (Seconds)'
                        }
                    },
                },
            },
        });
    }
    
    
    

   
});
