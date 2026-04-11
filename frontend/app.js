const form = document.getElementById("travel-form");
const submitBtn = document.getElementById("submit-btn");

const statusBox = document.getElementById("status");
const errorBox = document.getElementById("error");
const resultsBox = document.getElementById("results");
const resultsCaption = document.getElementById("results-caption");

const overviewContent = document.getElementById("overview-content");
const eventsContent = document.getElementById("events-content");
const flightsContent = document.getElementById("flights-content");
const accommodationsContent = document.getElementById("accommodations-content");
const toggleEventsBtn = document.getElementById("toggle-events-btn");

let allEvents = [];
let showAllEvents = false;
let currentEventNote = "";

function escapeHtml(value) {
    if (value === null || value === undefined) return "";
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

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

function setSubmitState(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.textContent = isLoading ? "Analyzing..." : "Analyze trip";
}

function clearResults() {
    resultsBox.classList.add("hidden");
    resultsCaption.textContent = "";
    overviewContent.innerHTML = "";
    eventsContent.innerHTML = "";
    flightsContent.innerHTML = "";
    accommodationsContent.innerHTML = "";
    allEvents = [];
    showAllEvents = false;
    currentEventNote = "";
    toggleEventsBtn.classList.add("hidden");
}

function formatNumber(value, digits = 2) {
    if (value === null || value === undefined || value === "") return "-";

    const parsed = Number(value);
    if (Number.isNaN(parsed)) {
        return String(value);
    }

    return Number.isInteger(parsed) ? String(parsed) : parsed.toFixed(digits);
}

function formatPrice(value) {
    if (value === null || value === undefined || value === "") return "-";

    const parsed = Number(value);
    if (Number.isNaN(parsed)) {
        return escapeHtml(String(value));
    }

    return `€${Number.isInteger(parsed) ? parsed : parsed.toFixed(2)}`;
}

function formatShortDate(value) {
    if (!value) return "-";

    const parsed = new Date(`${value}T00:00:00`);
    if (Number.isNaN(parsed.getTime())) {
        return escapeHtml(String(value));
    }

    return parsed.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    });
}

function getEventSortValue(event) {
    const date = event?.date || "";
    const time = event?.time && event.time !== "-" ? event.time : "00:00:00";

    const parsed = new Date(`${date}T${time}`);
    if (Number.isNaN(parsed.getTime())) {
        return Number.MAX_SAFE_INTEGER;
    }

    return parsed.getTime();
}

function createSummaryCard(label, value, subvalue = "", extraClass = "") {
    return `
        <div class="summary-box ${extraClass}">
            <span class="label">${escapeHtml(label)}</span>
            <div class="value">${value}</div>
            ${subvalue ? `<span class="subvalue">${escapeHtml(subvalue)}</span>` : ""}
        </div>
    `;
}

function createNote(note) {
    if (!note) return "";
    return `
        <div class="note-box">
            <strong>Note:</strong> ${escapeHtml(note)}
        </div>
    `;
}

function createEmptyState(message) {
    return `<div class="empty-state">${escapeHtml(message)}</div>`;
}

function renderOverview(resultData) {
    const events = resultData?.events || [];
    const flights = resultData?.flights_summary;
    const accommodations = resultData?.accommodations_summary;

    overviewContent.innerHTML = [
        createSummaryCard("Destination", escapeHtml(resultData?.city || "-"), "Selected city"),
        createSummaryCard("Date range", `${formatShortDate(resultData?.date_from)} → ${formatShortDate(resultData?.date_to)}`, "","summary-box-compact"),
        createSummaryCard("Events found", escapeHtml(String(events.length)), "Ticketmaster results"),
        createSummaryCard(
            "Cheapest flight",
            flights ? formatPrice(flights.min_price) : "-",
            flights ? `${escapeHtml(formatNumber(flights.count, 0))} options` : "No data"
        ),
        createSummaryCard(
            "Average flight price",
            flights ? formatPrice(flights.avg_price) : "-",
            flights ? `Avg duration ${escapeHtml(formatNumber(flights.avg_duration_minutes))} min` : ""
        ),
        createSummaryCard(
            "Cheapest stay",
            accommodations ? formatPrice(accommodations.min_price_per_stay) : "-",
            accommodations ? `${escapeHtml(formatNumber(accommodations.count, 0))} options` : "No data"
        ),
        createSummaryCard(
            "Average stay price",
            accommodations ? formatPrice(accommodations.avg_price_per_stay) : "-",
            accommodations ? `Avg rating ${escapeHtml(formatNumber(accommodations.avg_rating_score))}` : ""
        ),
    ].join("");
}

