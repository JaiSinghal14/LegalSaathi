# app.py

import json
import re
from typing import Any, Dict, List, Optional, Union

import streamlit as st
from dotenv import load_dotenv

from crew import legal_assistant_crew

load_dotenv()

st.set_page_config(page_title="AI Legal Assistant", page_icon="🧠", layout="wide")

EXAMPLE_SCENARIOS: Dict[str, str] = {
    "Workplace harassment": "My manager has been harassing me with constant threats of firing if I don’t work unpaid overtime. "
    "He also sent inappropriate messages late at night. What action can I take?",
    "Financial fraud": "I loaned ₹5 lakh to a relative who promised to return it in 3 months. It has been a year, "
    "and now he is denying the transaction even though I have bank transfer proof.",
    "Property dispute": "Our neighbor broke down the boundary wall and encroached on our land while we were out of town. "
    "We have the property papers and earlier photographs.",
}

if "issue_text" not in st.session_state:
    st.session_state.issue_text = ""
if "history" not in st.session_state:
    st.session_state.history: List[Dict[str, str]] = []


def _coerce_to_text(value: Any) -> str:
    """Best-effort conversion to displayable text."""
    if value is None:
        return ""
    if hasattr(value, "output"):
        value = value.output
    elif hasattr(value, "raw"):
        value = value.raw
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, ensure_ascii=False)
    return str(value)


def _extract_json(value: str) -> Optional[Union[Dict[str, Any], List[Any]]]:
    """Try to parse JSON from the model response."""
    if not value:
        return None
    fenced = re.search(r"json(.*?)", value, re.DOTALL | re.IGNORECASE)
    json_payload = fenced.group(1) if fenced else value
    json_payload = json_payload.strip()
    try:
        return json.loads(json_payload)
    except json.JSONDecodeError:
        return None


st.title("⚖ Personal AI Legal Assistant")
st.caption(
    "Describe your legal situation to receive a structured breakdown, IPC guidance, precedent summary, "
    "and a draft-ready document."
)

with st.sidebar:
    st.header("How to use")
    st.markdown(
        "- Share facts chronologically\n"
        "- Mention locations, dates, and amounts\n"
        "- Keep personal data generic for privacy\n"
        "- Review generated drafts before filing"
    )
    st.divider()
    st.subheader("Need inspiration?")
    scenario = st.selectbox("Sample scenarios", list(EXAMPLE_SCENARIOS.keys()), index=0)
    if st.button("Fill example", use_container_width=True):
        st.session_state.issue_text = EXAMPLE_SCENARIOS[scenario]
        st.toast("Example added to the editor.")
    st.divider()
    st.subheader("Recent runs")
    if st.session_state.history:
        for idx, item in enumerate(st.session_state.history[:3], start=1):
            st.markdown(f"#{idx}** {item['query'][:80]}{'...' if len(item['query']) > 80 else ''}")
    else:
        st.caption("No runs yet. Submit your first case!")

col1, col2, col3 = st.columns(3)
col1.metric("Agents engaged", "4", help="Case intake, IPC expert, precedent analyst, drafter")
col2.metric("Average turnaround", "~30s", help="Depends on workload and model latency")
col3.metric("Document types", "FIR, legal notice, summary", help="Final draft is customized per case")

st.divider()

with st.form("legal_form", clear_on_submit=False):
    user_input = st.text_area(
        "📝 Describe your legal issue",
        height=220,
        key="issue_text",
        placeholder="Provide a concise but detailed narrative of your legal problem...",
    )
    form_cols = st.columns([3, 1])
    submitted = form_cols[0].form_submit_button("🔍 Run Legal Assistant", use_container_width=True)
    cleared = form_cols[1].form_submit_button("Reset", use_container_width=True, type="secondary")

if cleared:
    st.session_state.issue_text = ""
    st.experimental_rerun()

if submitted:
    if not user_input.strip():
        st.warning("Please enter a legal issue to analyze.")
    else:
        with st.status("Running legal workflow...", expanded=True) as status:
            status.write("Collecting case intake information…")
            result = legal_assistant_crew.kickoff(inputs={"user_input": user_input})
            status.write("Drafting final legal document…")
            status.update(label="Workflow complete", state="complete", expanded=False)

        display_text = _coerce_to_text(result)
        parsed_json = _extract_json(display_text)

        st.success("✅ Workflow complete — review the structured insights below.")

        tabs = st.tabs(["Overview", "Structured data", "Raw output"])

        with tabs[0]:
            st.subheader("Summary")
            st.markdown(display_text if not parsed_json else "Structured data extracted — see next tab.")
            st.download_button(
                "Download summary",
                data=display_text,
                file_name="legal_assistant_summary.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with tabs[1]:
            st.subheader("JSON insights")
            if parsed_json:
                st.json(parsed_json, expanded=True)
            else:
                st.info("Could not detect JSON. The assistant may have returned plain text.")

        with tabs[2]:
            st.subheader("Raw assistant output")
            st.code(display_text, language="markdown")

        st.session_state.history.insert(
            0,
            {
                "query": user_input.strip(),
                "output": display_text,
            },
        )
        st.session_state.history = st.session_state.history[:5]

if st.session_state.history:
    st.divider()
    with st.expander("Previous analyses (most recent first)", expanded=False):
        for item in st.session_state.history:
            st.markdown(f"*Query*: {item['query']}")
            st.code(item["output"][:1200] + ("..." if len(item["output"]) > 1200 else ""), language="markdown")
            st.divider()