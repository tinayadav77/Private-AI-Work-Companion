let mediaRecorder;
let audioChunks = [];
let currentStream;

function speak(message) {
    if (!message) return;

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(message);
    speech.rate = 1;
    speech.pitch = 1;
    speech.volume = 1;

    window.speechSynthesis.speak(speech);
}

async function startListening() {

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Microphone access is not supported by this browser.");
        return;
    }

    if (mediaRecorder && mediaRecorder.state === "recording") {
        return;
    }

    try {

        currentStream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        audioChunks = [];

        mediaRecorder = new MediaRecorder(currentStream);

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {

            const audioBlob = new Blob(audioChunks, {
                type: "audio/webm"
            });

            const formData = new FormData();

            formData.append(
                "file",
                audioBlob,
                "voice.webm"
            );

            document.getElementById("voiceStatus").textContent =
                "Status: Processing...";

            try {

                const response = await fetch("/voice", {
                    method: "POST",
                    body: formData
                });

                const result = await response.json();

                let reply = "";

if (result.intent === "task") {
    reply = "Got it. I've added that to your tasks.";
}
else if (result.intent === "search") {

    const searchResults =
        document.getElementById("voiceSearchResults");

    if (result.results && result.results.length > 0) {

        const topResult = result.results[0];

        reply =
            `I found ${result.results.length} relevant file` +
            `${result.results.length === 1 ? "" : "s"}. ` +
            `The top match is ${topResult.filename}.`;

        searchResults.innerHTML = "";

        result.results.forEach((item, index) => {

            const percentage =
                (item.similarity * 100).toFixed(0);

            searchResults.innerHTML += `
                <div class="voice-search-result">

                    <div class="voice-search-file">
                        ${index + 1}. ${item.filename}
                    </div>

                    <div class="voice-search-relevance">
                        ${percentage}% relevant
                    </div>

                </div>
            `;
        });

    } else {

        reply =
            "I couldn't find a relevant file in your local workspace.";

        searchResults.innerHTML = `
            <p class="empty">
                No relevant files found.
            </p>
        `;
    }
}
else if (result.intent === "question") {
    reply =
        "I understood that as a question, but I don't have an answer for it yet.";
}
else {
    reply =
        `I heard you say: ${result.text}`;
}

speak(reply);

document.getElementById("voiceStatus").textContent =
    "Status: " + reply;

                document.getElementById("voiceStatus").textContent =
                    "Status: Ready";

            } catch (error) {

                console.error(error);

                alert(
                    "Something went wrong while processing your voice."
                );

                document.getElementById("voiceStatus").textContent =
                    "Status: Error";
            }
        };

        mediaRecorder.start();

        document.getElementById("startVoiceButton").disabled = true;
        document.getElementById("stopVoiceButton").disabled = false;

        document.getElementById("voiceStatus").textContent =
            "Status: Listening...";

    } catch (error) {

        console.error(error);

        alert(
            "Microphone permission was denied or recording failed."
        );
    }
}


function stopListening() {

    if (mediaRecorder && mediaRecorder.state === "recording") {

        mediaRecorder.stop();

        document.getElementById("startVoiceButton").disabled = false;
        document.getElementById("stopVoiceButton").disabled = true;

        document.getElementById("voiceStatus").textContent =
            "Status: Processing...";

        if (currentStream) {

            currentStream
                .getTracks()
                .forEach(track => track.stop());

            currentStream = null;
        }
    }
}


async function findFiles() {

    const query = prompt("What file or topic are you looking for?");

    if (!query) {
        return;
    }

    try {

        const response = await fetch(
            `/search?q=${encodeURIComponent(query)}`
        );

        const data = await response.json();

        if (data.results.length === 0) {
            alert("No relevant files found.");
            return;
        }

        let message = "Top matches:\n\n";

        data.results.forEach((result, index) => {

            message +=
                `${index + 1}. ${result.filename}\n` +
                `Relevance: ${(result.similarity * 100).toFixed(0)}%\n\n`;

        });

        alert(message);

    } catch (error) {

        console.error(error);

        alert("File search failed.");

    }
}
async function loadTasks() {

    try {

        const response = await fetch("/tasks");

        const data = await response.json();

        const taskList = document.getElementById("taskList");

        taskList.innerHTML = "";

        if (data.tasks.length === 0) {

            const emptyMessage = document.createElement("p");

            emptyMessage.className = "empty";
            emptyMessage.textContent = "No tasks yet.";

            taskList.appendChild(emptyMessage);

            return;
        }

        data.tasks.forEach(task => {

            const taskItem = document.createElement("div");

            taskItem.className = "task-item";

            taskItem.textContent =
                `${task.completed ? "✓" : "○"} ${task.task}`;

            taskList.appendChild(taskItem);
        });

    } catch (error) {

        console.error("Failed to load tasks:", error);
    }
}

async function loadActivity() {

    const response = await fetch("/activity");
    const data = await response.json();

    const activities = data.activity;

    const chart = document.getElementById("activityChart");
    const legend = document.getElementById("activityLegend");

    if (activities.length === 0) {
        chart.style.background = "none";
        legend.innerHTML = "<p>No activity recorded yet.</p>";
        return;
    }

    const total = activities.reduce(
        (sum, item) => sum + item.seconds,
        0
    );

    let currentAngle = 0;
   const segments = [];

   activities.forEach(item => {

    const percentage = (item.seconds / total) * 100;

    const startAngle = (currentAngle / 100) * 360;
    const endAngle = ((currentAngle + percentage) / 100) * 360;

    segments.push(
        `#${getCategoryColor(item.category)} ${startAngle}deg ${endAngle}deg`
    );

    currentAngle += percentage;
});

    const focusedActivity = activities.find(
    item => item.category === "Focused Work"
);

const focusedSeconds = focusedActivity
    ? focusedActivity.seconds
    : 0;

const focusPercentage = total > 0
    ? (focusedSeconds / total) * 100
    : 0;

document.getElementById("focusMetric").textContent =
    `Focus: ${focusPercentage.toFixed(0)}%`;

const totalMinutes = total / 60;

let wellnessMessage;

if (totalMinutes < 60) {
    wellnessMessage = "Status: Good";
} else if (totalMinutes < 120) {
    wellnessMessage = "Status: Consider a break";
} else {
    wellnessMessage = "Status: Break recommended";
}

document.getElementById("wellnessMetric").textContent =
    wellnessMessage;

    chart.style.background =
        `conic-gradient(${segments.join(", ")})`;

    legend.innerHTML = "";

    activities.forEach(item => {

        const percentage =
            ((item.seconds / total) * 100).toFixed(0);

        const minutes =
            (item.seconds / 60).toFixed(1);

        legend.innerHTML += `
            <div class="legend-item">
                <span class="legend-dot"
                      style="background:#${getCategoryColor(item.category)}">
                </span>

                <span>
                    <strong>${item.category}</strong>
                    <br>
                    ${minutes} min · ${percentage}%
                </span>
            </div>
        `;
    });
}


function getCategoryColor(category) {

    if (category === "Focused Work") {
        return "4ade80";
    }

    if (category === "Browser") {
        return "60a5fa";
    }

    if (category === "Productivity") {
        return "a78bfa";
    }

    if (category === "Entertainment") {
        return "f472b6";
    }

    return "94a3b8";
}

loadTasks();
loadActivity();