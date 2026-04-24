document.addEventListener("DOMContentLoaded", () => {
    initializeChat();
    initializeAssessment();
    initializeResults();
});

function initializeChat() {
    const toggle = document.getElementById("chat-toggle");
    const panel = document.getElementById("chat-panel");
    const closeButton = document.getElementById("chat-close");
    const form = document.getElementById("chat-form");
    const input = document.getElementById("chat-input");
    const messages = document.getElementById("chat-messages");
    const quickActions = document.querySelectorAll(".quick-action");

    if (!toggle || !panel || !form || !input || !messages) {
        return;
    }

    toggle.addEventListener("click", () => {
        panel.classList.toggle("hidden");
    });

    if (closeButton) {
        closeButton.addEventListener("click", () => {
            panel.classList.add("hidden");
        });
    }

    quickActions.forEach(button => {
        button.addEventListener("click", async () => {
            const message = button.dataset.message;
            await sendChatMessage(message, messages);
        });
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const message = input.value.trim();

        if (!message) {
            return;
        }

        input.value = "";
        await sendChatMessage(message, messages);
    });
}

async function sendChatMessage(message, messagesContainer) {
    appendBubble(messagesContainer, message, "user");

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        let botHtml = escapeHtml(data.response || "I am ready to guide you.");

        if (data.actionUrl && data.actionLabel) {
            botHtml += `<br><a class="chat-action-link" href="${data.actionUrl}">${escapeHtml(data.actionLabel)}</a>`;
        }

        appendBubble(messagesContainer, botHtml, "bot", true);
    } catch (error) {
        appendBubble(messagesContainer, "Something went wrong while contacting LUMEN.", "bot");
    }
}

function appendBubble(container, text, role, isHtml = false) {
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${role}`;

    if (isHtml) {
        bubble.innerHTML = text;
    } else {
        bubble.textContent = text;
    }

    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
}

function initializeAssessment() {
    const form = document.getElementById("assessment-form");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const answers = [];

        for (let i = 1; i <= 10; i += 1) {
            const selected = form.querySelector(`input[name="q${i}"]:checked`);

            if (!selected) {
                alert(`Please answer Question ${i} before continuing.`);
                return;
            }

            answers.push(selected.value);
        }

        try {
            const response = await fetch("/api/assessment", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ answers })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || "Unable to calculate your result.");
                return;
            }

            localStorage.setItem("lumenResult", JSON.stringify(data));
            window.location.href = "/results";
        } catch (error) {
            alert("Something went wrong while calculating your result.");
        }
    });
}

function initializeResults() {
    const resultView = document.getElementById("result-view");

    if (!resultView) {
        return;
    }

    const raw = localStorage.getItem("lumenResult");

    if (!raw) {
        return;
    }

    const data = JSON.parse(raw);

    document.getElementById("primary-title").textContent = `${data.primaryProfile.name}`;
    document.getElementById("primary-tagline").textContent = `${data.primaryProfile.tagline}`;
    document.getElementById("primary-summary").textContent = `${data.primaryProfile.summary}`;

    document.getElementById("secondary-title").textContent = `${data.secondaryProfile.name} — ${data.secondaryProfile.tagline}`;
    document.getElementById("secondary-summary").textContent = `${data.secondaryProfile.summary}`;

    fillList("strength-list", data.primaryProfile.strengths);
    fillList("onboarding-list", data.primaryProfile.onboarding_style);
    fillList("manager-list", data.primaryProfile.manager_tips);
    fillScores(data.scores);
}

function fillList(elementId, items) {
    const target = document.getElementById(elementId);

    if (!target) {
        return;
    }

    target.innerHTML = "";

    items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        target.appendChild(li);
    });
}

function fillScores(scores) {
    const scoreBars = document.getElementById("score-bars");

    if (!scoreBars) {
        return;
    }

    const colors = {
        Red: "#ff5c5c",
        Blue: "#4f8cff",
        Green: "#30c46c",
        Yellow: "#ffc247"
    };

    scoreBars.innerHTML = "";

    Object.entries(scores).forEach(([label, value]) => {
        const row = document.createElement("div");
        row.className = "score-row";

        row.innerHTML = `
            <strong>${label}: ${value}</strong>
            <div class="score-track">
                <div class="score-fill" style="width:${value * 10}%; background:${colors[label]};"></div>
            </div>
        `;

        scoreBars.appendChild(row);
    });
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
