from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

QUESTIONS = [
    {
        "id": 1,
        "question": "When you start a new role, what feels most natural to you?",
        "options": [
            {"text": "Take action quickly and figure things out while moving.", "color": "Red"},
            {"text": "Understand the process and details before acting.", "color": "Blue"},
            {"text": "Get comfortable with the people and team rhythm first.", "color": "Green"},
            {"text": "Explore ideas, possibilities, and the bigger picture.", "color": "Yellow"}
        ]
    },
    {
        "id": 2,
        "question": "In a team setting, what role do you often play?",
        "options": [
            {"text": "The one who pushes things forward.", "color": "Red"},
            {"text": "The one who checks quality and accuracy.", "color": "Blue"},
            {"text": "The one who keeps harmony and supports others.", "color": "Green"},
            {"text": "The one who energizes people and brings enthusiasm.", "color": "Yellow"}
        ]
    },
    {
        "id": 3,
        "question": "How do you usually handle pressure?",
        "options": [
            {"text": "Move faster and take control.", "color": "Red"},
            {"text": "Slow down and analyze the facts.", "color": "Blue"},
            {"text": "Stay calm and work steadily.", "color": "Green"},
            {"text": "Talk it through and stay optimistic.", "color": "Yellow"}
        ]
    },
    {
        "id": 4,
        "question": "What kind of work environment helps you most?",
        "options": [
            {"text": "Fast-paced with clear targets.", "color": "Red"},
            {"text": "Structured with clear expectations.", "color": "Blue"},
            {"text": "Stable, supportive, and collaborative.", "color": "Green"},
            {"text": "Creative, social, and flexible.", "color": "Yellow"}
        ]
    },
    {
        "id": 5,
        "question": "What matters most when making decisions?",
        "options": [
            {"text": "Speed and results.", "color": "Red"},
            {"text": "Logic and evidence.", "color": "Blue"},
            {"text": "People impact and consistency.", "color": "Green"},
            {"text": "Vision and possibilities.", "color": "Yellow"}
        ]
    },
    {
        "id": 6,
        "question": "How do you prefer to communicate?",
        "options": [
            {"text": "Direct and concise.", "color": "Red"},
            {"text": "Clear, precise, and detailed.", "color": "Blue"},
            {"text": "Warm, calm, and supportive.", "color": "Green"},
            {"text": "Friendly, expressive, and energetic.", "color": "Yellow"}
        ]
    },
    {
        "id": 7,
        "question": "What motivates you the most in a new company?",
        "options": [
            {"text": "Ambitious goals and progress.", "color": "Red"},
            {"text": "Competence, mastery, and clarity.", "color": "Blue"},
            {"text": "Belonging and reliability.", "color": "Green"},
            {"text": "Inspiration and people connection.", "color": "Yellow"}
        ]
    },
    {
        "id": 8,
        "question": "When solving a problem, what do you usually do first?",
        "options": [
            {"text": "Take immediate action.", "color": "Red"},
            {"text": "Break the problem down carefully.", "color": "Blue"},
            {"text": "Ask who is affected and what support is needed.", "color": "Green"},
            {"text": "Brainstorm several possible approaches.", "color": "Yellow"}
        ]
    },
    {
        "id": 9,
        "question": "How do you prefer to learn during onboarding?",
        "options": [
            {"text": "By doing real tasks quickly.", "color": "Red"},
            {"text": "With documentation and structured training.", "color": "Blue"},
            {"text": "With guided support and practical repetition.", "color": "Green"},
            {"text": "With interactive sessions and engaging discussions.", "color": "Yellow"}
        ]
    },
    {
        "id": 10,
        "question": "What kind of first impression from a company helps you trust it?",
        "options": [
            {"text": "Confidence, direction, and strong leadership.", "color": "Red"},
            {"text": "Professionalism, detail, and competence.", "color": "Blue"},
            {"text": "Care, consistency, and human warmth.", "color": "Green"},
            {"text": "Energy, inspiration, and vision.", "color": "Yellow"}
        ]
    }
]

