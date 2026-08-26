import streamlit as st

from core.nexus_engine import NexusEngine
from core.history_manager import HistoryManager


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NEXUS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(76, 0, 255, 0.15),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(0, 200, 255, 0.10),
                transparent 25%
            ),
            #090b12;
        color: #f5f7ff;
    }

    /* Hide default Streamlit clutter */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Main content spacing */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }

    /* Hero */

    .nexus-brand {
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: 0.18em;
        margin-bottom: 0;
        background:
            linear-gradient(
                90deg,
                #ffffff,
                #9bb8ff,
                #a97cff
            );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .nexus-subtitle {
        color: #8f98b3;
        font-size: 1rem;
        letter-spacing: 0.12em;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
    }

    /* Glass cards */

    .glass-card {
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.07),
                rgba(255,255,255,0.025)
            );
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 18px;
        padding: 1.4rem;
        backdrop-filter: blur(12px);
        box-shadow:
            0 12px 40px
            rgba(0,0,0,0.25);
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #dce4ff;
        margin-bottom: 0.8rem;
    }

    /* Metrics */

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 1rem;
        border-radius: 16px;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 2rem;
    }

    /* Buttons */

    .stButton > button {
        border-radius: 12px;
        border: 1px solid
            rgba(155, 184, 255, 0.35);
        background:
            linear-gradient(
                135deg,
                #5f72ff,
                #8b5cff
            );
        color: white;
        font-weight: 700;
        min-height: 48px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 8px 30px
            rgba(100,100,255,0.35);
    }

    /* Inputs */

    textarea,
    input {
        border-radius: 12px !important;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0c0f19,
                #090b12
            );
        border-right:
            1px solid
            rgba(255,255,255,0.06);
    }

    /* Divider */

    hr {
        border-color:
            rgba(255,255,255,0.08);
    }

    /* Expander */

    details {
        background:
            rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 0.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "report" not in st.session_state:
    st.session_state.report = None

if "page" not in st.session_state:
    st.session_state.page = "Investigate"


# ============================================================
# ENGINES
# ============================================================

nexus = NexusEngine()
history = HistoryManager()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:2rem;
            font-weight:800;
            letter-spacing:0.12em;
        ">
        ⚡ NEXUS
        </div>

        <div style="
            color:#7f89a5;
            font-size:0.75rem;
            letter-spacing:0.08em;
            margin-bottom:1.5rem;
        ">
        INCIDENT INTELLIGENCE SYSTEM
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    if st.button(
        "🔍 Investigate",
        use_container_width=True,
    ):
        st.session_state.page = "Investigate"

    if st.button(
        "📜 Incident History",
        use_container_width=True,
    ):
        st.session_state.page = "History"

    if st.button(
        "⚔️ Compare Incidents",
        use_container_width=True,
    ):
        st.session_state.page = "Compare"

    st.divider()

    st.markdown(
        """
        <div style="
            color:#626b84;
            font-size:0.75rem;
            line-height:1.6;
        ">
        NEXUS analyzes incident context,
        evidence, severity, probable causes,
        timelines and investigation confidence.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# INVESTIGATION PAGE
# ============================================================

if st.session_state.page == "Investigate":

    st.markdown(
        """
        <div class="nexus-brand">
        NEXUS
        </div>

        <div class="nexus-subtitle">
        INCIDENT INTELLIGENCE • EVIDENCE-DRIVEN INVESTIGATION
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="glass-card">
        <div class="section-title">
        NEW INVESTIGATION
        </div>
        """,
        unsafe_allow_html=True,
    )

    description = st.text_area(
        "Describe the incident",
        height=170,
        placeholder=(
            "Example: After the latest deployment, "
            "users are unable to log in. The server "
            "shows database connection errors..."
        ),
    )

    col1, col2 = st.columns(2)

    with col1:

        system = st.text_input(
            "Affected system",
            placeholder="Production API",
        )

    with col2:

        environment = st.selectbox(
            "Environment",
            [
                "",
                "Development",
                "Staging",
                "Production",
            ],
        )

    logs = st.text_area(
        "Technical logs or error context (optional)",
        height=130,
        placeholder=(
            "Paste logs, error messages, stack traces "
            "or technical observations..."
        ),
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "⚡ INVESTIGATE INCIDENT",
        use_container_width=True,
    ):

        if not description.strip():

            st.warning(
                "Please describe the incident first."
            )

        else:

            with st.spinner(
                "NEXUS is analyzing incident intelligence..."
            ):

                report = nexus.investigate(
                    description=description,
                    system=system,
                    environment=environment,
                    logs=logs,
                )

                st.session_state.report = report

                history.add_incident(
                    report
                )

            st.success(
                "Investigation completed."
            )


    # ========================================================
    # REPORT DISPLAY
    # ========================================================

    report = st.session_state.report

    if report:

        st.markdown("---")

        severity = report["severity"]
        confidence = report["confidence"]
        incident = report["incident"]

        st.markdown(
            """
            <div class="section-title">
            INVESTIGATION OVERVIEW
            </div>
            """,
            unsafe_allow_html=True,
        )

        metric1, metric2, metric3, metric4 = (
            st.columns(4)
        )

        with metric1:

            st.metric(
                "SEVERITY",
                severity["severity_level"],
                f"{severity['severity_score']}/100",
            )

        with metric2:

            st.metric(
                "CONFIDENCE",
                confidence["confidence_level"],
                f"{confidence['confidence_score']}/100",
            )

        with metric3:

            st.metric(
                "INCIDENT TYPE",
                incident["incident_type"],
            )

        with metric4:

            st.metric(
                "EVIDENCE",
                report["evidence"][
                    "evidence_count"
                ],
            )

        st.markdown("### Executive Intelligence")

        st.markdown(
            f"""
            <div class="glass-card">
            {report["summary"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        left, right = st.columns(2)

        # ----------------------------------------------------
        # PROBABLE CAUSES
        # ----------------------------------------------------

        with left:

            st.markdown(
                "### 🧠 Probable Causes"
            )

            for cause in report[
                "causes"
            ][
                "probable_causes"
            ]:

                with st.expander(
                    f"{cause['confidence']} — "
                    f"{cause['cause']}"
                ):

                    st.write(
                        "**Evidence:** "
                        + ", ".join(
                            cause["evidence"]
                        )
                    )

                    st.write(
                        "**Investigation:** "
                        + cause["investigation"]
                    )

        # ----------------------------------------------------
        # TIMELINE
        # ----------------------------------------------------

        with right:

            st.markdown(
                "### 🕒 Incident Timeline"
            )

            for index, event in enumerate(
                report["timeline"]["timeline"],
                start=1,
            ):

                st.markdown(
                    f"""
                    <div class="glass-card">
                    <b>{index:02d}</b>
                    &nbsp;&nbsp;
                    {event["event"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # ----------------------------------------------------
        # ACTIONS
        # ----------------------------------------------------

        st.markdown(
            "### ⚡ Recommended Actions"
        )

        for action in report[
            "actions"
        ][
            "recommended_actions"
        ]:

            st.markdown(
                f"""
                <div class="glass-card">
                <b>P{action['priority']}</b>
                &nbsp;&nbsp;
                <b>{action['type']}</b>
                <br><br>
                {action['action']}
                <br><br>
                <span style="
                    color:#8b94ad;
                    font-size:0.9rem;
                ">
                {action['reason']}
                </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        st.markdown(
            "### 🎯 Investigation Confidence"
        )

        st.progress(
            confidence["confidence_score"] / 100
        )

        for factor in confidence[
            "confidence_factors"
        ]:

            st.write(
                f"✓ {factor}"
            )

        # ----------------------------------------------------
        # GAPS
        # ----------------------------------------------------

        gaps = report[
            "gaps"
        ][
            "investigation_gaps"
        ]

        st.markdown(
            "### 🔍 Investigation Gaps"
        )

        if not gaps:

            st.success(
                "No major investigation gaps detected."
            )

        else:

            for gap in gaps:

                st.warning(
                    f"**{gap['priority']} Priority — "
                    f"{gap['gap']}**\n\n"
                    f"{gap['question']}"
                )

        # ----------------------------------------------------
        # REPORT DOWNLOAD
        # ----------------------------------------------------

        st.markdown("---")

        report_text = nexus.to_text(
            report
        )

        st.download_button(
            "📥 DOWNLOAD INCIDENT REPORT",
            data=report_text,
            file_name=(
                f"{report['report_id']}.txt"
            ),
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# HISTORY PAGE
# ============================================================

elif st.session_state.page == "History":

    st.markdown(
        """
        <div class="nexus-brand" style="font-size:3rem;">
        INCIDENT ARCHIVE
        </div>

        <div class="nexus-subtitle">
        HISTORICAL INVESTIGATIONS • INTELLIGENCE RECORDS
        </div>
        """,
        unsafe_allow_html=True,
    )

    incidents = history.get_history()

    if not incidents:

        st.markdown(
            """
            <div class="glass-card">
            <div class="section-title">
            NO INCIDENTS RECORDED
            </div>

            Your completed NEXUS investigations will appear
            here as an intelligence archive.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        total_incidents = len(incidents)

        critical_count = sum(
            1
            for incident in incidents
            if incident["severity_level"]
            == "Critical"
        )

        high_count = sum(
            1
            for incident in incidents
            if incident["severity_level"]
            == "High"
        )

        avg_confidence = round(
            sum(
                incident[
                    "confidence_score"
                ]
                for incident in incidents
            )
            / total_incidents
        )

        metric1, metric2, metric3, metric4 = (
            st.columns(4)
        )

        with metric1:

            st.metric(
                "TOTAL INCIDENTS",
                total_incidents,
            )

        with metric2:

            st.metric(
                "CRITICAL",
                critical_count,
            )

        with metric3:

            st.metric(
                "HIGH SEVERITY",
                high_count,
            )

        with metric4:

            st.metric(
                "AVG CONFIDENCE",
                f"{avg_confidence}%",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="section-title">
            INVESTIGATION RECORDS
            </div>
            """,
            unsafe_allow_html=True,
        )

        for entry in incidents:

            severity_level = (
                entry["severity_level"]
            )

            severity_score = (
                entry["severity_score"]
            )

            confidence_score = (
                entry["confidence_score"]
            )

            incident_type = (
                entry["incident_type"]
            )

            timestamp = (
                entry["timestamp"]
                .replace("T", " • ")
            )

            with st.expander(
                f"{incident_type.upper()}  •  "
                f"{severity_level.upper()}  •  "
                f"{severity_score}/100"
            ):

                st.markdown(
                    f"""
                    <div class="glass-card">

                    <div style="
                        color:#7f89a5;
                        font-size:0.75rem;
                        letter-spacing:0.08em;
                        margin-bottom:0.8rem;
                    ">
                    INVESTIGATION RECORDED • {timestamp}
                    </div>

                    <div style="
                        font-size:1rem;
                        line-height:1.7;
                        color:#dce4ff;
                    ">
                    {entry["description"]}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "SEVERITY",
                        severity_level,
                        f"{severity_score}/100",
                    )

                with col2:

                    st.metric(
                        "CONFIDENCE",
                        f"{confidence_score}%",
                    )

                with col3:

                    st.metric(
                        "INCIDENT TYPE",
                        incident_type,
                    )

                st.markdown(
                    """
                    <div class="section-title">
                    ARCHIVE ACTIONS
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                action1, action2 = (
                    st.columns(2)
                )

                with action1:

                    if st.button(
                        "🗑 DELETE RECORD",
                        key=(
                            f"delete_"
                            f"{entry['id']}"
                        ),
                        use_container_width=True,
                    ):

                        history.delete_incident(
                            entry["id"]
                        )

                        st.rerun()

                with action2:

                    analysis = entry.get(
                        "analysis",
                        {}
                    )

                    if analysis:

                        report_text = (
                            nexus.to_text(
                                analysis
                            )
                        )

                        st.download_button(
                            "📥 DOWNLOAD REPORT",
                            data=report_text,
                            file_name=(
                                f"{analysis.get('report_id', 'nexus-report')}.txt"
                            ),
                            mime="text/plain",
                            key=(
                                f"download_"
                                f"{entry['id']}"
                            ),
                            use_container_width=True,
                        )

# ============================================================
# COMPARE PAGE
# ============================================================

elif st.session_state.page == "Compare":

    st.markdown(
        """
        <div class="nexus-brand" style="font-size:3rem;">
        INCIDENT DIFF
        </div>

        <div class="nexus-subtitle">
        COMPARE INVESTIGATIONS • DETECT ESCALATION • REVEAL CHANGE
        </div>
        """,
        unsafe_allow_html=True,
    )

    incidents = history.get_history()

    if len(incidents) < 2:

        st.markdown(
            """
            <div class="glass-card">
            <div class="section-title">
            INSUFFICIENT INVESTIGATION DATA
            </div>

            At least two completed investigations are required
            to generate comparative intelligence.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        incident_map = {
            (
                f"{item['timestamp'].replace('T', ' • ')}"
                f" — {item['incident_type']}"
                f" — {item['severity_level']}"
            ): item
            for item in incidents
        }

        options = list(incident_map.keys())

        st.markdown(
            """
            <div class="glass-card">
            <div class="section-title">
            SELECT INVESTIGATION PAIR
            </div>
            Compare two completed investigations to identify
            severity changes, confidence shifts, shared systems,
            evidence overlap and emerging probable causes.
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:

            previous_label = st.selectbox(
                "BASELINE INCIDENT",
                options,
                index=1 if len(options) > 1 else 0,
            )

        with col2:

            current_label = st.selectbox(
                "CURRENT INCIDENT",
                options,
                index=0,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "⚔️ GENERATE INTELLIGENCE COMPARISON",
            use_container_width=True,
        ):

            from core.comparison_engine import (
                ComparisonEngine
            )

            previous = (
                incident_map[
                    previous_label
                ]["analysis"]
            )

            current = (
                incident_map[
                    current_label
                ]["analysis"]
            )

            comparison = (
                ComparisonEngine().compare(
                    previous,
                    current,
                )
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # =================================================
            # COMPARISON OVERVIEW
            # =================================================

            st.markdown(
                """
                <div class="section-title">
                COMPARISON OVERVIEW
                </div>
                """,
                unsafe_allow_html=True,
            )

            metric1, metric2, metric3, metric4 = (
                st.columns(4)
            )

            severity_delta = (
                comparison["severity_change"]
            )

            confidence_delta = (
                comparison["confidence_change"]
            )

            with metric1:

                st.metric(
                    "SEVERITY",
                    (
                        f"{comparison['current_severity_score']}"
                        f"/100"
                    ),
                    (
                        f"{severity_delta:+d}"
                        f" points"
                    ),
                )

            with metric2:

                st.metric(
                    "CONFIDENCE",
                    (
                        f"{comparison['current_confidence_score']}"
                        f"/100"
                    ),
                    (
                        f"{confidence_delta:+d}"
                        f" points"
                    ),
                )

            with metric3:

                st.metric(
                    "SIMILARITY",
                    (
                        f"{comparison['similarity_score']}%"
                    ),
                )

            with metric4:

                st.metric(
                    "SHARED SYSTEMS",
                    len(
                        comparison[
                            "common_systems"
                        ]
                    ),
                )

            # =================================================
            # INTELLIGENCE SUMMARY
            # =================================================

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                """
                <div class="section-title">
                INTELLIGENCE ASSESSMENT
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="glass-card"
                     style="font-size:1.05rem;
                            line-height:1.8;">
                {comparison["summary"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # =================================================
            # SEVERITY TRANSITION
            # =================================================

            left, right = st.columns(2)

            with left:

                st.markdown(
                    "### 📈 Severity Transition"
                )

                st.markdown(
                    f"""
                    <div class="glass-card">
                    <div style="
                        color:#7f89a5;
                        font-size:0.75rem;
                        letter-spacing:0.08em;
                    ">
                    BASELINE
                    </div>

                    <div style="
                        font-size:2rem;
                        font-weight:700;
                        margin-top:0.5rem;
                    ">
                    {comparison['previous_severity_score']}/100
                    </div>

                    <br>

                    <div style="
                        color:#9bb8ff;
                        font-weight:700;
                    ">
                    ↓
                    </div>

                    <br>

                    <div style="
                        color:#7f89a5;
                        font-size:0.75rem;
                        letter-spacing:0.08em;
                    ">
                    CURRENT
                    </div>

                    <div style="
                        font-size:2rem;
                        font-weight:700;
                        margin-top:0.5rem;
                    ">
                    {comparison['current_severity_score']}/100
                    </div>

                    <br>

                    <div style="
                        color:#a97cff;
                        font-weight:700;
                    ">
                    {comparison['severity_trend']}
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with right:

                st.markdown(
                    "### 🎯 Confidence Shift"
                )

                st.markdown(
                    f"""
                    <div class="glass-card">
                    <div style="
                        color:#7f89a5;
                        font-size:0.75rem;
                        letter-spacing:0.08em;
                    ">
                    BASELINE
                    </div>

                    <div style="
                        font-size:2rem;
                        font-weight:700;
                        margin-top:0.5rem;
                    ">
                    {comparison['previous_confidence_score']}/100
                    </div>

                    <br>

                    <div style="
                        color:#9bb8ff;
                        font-weight:700;
                    ">
                    ↓
                    </div>

                    <br>

                    <div style="
                        color:#7f89a5;
                        font-size:0.75rem;
                        letter-spacing:0.08em;
                    ">
                    CURRENT
                    </div>

                    <div style="
                        font-size:2rem;
                        font-weight:700;
                        margin-top:0.5rem;
                    ">
                    {comparison['current_confidence_score']}/100
                    </div>

                    <br>

                    <div style="
                        color:#a97cff;
                        font-weight:700;
                    ">
                    {comparison['confidence_change']:+d}
                    point intelligence shift
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # =================================================
            # SHARED INTELLIGENCE
            # =================================================

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    "### 🔗 Shared Systems"
                )

                systems = comparison[
                    "common_systems"
                ]

                if systems:

                    for system in systems:

                        st.markdown(
                            f"""
                            <div class="glass-card">
                            ⚙️ &nbsp; {system}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                else:

                    st.info(
                        "No shared affected systems detected."
                    )

            with col2:

                st.markdown(
                    "### 🔍 Shared Evidence"
                )

                evidence = comparison[
                    "shared_evidence"
                ]

                if evidence:

                    for item in evidence:

                        st.markdown(
                            f"""
                            <div class="glass-card">
                            ✓ &nbsp; {item}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                else:

                    st.info(
                        "No shared evidence patterns detected."
                    )

            # =================================================
            # CHANGE DETECTION
            # =================================================

            st.markdown(
                "### ⚠️ Investigation Change Detection"
            )

            new_causes = comparison[
                "new_causes"
            ]

            removed_causes = comparison[
                "removed_causes"
            ]

            change1, change2 = st.columns(2)

            with change1:

                st.markdown(
                    """
                    <div class="section-title">
                    NEW PROBABLE CAUSES
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if new_causes:

                    for cause in new_causes:

                        st.markdown(
                            f"""
                            <div class="glass-card">
                            <b>+</b>
                            &nbsp;&nbsp;
                            {cause}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                else:

                    st.success(
                        "No new probable causes detected."
                    )

            with change2:

                st.markdown(
                    """
                    <div class="section-title">
                    REMOVED PROBABLE CAUSES
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if removed_causes:

                    for cause in removed_causes:

                        st.markdown(
                            f"""
                            <div class="glass-card">
                            <b>−</b>
                            &nbsp;&nbsp;
                            {cause}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                else:

                    st.success(
                        "No probable causes were removed."
                    )