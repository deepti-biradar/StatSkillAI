import streamlit as st
from google import genai
from google.genai import types
import json
import os
import base64
from datetime import datetime


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="StatSkill AI",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# FIND BACKGROUND IMAGE AUTOMATICALLY
# ============================================================

def find_background():

    possible_files = [
        "background.jpg",
        "background.jpeg",
        "background.png",
        "bg.jpg",
        "bg.jpeg",
        "bg.png"
    ]

    for filename in possible_files:

        if os.path.exists(filename):
            return filename

    # Also look for any image in the folder
    for filename in os.listdir("."):

        if filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):

            return filename

    return None


background_file = find_background()


# ============================================================
# CUSTOM UI
# ============================================================

if background_file:

    with open(
        background_file,
        "rb"
    ) as f:

        image_data = base64.b64encode(
            f.read()
        ).decode()

    extension = background_file.lower().split(".")[-1]

    if extension == "jpg":
        mime_type = "image/jpeg"
    elif extension == "jpeg":
        mime_type = "image/jpeg"
    else:
        mime_type = "image/png"


    st.markdown(
        f"""
        <style>

        /* =========================================
           FULL PAGE BACKGROUND
        ========================================= */

        [data-testid="stAppViewContainer"] {{

            background-image:
                linear-gradient(
                    rgba(255, 185, 220, 0.38),
                    rgba(255, 150, 205, 0.38)
                ),
                url("data:{mime_type};base64,{image_data}");

            background-size: cover !important;

            background-position:
                center center !important;

            background-attachment:
                fixed !important;

            min-height: 100vh;
        }}


        /* =========================================
           REMOVE DEFAULT WHITE BACKGROUND
        ========================================= */

        [data-testid="stAppViewContainer"]
        .main {{

            background:
                transparent !important;
        }}


        [data-testid="stAppViewContainer"]
        .block-container {{

            background:
                transparent !important;

            padding-top:
                2rem !important;

            padding-bottom:
                3rem !important;
        }}


        /* =========================================
           TOP STREAMLIT HEADER
        ========================================= */

        [data-testid="stHeader"] {{

            background:
                rgba(255,255,255,0.15) !important;

            backdrop-filter:
                blur(10px);
        }}


        /* =========================================
           GLASS DASHBOARD SECTIONS
        ========================================= */

        [data-testid="stVerticalBlockBorderWrapper"] {{

            background:
                rgba(255,255,255,0.72) !important;

            border-radius:
                24px !important;

            border:
                1px solid
                rgba(255,255,255,0.8) !important;

            box-shadow:
                0 10px 35px
                rgba(160,50,120,0.15) !important;

            backdrop-filter:
                blur(14px);
        }}


        /* =========================================
           METRIC CARDS
        ========================================= */

        div[data-testid="metric-container"] {{

            background:
                rgba(255,255,255,0.82) !important;

            border-radius:
                20px !important;

            padding:
                18px !important;

            border:
                1px solid
                rgba(255,255,255,0.9) !important;

            box-shadow:
                0 8px 25px
                rgba(180,60,130,0.15) !important;

            backdrop-filter:
                blur(12px);
        }}


        /* =========================================
           SIDEBAR
        ========================================= */

        section[data-testid="stSidebar"] {{

            background:
                linear-gradient(
                    180deg,
                    rgba(112,45,100,0.96),
                    rgba(190,65,135,0.93)
                ) !important;

            box-shadow:
                5px 0 30px
                rgba(80,20,60,0.25);
        }}


        section[data-testid="stSidebar"] * {{

            color:
                white !important;
        }}


        /* =========================================
           TITLE
        ========================================= */

        h1 {{

            color:
                #8c155f !important;

            font-weight:
                900 !important;

            text-shadow:
                0 2px 10px
                rgba(255,255,255,0.7);
        }}


        h2 {{

            color:
                #941766 !important;

            font-weight:
                800 !important;
        }}


        h3 {{

            color:
                #a21d70 !important;

            font-weight:
                750 !important;
        }}


        /* =========================================
           BUTTONS
        ========================================= */

        .stButton > button {{

            background:
                linear-gradient(
                    135deg,
                    #ff4fa3,
                    #9b5cff
                ) !important;

            color:
                white !important;

            border:
                none !important;

            border-radius:
                14px !important;

            font-weight:
                700 !important;

            padding:
                0.65rem 1.3rem !important;

            box-shadow:
                0 6px 18px
                rgba(190,60,140,0.25);

            transition:
                0.2s ease;
        }}


        .stButton > button:hover {{

            transform:
                translateY(-2px);

            box-shadow:
                0 10px 25px
                rgba(190,60,140,0.35);
        }}


        /* =========================================
           INPUTS
        ========================================= */

        textarea,
        input {{

            background:
                rgba(255,255,255,0.82) !important;

            border-radius:
                14px !important;

            border:
                1px solid
                rgba(220,90,170,0.25) !important;
        }}


        div[data-baseweb="select"] > div {{

            background:
                rgba(255,255,255,0.85) !important;

            border-radius:
                14px !important;
        }}


        /* =========================================
           ALERTS
        ========================================= */

        div[data-testid="stAlert"] {{

            border-radius:
                16px !important;

            backdrop-filter:
                blur(10px);
        }}


        /* =========================================
           DIVIDERS
        ========================================= */

        hr {{

            border:
                none !important;

            border-top:
                1px solid
                rgba(150,40,110,0.15) !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

else:

    st.warning(
        "⚠️ No background image found. "
        "Put a JPG or PNG image in the same folder as app.py."
    )


# ============================================================
# GEMINI
# ============================================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL = "gemini-3.5-flash-lite"

PROGRESS_FILE = "progress.json"


# ============================================================
# PROGRESS FUNCTIONS
# ============================================================

def load_progress():

    if not os.path.exists(
        PROGRESS_FILE
    ):
        return []

    try:

        with open(
            PROGRESS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return []


def save_progress(history):

    with open(
        PROGRESS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            indent=4
        )


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:

    st.session_state.history = (
        load_progress()
    )


if "questions" not in st.session_state:

    st.session_state.questions = None


if "evaluation" not in st.session_state:

    st.session_state.evaluation = None


if "learning_path" not in st.session_state:

    st.session_state.learning_path = None


if "assessment_skill" not in st.session_state:

    st.session_state.assessment_skill = None


if "assessment_level" not in st.session_state:

    st.session_state.assessment_level = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 📊 StatSkill AI"
    )

    st.caption(
        "Learn • Assess • Grow"
    )

    st.divider()

    st.header(
        "🎯 Assessment Setup"
    )

    skill = st.selectbox(
        "What skill do you want to assess?",
        [
            "Python",
            "Machine Learning",
            "Data Structures",
            "Artificial Intelligence",
            "SQL",
            "Cybersecurity",
            "Communication"
        ]
    )

    level = st.selectbox(
        "Your current level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.divider()

    st.caption(
        "✨ Small progress every day "
        "leads to big results."
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "📊 StatSkill AI"
)

st.subheader(
    "Adaptive Competency & Learning Platform"
)

st.write(
    "Assess your skills. Get personalized feedback. "
    "Learn, improve, and reassess."
)


# ============================================================
# DASHBOARD
# ============================================================

st.header(
    "🎓 Student Dashboard"
)

history = st.session_state.history


if not history:

    st.info(
        "👋 Complete your first assessment "
        "to start building your competency profile."
    )

else:

    all_scores = [
        float(item["score"])
        for item in history
    ]

    average_score = (
        sum(all_scores)
        / len(all_scores)
    )

    best_score = max(
        all_scores
    )

    latest = history[-1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📋 Assessments",
            len(history)
        )

    with col2:

        st.metric(
            "⭐ Average Score",
            f"{average_score:.1f}/10"
        )

    with col3:

        st.metric(
            "🏆 Best Score",
            f"{best_score:.1f}/10"
        )

    with col4:

        st.metric(
            "🎯 Current Level",
            latest.get(
                "level",
                "Unknown"
            )
        )


    # ========================================================
    # SKILLS
    # ========================================================

    st.subheader(
        "🧠 Skill Overview"
    )

    skills = {}

    for item in history:

        item_skill = item["skill"]

        item_score = float(
            item["score"]
        )

        if item_skill not in skills:

            skills[item_skill] = []

        skills[item_skill].append(
            item_score
        )


    columns = st.columns(
        min(
            max(len(skills), 1),
            4
        )
    )


    for index, (
        skill_name,
        scores
    ) in enumerate(
        skills.items()
    ):

        with columns[
            index % len(columns)
        ]:

            latest_score = scores[-1]

            if latest_score >= 8.5:

                status = "🏆 Advanced"

            elif latest_score >= 7:

                status = "🚀 Strong"

            elif latest_score >= 5:

                status = "📈 Developing"

            else:

                status = "🌱 Needs Practice"


            st.metric(
                skill_name,
                f"{latest_score:.1f}/10"
            )

            st.caption(
                status
            )


    # ========================================================
    # OVERALL PROGRESS
    # ========================================================

    st.subheader(
        "📈 Overall Progress"
    )

    chart_scores = [
        float(item["score"])
        for item in history
    ]

    chart_data = {

        "Assessment":
            list(
                range(
                    1,
                    len(chart_scores) + 1
                )
            ),

        "Score":
            chart_scores
    }

    st.line_chart(
        chart_data,
        x="Assessment",
        y="Score"
    )


# ============================================================
# ASSESSMENT
# ============================================================

st.divider()

st.header(
    "📝 Competency Assessment"
)


# ============================================================
# PREVIOUS SCORE
# ============================================================

skill_history = [

    item

    for item
    in st.session_state.history

    if item["skill"] == skill
]


previous_score = None


if skill_history:

    previous_score = float(
        skill_history[-1]["score"]
    )


# ============================================================
# DIFFICULTY
# ============================================================

def get_difficulty(
    score,
    selected_level
):

    if score is None:

        return selected_level

    if score < 3:

        return "Very Basic"

    elif score < 5:

        return "Foundational"

    elif score < 7:

        return "Intermediate"

    elif score < 8.5:

        return "Advanced Application"

    else:

        return "Challenging"


difficulty = get_difficulty(
    previous_score,
    level
)


if previous_score is not None:

    st.info(
        f"🧠 Previous {skill} score: "
        f"**{previous_score}/10**  | "
        f"Next difficulty: "
        f"**{difficulty}**"
    )

else:

    st.info(
        f"🆕 First {skill} assessment — "
        f"starting at **{level}** level."
    )


# ============================================================
# GENERATE ASSESSMENT
# ============================================================

if st.button(
    "✨ Generate Adaptive Assessment"
):

    if previous_score is None:

        difficulty_instruction = f"""
This is the student's first assessment.

Use the selected level:
{level}
"""

    else:

        difficulty_instruction = f"""
The student previously scored:
{previous_score}/10.

Adapt the next assessment to this performance.

Difficulty:
{difficulty}

Do not repeat previous questions.
"""


    prompt = f"""
Create an adaptive competency assessment.

Skill:
{skill}

Student level:
{level}

{difficulty_instruction}

Create exactly 3 questions.

Question 1:
Test conceptual understanding.

Question 2:
Test practical application.

Question 3:
Test reasoning or problem solving.

Rules:
- Questions must be relevant to {skill}.
- Questions must match the difficulty.
- Do not provide answers.
- Keep questions clear.
- Do not repeat previous questions.

Return only the questions.
"""


    try:

        response = client.models.generate_content(

            model=MODEL,

            contents=prompt
        )

        st.session_state.questions = (
            response.text
        )

        st.session_state.assessment_skill = (
            skill
        )

        st.session_state.assessment_level = (
            level
        )

        st.session_state.evaluation = None

        st.session_state.learning_path = None


    except Exception as e:

        st.error(
            "Could not generate assessment."
        )

        st.code(
            str(e)
        )


# ============================================================
# QUESTIONS
# ============================================================

if st.session_state.questions:

    st.divider()

    st.header(
        "📝 Your Adaptive Assessment"
    )

    st.write(
        st.session_state.questions
    )

    st.subheader(
        "✍️ Your Answers"
    )

    answer1 = st.text_area(
        "Answer to Q1",
        key="answer1"
    )

    answer2 = st.text_area(
        "Answer to Q2",
        key="answer2"
    )

    answer3 = st.text_area(
        "Answer to Q3",
        key="answer3"
    )


    # ========================================================
    # EVALUATE
    # ========================================================

    if st.button(
        "🔍 Evaluate My Competency"
    ):

        evaluation_prompt = f"""
You are a strict but fair competency evaluator.

Skill:
{st.session_state.assessment_skill}

Student level:
{st.session_state.assessment_level}

Assessment:
{st.session_state.questions}

Student Answer 1:
{answer1}

Student Answer 2:
{answer2}

Student Answer 3:
{answer3}

Evaluate only what the student demonstrated.

Rules:
- Score from 0 to 10.
- Give partial credit when appropriate.
- Do not assume knowledge not demonstrated.
- Do not give credit for incorrect answers.
- Do not change or revise the score.
- Do not show internal reasoning.
- Be objective.
- Identify strengths.
- Identify weaknesses.
- Recommend next topics.

Return ONLY valid JSON:

{{
    "score": 0,
    "competency_level": "Beginner",
    "strengths": [
        "strength 1"
    ],
    "weaknesses": [
        "weakness 1"
    ],
    "next_topics": [
        "topic 1",
        "topic 2",
        "topic 3"
    ],
    "explanation": "Short explanation."
}}

Score must be between 0 and 10.
"""


        try:

            response = client.models.generate_content(

                model=MODEL,

                contents=evaluation_prompt,

                config=types.GenerateContentConfig(

                    response_mime_type=
                    "application/json"
                )
            )


            raw = response.text.strip()


            if raw.startswith("```"):

                raw = raw.replace(
                    "```json",
                    ""
                )

                raw = raw.replace(
                    "```",
                    ""
                )

                raw = raw.strip()


            evaluation = json.loads(
                raw
            )


            score = float(
                evaluation.get(
                    "score",
                    0
                )
            )


            score = max(
                0,
                min(
                    10,
                    score
                )
            )


            evaluation["score"] = score


            st.session_state.evaluation = (
                evaluation
            )


            # =================================================
            # SAVE PROGRESS
            # =================================================

            new_record = {

                "skill":
                    st.session_state.assessment_skill,

                "score":
                    score,

                "level":
                    evaluation.get(
                        "competency_level",
                        "Unknown"
                    ),

                "timestamp":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
            }


            st.session_state.history.append(
                new_record
            )


            save_progress(
                st.session_state.history
            )


        except Exception as e:

            st.error(
                "Could not evaluate the answers."
            )

            st.code(
                str(e)
            )


# ============================================================
# REPORT
# ============================================================

if st.session_state.evaluation:

    evaluation = (
        st.session_state.evaluation
    )

    st.divider()

    st.header(
        "📊 Your Competency Report"
    )


    score = evaluation[
        "score"
    ]

    competency = evaluation.get(
        "competency_level",
        "Unknown"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "📊 Score",
            f"{score}/10"
        )


    with col2:

        st.metric(
            "🎯 Competency Level",
            competency
        )


    with col3:

        current_history = [

            item

            for item
            in st.session_state.history

            if item["skill"]
            == st.session_state.assessment_skill
        ]


        if len(current_history) > 1:

            previous = float(
                current_history[-2]["score"]
            )

            change = (
                score - previous
            )

            st.metric(
                "📈 Change",
                f"{change:+.1f}"
            )

        else:

            st.metric(
                "📋 Assessments",
                1
            )


    st.subheader(
        "💪 Strengths"
    )

    for strength in evaluation.get(
        "strengths",
        []
    ):

        st.success(
            strength
        )


    st.subheader(
        "⚠️ Areas to Improve"
    )

    for weakness in evaluation.get(
        "weaknesses",
        []
    ):

        st.warning(
            weakness
        )


    st.subheader(
        "📚 Recommended Next Topics"
    )

    for topic in evaluation.get(
        "next_topics",
        []
    ):

        st.write(
            "➡️",
            topic
        )


    st.subheader(
        "📝 Evaluation"
    )

    st.write(
        evaluation.get(
            "explanation",
            "No explanation provided."
        )
    )


# ============================================================
# LEARNING PATH
# ============================================================

if st.session_state.evaluation:

    st.divider()

    st.header(
        "🚀 Personalized Learning Path"
    )


    if st.button(
        "✨ Generate My Learning Path"
    ):

        evaluation = (
            st.session_state.evaluation
        )


        learning_prompt = f"""
Create a personalized learning path.

Skill:
{st.session_state.assessment_skill}

Competency:
{evaluation.get("competency_level")}

Score:
{evaluation.get("score")}/10

Strengths:
{evaluation.get("strengths")}

Weaknesses:
{evaluation.get("weaknesses")}

Recommended topics:
{evaluation.get("next_topics")}

Create a practical learning plan.

Include:

1. Priority areas
2. Topics in learning order
3. What to learn
4. One practical exercise for each topic
5. A milestone for reaching the next level

Keep it concise and actionable.
"""


        try:

            response = client.models.generate_content(

                model=MODEL,

                contents=learning_prompt
            )


            st.session_state.learning_path = (
                response.text
            )


        except Exception as e:

            st.error(
                "Could not generate learning path."
            )

            st.code(
                str(e)
            )


    if st.session_state.learning_path:

        st.write(
            st.session_state.learning_path
        )


# ============================================================
# RESET
# ============================================================

st.divider()

if st.button(
    "🔄 Start Fresh Assessment"
):

    st.session_state.questions = None

    st.session_state.evaluation = None

    st.session_state.learning_path = None

    st.session_state.assessment_skill = None

    st.session_state.assessment_level = None

    st.rerun()