PROFILES = {
    "Red": {
        "name": "Red Driver",
        "tagline": "Action-Oriented, Direct, Decisive",
        "summary": "You are energized by momentum, challenge, and visible progress. You usually prefer clarity, speed, and practical next steps.",
        "strengths": [
            "Takes initiative quickly",
            "Comfortable making decisions",
            "Focuses on outcomes",
            "Handles pressure with urgency"
        ],
        "onboarding_style": [
            "Fast start with clear goals",
            "Immediate ownership of practical tasks",
            "Visible milestones and outcomes",
            "Short, direct communication"
        ],
        "manager_tips": [
            "Be concise and outcome-focused",
            "Give ownership early",
            "Set clear targets",
            "Avoid unnecessary delays"
        ],
        "accent": "#ff5c5c"
    },
    "Blue": {
        "name": "Blue Analyst",
        "tagline": "Logical, Accurate, Structured",
        "summary": "You value clarity, logic, and strong systems. You usually perform best when expectations, standards, and processes are well explained.",
        "strengths": [
            "Strong attention to detail",
            "Thinks carefully before acting",
            "Values quality and precision",
            "Learns well through structure"
        ],
        "onboarding_style": [
            "Clear documentation and process walkthroughs",
            "Structured training modules",
            "Defined success criteria",
            "Time to understand tools and systems"
        ],
        "manager_tips": [
            "Provide context and documentation",
            "Explain the why behind decisions",
            "Avoid vague expectations",
            "Respect careful thinking"
        ],
        "accent": "#4f8cff"
    },
    "Green": {
        "name": "Green Supporter",
        "tagline": "Steady, Supportive, Reliable",
        "summary": "You are often calm, dependable, and people-aware. You tend to thrive in environments with trust, consistency, and thoughtful support.",
        "strengths": [
            "Reliable and steady",
            "Strong team awareness",
            "Patient and consistent",
            "Creates stability in groups"
        ],
        "onboarding_style": [
            "Supportive guidance and check-ins",
            "Clear routine and steady pacing",
            "Human-centered team introductions",
            "Safe environment for learning"
        ],
        "manager_tips": [
            "Create a calm onboarding rhythm",
            "Encourage questions",
            "Offer reassurance and consistency",
            "Help build relationships early"
        ],
        "accent": "#30c46c"
    },
    "Yellow": {
        "name": "Yellow Influencer",
        "tagline": "Energetic, Expressive, Vision-Led",
        "summary": "You are often motivated by inspiration, people, and possibility. You usually enjoy engaging environments, collaborative energy, and future-focused thinking.",
        "strengths": [
            "Brings energy to teams",
            "Communicates openly",
            "Naturally enthusiastic",
            "Sees creative possibilities"
        ],
        "onboarding_style": [
            "Interactive and engaging sessions",
            "Visual, people-centered onboarding",
            "Inspiring brand and mission context",
            "Space for ideas and discussion"
        ],
        "manager_tips": [
            "Keep communication engaging",
            "Connect tasks to the bigger vision",
            "Use collaborative sessions",
            "Channel enthusiasm into action"
        ],
        "accent": "#ffc247"
    }
}

NAVIGATION_HINTS = {
    "assessment": ("/assessment", "Start Assessment"),
    "about": ("/about", "Open About"),
    "pathways": ("/pathways", "View Pathways"),
    "results": ("/results", "View Results"),
    "home": ("/", "Go Home")
}


def calculate_result(answer_colors):
    scores = {"Red": 0, "Blue": 0, "Green": 0, "Yellow": 0}

    for color in answer_colors:
        if color in scores:
            scores[color] += 1

    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    primary_color = ordered[0][0]
    secondary_color = ordered[1][0]

    primary_profile = PROFILES[primary_color]
    secondary_profile = PROFILES[secondary_color]

    return {
        "primaryColor": primary_color,
        "secondaryColor": secondary_color,
        "primaryProfile": primary_profile,
        "secondaryProfile": secondary_profile,
        "scores": scores
    }