function renderFlights(summary, note) {
    if (!summary) {
        flightsContent.innerHTML = createEmptyState("No flight options available.");
        return;
    }

    const cheapestOptions = summary.top_cheapest_options || [];

    const optionCards = cheapestOptions.length
        ? `
            <div class="item-list">
                ${cheapestOptions.map((option) => `
                    <article class="item flight-item">
                        <div class="price-chip">${formatPrice(option.price)}</div>
                        <h3>${escapeHtml(option.departure_city || "-")} → ${escapeHtml(option.destination_city || "-")}</h3>
                        <p><strong>Airports:</strong> ${escapeHtml(option.departure_airport || "-")} → ${escapeHtml(option.arrival_airport || "-")}</p>
                        <p><strong>Duration:</strong> ${escapeHtml(formatNumber(option.duration_minutes))} min</p>
                        <p><strong>Flights per day:</strong> ${escapeHtml(formatNumber(option.flights_per_day, 0))}</p>
                        <p><strong>Flights per week:</strong> ${escapeHtml(formatNumber(option.flights_per_week, 0))}</p>
                    </article>
                `).join("")}
            </div>
        `
        : createEmptyState("No detailed flight options available.");

    flightsContent.innerHTML = `
        ${createNote(note)}

        <div class="summary-grid">
            ${createSummaryCard("Destination", escapeHtml(summary.destination_city || "-"))}
            ${createSummaryCard("Options found", escapeHtml(formatNumber(summary.count, 0)))}
            ${createSummaryCard("Minimum price", formatPrice(summary.min_price))}
            ${createSummaryCard("Average price", formatPrice(summary.avg_price))}
            ${createSummaryCard("Minimum duration", `${escapeHtml(formatNumber(summary.min_duration_minutes))} min`)}
            ${createSummaryCard("Average duration", `${escapeHtml(formatNumber(summary.avg_duration_minutes))} min`)}
        </div>

        <h3 class="subsection-title">Top cheapest options</h3>
        ${optionCards}
    `;
}

function renderAccommodations(summary, note) {
    if (!summary) {
        accommodationsContent.innerHTML = createEmptyState("No accommodation options available.");
        return;
    }

    const cheapestOptions = summary.top_cheapest_options || [];

    const optionCards = cheapestOptions.length
        ? `
            <div class="item-list">
                ${cheapestOptions.map((option) => `
                    <article class="item stay-item">
                        <div class="price-chip">${formatPrice(option.price_per_stay)}</div>
                        <h3>${escapeHtml(option.hotel_name || "-")}</h3>
                        <p><strong>Area:</strong> ${escapeHtml(option.area || "-")}</p>
                        <p><strong>Destination city:</strong> ${escapeHtml(option.destination_city || "-")}</p>
                        <p><strong>Rating:</strong> ${escapeHtml(formatNumber(option.rating_score))}</p>
                        <p><strong>Stars:</strong> ${escapeHtml(formatNumber(option.stars, 0))}</p>
                        <p><strong>Breakfast:</strong> ${escapeHtml(option.breakfast || "-")}</p>
                    </article>
                `).join("")}
            </div>
        `
        : createEmptyState("No detailed accommodation options available.");

    accommodationsContent.innerHTML = `
        ${createNote(note)}

        <div class="summary-grid">
            ${createSummaryCard("Destination", escapeHtml(summary.destination_city || "-"))}
            ${createSummaryCard("Options found", escapeHtml(formatNumber(summary.count, 0)))}
            ${createSummaryCard("Minimum stay price", formatPrice(summary.min_price_per_stay))}
            ${createSummaryCard("Average stay price", formatPrice(summary.avg_price_per_stay))}
            ${createSummaryCard("Average rating", escapeHtml(formatNumber(summary.avg_rating_score)))}
        </div>

        <h3 class="subsection-title">Top cheapest options</h3>
        ${optionCards}
    `;
}

function renderEvents(events, note) {
    allEvents = events || [];
    currentEventNote = note || "";

    const sortedEvents = [...allEvents].sort(
    (a, b) => getEventSortValue(a) - getEventSortValue(b));

    const visibleEvents = showAllEvents ? sortedEvents : sortedEvents.slice(0, 5);

    if (!allEvents.length) {
        eventsContent.innerHTML = `
            ${createNote(currentEventNote)}
            ${createEmptyState("No events found for the selected city and period.")}
        `;
        toggleEventsBtn.classList.add("hidden");
        return;
    }

    eventsContent.innerHTML = `
        ${createNote(currentEventNote)}

        <div class="item-list events-list">
            ${visibleEvents.map((event) => `
                <article class="item event-item">
                    <div class="price-chip">${formatShortDate(event.date)}</div>
                    <h3>${escapeHtml(event.name || "-")}</h3>
                    <p><strong>Time:</strong> ${escapeHtml(event.time || "-")}</p>
                    <p><strong>Venue:</strong> ${escapeHtml(event.venue || "-")}</p>
                    <p><strong>City:</strong> ${escapeHtml(event.city || "-")}</p>
                    ${event.url
                        ? `<a class="link-btn" href="${escapeHtml(event.url)}" target="_blank" rel="noopener noreferrer">Open event</a>`
                        : ""
                    }
                </article>
            `).join("")}
        </div>
    `;

    if (allEvents.length > 5) {
        toggleEventsBtn.classList.remove("hidden");
        toggleEventsBtn.textContent = showAllEvents ? "Show less" : "Show more";
    } else {
        toggleEventsBtn.classList.add("hidden");
    }
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
        await new Promise((resolve) => setTimeout(resolve, 2000));
    }

    throw new Error("Request timed out.");
}

toggleEventsBtn.addEventListener("click", () => {
    showAllEvents = !showAllEvents;
    renderEvents(allEvents, currentEventNote);
});

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
        setSubmitState(true);
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
        resultsCaption.textContent = `${resultData.city || city} | ${formatShortDate(dateFrom)} → ${formatShortDate(dateTo)}`;

        renderOverview(resultData);
        renderFlights(resultData.flights_summary, resultData.notes?.flights);
        renderAccommodations(resultData.accommodations_summary, resultData.notes?.accommodations);
        renderEvents(resultData.events, resultData.notes?.events);

        resultsBox.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
        hideStatus();
        showError(error.message || "Something went wrong.");
    } finally {
        setSubmitState(false);
    }
});