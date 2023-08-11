document.addEventListener("DOMContentLoaded", function() {
    const scrollButton = document.getElementById("scrollToTechnologies");
    const technologiesSection = document.getElementById("technologies");

    scrollButton.addEventListener("click", function() {
        // Calculate the position of the technologies section relative to the viewport
        const rect = technologiesSection.getBoundingClientRect();

        // Scroll to the technologies section with a smooth behavior
        window.scrollTo({
            top: window.scrollY + rect.top,
            behavior: "smooth"
        });
    });
});