def build_chat_response(message):
    normalized = message.lower().strip()

    if any(term in normalized for term in ["start", "assessment", "questions", "quiz"]):
        return {
            "response": "I can guide you into the 10-question LUMEN profile assessment. It helps place candidates into one of four communication and onboarding style groups.",
            "actionLabel": NAVIGATION_HINTS["assessment"][1],
            "actionUrl": NAVIGATION_HINTS["assessment"][0]
        }

    if "lumen" in normalized:
        return {
            "response": "LUMEN is the main onboarding experience. It helps candidates and employees move through guided questions, onboarding pathways, and next steps in a more intentional way.",
            "actionLabel": NAVIGATION_HINTS["about"][1],
            "actionUrl": NAVIGATION_HINTS["about"][0]
        }

    if "avian" in normalized or "security" in normalized:
        return {
            "response": "AVIAN is the structured intelligence and security side of the platform. In this concept, it supports guided interpretation, trust, and controlled workflow logic behind the onboarding experience.",
            "actionLabel": NAVIGATION_HINTS["about"][1],
            "actionUrl": NAVIGATION_HINTS["about"][0]
        }

    if any(term in normalized for term in ["color", "profile", "personality", "group"]):
        return {
            "response": "The platform uses four color groups: Red Driver, Blue Analyst, Green Supporter, and Yellow Influencer. These are meant to guide communication and onboarding style, not act as a final hiring decision system.",
            "actionLabel": NAVIGATION_HINTS["pathways"][1],
            "actionUrl": NAVIGATION_HINTS["pathways"][0]
        }

    if any(term in normalized for term in ["results", "my result"]):
        return {
            "response": "If you have already finished the assessment, your results page will show your primary color, secondary color, score breakdown, strengths, and best onboarding style.",
            "actionLabel": NAVIGATION_HINTS["results"][1],
            "actionUrl": NAVIGATION_HINTS["results"][0]
        }

    if any(term in normalized for term in ["path", "pathway", "onboarding"]):
        return {
            "response": "The pathways section explains how each color group may prefer to learn, communicate, and move through onboarding. It is designed as a practical onboarding support tool.",
            "actionLabel": NAVIGATION_HINTS["pathways"][1],
            "actionUrl": NAVIGATION_HINTS["pathways"][0]
        }

    if any(term in normalized for term in ["hello", "hi", "hey"]):
        return {
            "response": "Welcome to LUMEN. I can help you start the assessment, explain AVIAN, show the onboarding pathways, or guide you to your results.",
            "actionLabel": NAVIGATION_HINTS["assessment"][1],
            "actionUrl": NAVIGATION_HINTS["assessment"][0]
        }

    return {
        "response": "I can help you start the assessment, explain LUMEN or AVIAN, show the four color groups, or guide you to the onboarding pathways.",
        "actionLabel": NAVIGATION_HINTS["home"][1],
        "actionUrl": NAVIGATION_HINTS["home"][0]
    }


@app.route("/")
def home():
    return render_template("index.html", title="LUMEN | Onboarding Portal")


@app.route("/assessment")
def assessment():
    return render_template("assessment.html", title="Assessment | LUMEN", questions=QUESTIONS)


@app.route("/results")
def results():
    return render_template("results.html", title="Results | LUMEN")


@app.route("/about")
def about():
    return render_template("about.html", title="About | LUMEN")


@app.route("/pathways")
def pathways():
    return render_template("pathways.html", title="Pathways | LUMEN", profiles=PROFILES)


@app.route("/api/assessment", methods=["POST"])
def api_assessment():
    payload = request.get_json(silent=True) or {}
    answers = payload.get("answers", [])

    if len(answers) != 10:
        return jsonify({"error": "Please answer all 10 questions."}), 400

    result = calculate_result(answers)
    return jsonify(result)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "").strip()

    if not message:
        return jsonify({"response": "Please enter a message so I can guide you.", "actionLabel": "", "actionUrl": ""}), 400

    response = build_chat_response(message)
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
