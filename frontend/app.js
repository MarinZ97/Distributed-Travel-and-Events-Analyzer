const form = document.getElementById("travel-form");
const statusBox = document.getElementById("status");
const errorBox = document.getElementById("error");
const resultsBox = document.getElementById("results");

const eventsContent = document.getElementById("events-content");
const flightsContent = document.getElementById("flights-content");
const accommodationsContent = document.getElementById("accommodations-content");

function showStatus(message) {
    statusBox.textContent = message;
    statusBox.classList.remove("hidden");
}

function hideStatus() {
    statusBox.classList.add("hidden");
    statusBox.textContent = "";
}

function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
}

function hideError() {
    errorBox.classList.add("hidden");
    errorBox.textContent = "";
}

function clearResults() {
    resultsBox.classList.add("hidden");
    eventsContent.innerHTML = "";
    flightsContent.innerHTML = "";
    accommodationsContent.innerHTML = "";
}

function formatNumber(value) {
    if (value === null || value === undefined) return "-";
    return value;
}

function renderEvents(events) {
    if (!events || events.length === 0) {
        eventsContent.innerHTML = "<p>No events found for the selected city and period.</p>";
        return;
    }

    const items = events.map(event => `
        <div class="item">
            <h3>${event.name}</h3>
            <p><strong>Date:</strong> ${event.date || "-"}</p>
            <p><strong>Time:</strong> ${event.time || "-"}</p>
            <p><strong>Venue:</strong> ${event.venue || "-"}</p>
            <p><strong>City:</strong> ${event.city || "-"}</p>
            <p><a href="${event.url}" target="_blank" rel="noopener noreferrer">Open event</a></p>
        </div>
    `).join("");

    eventsContent.innerHTML = `<div class="item-list">${items}</div>`;
}

function renderFlights(summary) {
    if (!summary) {
        flightsContent.innerHTML = "<p>No flight options available.</p>";
        return;
    }

    const cheapest = (summary.top_cheapest_options || []).map(option => `
        <div class="item">
            <h3>${option.departure_city} → ${option.destination_city}</h3>
            <p><strong>Airports:</strong> ${option.departure_airport} → ${option.arrival_airport}</p>
            <p><strong>Price:</strong> ${option.price}</p>
            <p><strong>Duration:</strong> ${option.duration_minutes} min</p>
            <p><strong>Flights per day:</strong> ${option.flights_per_day}</p>
            <p><strong>Flights per week:</strong> ${option.flights_per_week}</p>
        </div>
    `).join("");

    flightsContent.innerHTML = `
        <div class="summary-grid">
            <div class="summary-box">
                <strong>Destination city</strong>
                ${summary.destination_city}
            </div>
            <div class="summary-box">
                <strong>Options found</strong>
                ${formatNumber(summary.count)}
            </div>
            <div class="summary-box">
                <strong>Min price</strong>
                ${formatNumber(summary.min_price)}
            </div>
            <div class="summary-box">
                <strong>Average price</strong>
                ${formatNumber(summary.avg_price)}
            </div>
            <div class="summary-box">
                <strong>Min duration</strong>
                ${formatNumber(summary.min_duration_minutes)} min
            </div>
            <div class="summary-box">
                <strong>Average duration</strong>
                ${formatNumber(summary.avg_duration_minutes)} min
            </div>
        </div>

        <h3>Top cheapest options</h3>
        <div class="item-list">${cheapest || "<p>No flight options found.</p>"}</div>
    `;
}

function renderAccommodations(summary) {
    if (!summary) {
        accommodationsContent.innerHTML = "<p>No accommodation options available.</p>";
        return;
    }

    const cheapest = (summary.top_cheapest_options || []).map(option => `
        <div class="item">
            <h3>${option.hotel_name}</h3>
            <p><strong>City:</strong> ${option.destination_city}</p>
            <p><strong>Area:</strong> ${option.area || "-"}</p>
            <p><strong>Price per stay:</strong> ${option.price_per_stay}</p>
            <p><strong>Rating:</strong> ${option.rating_score ?? "-"}</p>
            <p><strong>Stars:</strong> ${option.stars ?? "-"}</p>
            <p><strong>Breakfast:</strong> ${option.breakfast || "-"}</p>
        </div>
    `).join("");

    accommodationsContent.innerHTML = `
        <div class="summary-grid">
            <div class="summary-box">
                <strong>Destination city</strong>
                ${summary.destination_city}
            </div>
            <div class="summary-box">
                <strong>Options found</strong>
                ${formatNumber(summary.count)}
            </div>
            <div class="summary-box">
                <strong>Min price per stay</strong>
                ${formatNumber(summary.min_price_per_stay)}
            </div>
            <div class="summary-box">
                <strong>Average price per stay</strong>
                ${formatNumber(summary.avg_price_per_stay)}
            </div>
            <div class="summary-box">
                <strong>Average rating</strong>
                ${formatNumber(summary.avg_rating_score)}
            </div>
        </div>

        <h3>Top cheapest options</h3>
        <div class="item-list">${cheapest || "<p>No accommodation options found.</p>"}</div>
    `;
}

async function pollJob(jobId) {
    const maxAttempts = 60;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
        const statusResponse = await fetch(`/api/requests/${jobId}`);
        if (!statusResponse.ok) {
            throw new Error("Failed to fetch job status.");
        }

        const statusData = await statusResponse.json();

        if (statusData.status === "DONE") {
            const resultResponse = await fetch(`/api/requests/${jobId}/result`);
            if (!resultResponse.ok) {
                throw new Error("Failed to fetch job result.");
            }

            const resultData = await resultResponse.json();
            return resultData.result ?? resultData;
        }

        if (statusData.status === "FAILURE") {
            throw new Error("Request processing failed.");
        }

        showStatus(`Processing request... (${statusData.status})`);
        await new Promise(resolve => setTimeout(resolve, 2000));
    }

    throw new Error("Request timed out.");
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    hideError();
    clearResults();

    const city = document.getElementById("city").value.trim();
    const dateFrom = document.getElementById("date_from").value;
    const dateTo = document.getElementById("date_to").value;

    if (!city || !dateFrom || !dateTo) {
        showError("Please fill in all fields.");
        return;
    }

    if (dateFrom > dateTo) {
        showError("Date from must be earlier than or equal to date to.");
        return;
    }

    try {
        showStatus("Submitting request...");

        const response = await fetch("/api/requests", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                city: city,
                date_from: dateFrom,
                date_to: dateTo,
            }),
        });

        if (!response.ok) {
            throw new Error("Failed to create request.");
        }

        const data = await response.json();
        const resultData = await pollJob(data.job_id);

        hideStatus();
        resultsBox.classList.remove("hidden");

        renderEvents(resultData.events);
        renderFlights(resultData.flights_summary);
        renderAccommodations(resultData.accommodations_summary);
    } catch (error) {
        hideStatus();
        showError(error.message || "Something went wrong.");
    }
});