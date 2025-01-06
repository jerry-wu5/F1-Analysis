// document.addEventListener("DOMContentLoaded", () => {
//     const yearDropdown = document.getElementById("year-dropdown");
//     const raceDropdown = document.getElementById("race-dropdown");
//     const viewAnimationButton = document.getElementById("view-animation");

//     yearDropdown.addEventListener("change", async () => {
//         const year = yearDropdown.value;
//         if (!year) return;

//         const response = await fetch(`/get-races?year=${year}`);
//         const races = await response.json();

//         // Populate race dropdown
//         raceDropdown.innerHTML = '<option value="">-- Select a Race --</option>';
//         races.forEach(race => {
//             const option = document.createElement("option");
//             option.value = race.raceId;
//             option.textContent = race.name;
//             raceDropdown.appendChild(option);
//         });
//     });

//     viewAnimationButton.addEventListener("click", () => {
//         const raceId = raceDropdown.value;
//         if (!raceId) {
//             alert("Please select a race.");
//             return;
//         }
//         window.location.href = `/animate?raceId=${raceId}`;
//     });
// });

document.addEventListener("DOMContentLoaded", () => {
    const yearDropdown = document.getElementById("year-dropdown");
    const raceDropdown = document.getElementById("race-dropdown");
    const viewAnimationButton = document.getElementById("view-animation");

    yearDropdown.addEventListener("change", async () => {
        const year = yearDropdown.value;
        if (!year) return;

        const response = await fetch(`/get-races?year=${year}`);
        const races = await response.json();

        // Populate race dropdown
        raceDropdown.innerHTML = '<option value="">-- Select a Race --</option>';
        races.forEach(race => {
            const option = document.createElement("option");
            option.value = race.raceId;
            option.textContent = race.name;
            raceDropdown.appendChild(option);
        });
    });

    viewAnimationButton.addEventListener("click", () => {
        const raceId = raceDropdown.value;
        if (!raceId) {
            alert("Please select a race.");
            return;
        }
        window.location.href = `/animate?raceId=${raceId}`;
    });
});
