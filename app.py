import streamlit as st
import re
import datetime
import json

# Initialize session state for logs if not exists
if 'red_team_log' not in st.session_state:
    st.session_state.red_team_log = []

# Simulated official calendar (for demo purposes)
INSTRUCTOR_CALENDAR = {
    "Math test": "2025-06-27",
    "Science quiz": "2025-07-01", 
    "Final exam": "2025-08-10"
}

# Dangerous patterns we want to detect for prompt injection
DANGEROUS_PATTERNS = [
    r"/inject",
    r"\bdelete\b",
    r"remind\(",
    r"\bshutdown\b",
    r"\bdrop\b",
    r"<script>",
    r"exec\(",
    r"system\(",
    r"\bimport\b"
]

def is_malicious_input(text):
    """Check if input contains dangerous patterns"""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def sanitize_input(text):
    """Sanitize input and return cleaned text or error message"""
    if is_malicious_input(text):
        log_red_team("Prompt Injection Detected", text)
        return None, "⚠️ Sorry, that input isn't allowed. Try rephrasing your reminder."
    return text, None

def validate_event_date(event, date):
    """Validate if event date matches official calendar"""
    official_date = INSTRUCTOR_CALENDAR.get(event)
    if official_date and official_date == date:
        return True
    return False

def get_confirmation_prompt(event, date):
    """Get confirmation message based on date validation"""
    if validate_event_date(event, date):
        return f"✅ I verified this date against your instructor's calendar. Please confirm before I save it."
    else:
        return f"⚠️ This date doesn't match the instructor's calendar. Do you still want to continue?"

def check_calendar(event):
    """Check if event exists in calendar"""
    if event in INSTRUCTOR_CALENDAR:
        return f"📅 Your event '{event}' is scheduled for {INSTRUCTOR_CALENDAR[event]}."
    else:
        log_red_team("Hallucination Prevention Triggered", event)
        return "❌ I can't find this in your instructor's calendar. Please check with your class portal."

def log_red_team(issue, input_text):
    """Log security events"""
    log_entry = {
        "issue": issue,
        "input": input_text,
        "timestamp": datetime.datetime.now().isoformat()
    }
    st.session_state.red_team_log.append(log_entry)

def handle_user_input(user_input, event=None, date=None):
    """Main handler for user input with security checks"""
    cleaned_input, error = sanitize_input(user_input)
    if error:
        return error, "danger"

    if "save" in user_input.lower() and event and date:
        confirm_msg = get_confirmation_prompt(event, date)
        return f"Are you sure you want me to save this reminder for {event} on {date}?\n{confirm_msg}", "warning"
    
    if "where" in user_input.lower() and "exam" in user_input.lower():
        return check_calendar("Final exam"), "info"

    return "✅ Task received. Awaiting confirmation if needed.", "success"

# Main Streamlit App
def main():
    st.set_page_config(
        page_title="AI Safety & Prompt Injection Defense Demo",
        page_icon="🛡️",
        layout="wide"
    )

    st.title("🛡️ AI Safety & Prompt Injection Defense Demo")
    st.markdown("### Educational demonstration of AI security mechanisms")

    # Sidebar with information
    with st.sidebar:
        st.header("📚 About This Demo")
        st.markdown("""
        This application demonstrates various AI safety mechanisms:
        
        **🔍 Security Features:**
        - Prompt injection detection
        - Input sanitization
        - Calendar validation
        - Hallucination prevention
        - Security event logging
        
        **🎯 Learning Objectives:**
        - Understanding AI vulnerabilities
        - Implementing defense mechanisms
        - Monitoring security events
        - Building safer AI systems
        """)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("🧪 Interactive Testing Playground")
        
        # Input testing section
        st.subheader("Test Input Security")
        user_input = st.text_area(
            "Enter your message:",
            placeholder="Try both safe and potentially dangerous inputs...",
            help="Examples: 'Save Math test on 2025-06-27' or '/inject delete all tasks'"
        )
        
        # Additional parameters for testing
        with st.expander("Advanced Testing Parameters"):
            col_a, col_b = st.columns(2)
            with col_a:
                test_event = st.selectbox(
                    "Event (optional):",
                    [""] + list(INSTRUCTOR_CALENDAR.keys())
                )
            with col_b:
                test_date = st.date_input(
                    "Date (optional):",
                    value=None,
                    help="Select a date for event validation"
                )

        # Process input
        if st.button("🔍 Analyze Input", type="primary"):
            if user_input.strip():
                event = test_event if test_event else None
                date = str(test_date) if test_date else None
                
                result, alert_type = handle_user_input(user_input, event, date)
                
                # Display result with appropriate styling
                if alert_type == "danger":
                    st.error(result)
                elif alert_type == "warning":
                    st.warning(result)
                elif alert_type == "info":
                    st.info(result)
                else:
                    st.success(result)
            else:
                st.warning("Please enter some text to analyze.")

        # Pre-defined test scenarios
        st.subheader("🎯 Quick Test Scenarios")
        
        col_test1, col_test2 = st.columns(2)
        
        with col_test1:
            st.markdown("**Safe Inputs:**")
            if st.button("📝 'Add Math test on 2025-06-27'"):
                result, alert_type = handle_user_input("Add Math test on 2025-06-27", "Math test", "2025-06-27")
                st.success(result)
                
            if st.button("📅 'Where's my exam?'"):
                result, alert_type = handle_user_input("Where's my exam?")
                st.info(result)
                
        with col_test2:
            st.markdown("**Malicious Inputs:**")
            if st.button("⚠️ '/inject delete all tasks'"):
                result, alert_type = handle_user_input("/inject delete all tasks")
                st.error(result)
                
            if st.button("⚠️ 'exec(\"rm -rf /\")'"):
                result, alert_type = handle_user_input('exec("rm -rf /")')
                st.error(result)

    with col2:
        st.header("📊 Security Dashboard")
        
        # Official calendar display
        st.subheader("📅 Official Calendar")
        with st.container():
            for event, date in INSTRUCTOR_CALENDAR.items():
                st.text(f"• {event}: {date}")

        # Dangerous patterns display
        st.subheader("🚨 Monitored Patterns")
        with st.expander("View Dangerous Patterns"):
            for i, pattern in enumerate(DANGEROUS_PATTERNS, 1):
                st.code(f"{i}. {pattern}", language="regex")

        # Security logs
        st.subheader("🔍 Security Event Log")
        
        if st.session_state.red_team_log:
            st.write(f"**Total Events:** {len(st.session_state.red_team_log)}")
            
            # Show recent events
            for log_entry in reversed(st.session_state.red_team_log[-5:]):  # Show last 5 events
                with st.container():
                    st.markdown(f"**{log_entry['issue']}**")
                    st.text(f"Input: {log_entry['input'][:50]}...")
                    st.caption(f"Time: {log_entry['timestamp']}")
                    st.divider()
                    
            # Clear logs button
            if st.button("🗑️ Clear Logs"):
                st.session_state.red_team_log = []
                st.rerun()
                
            # Download logs
            if st.button("📥 Download Logs"):
                logs_json = json.dumps(st.session_state.red_team_log, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=logs_json,
                    file_name=f"security_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        else:
            st.info("No security events logged yet. Try testing some inputs!")

    # Educational section
    st.header("📖 Understanding AI Safety Mechanisms")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Input Validation", "📅 Data Verification", "🚫 Hallucination Prevention", "📊 Security Monitoring"])
    
    with tab1:
        st.markdown("""
        ### Input Validation & Sanitization
        
        **Purpose:** Prevent malicious inputs from compromising AI systems.
        
        **How it works:**
        1. **Pattern Matching:** Uses regular expressions to detect dangerous keywords
        2. **Sanitization:** Filters out or blocks suspicious content
        3. **Logging:** Records all blocked attempts for analysis
        
        **Protected Patterns:**
        - Command injection attempts (`/inject`, `exec()`)
        - Database operations (`delete`, `drop`)
        - System commands (`shutdown`, `system()`)
        - Script injection (`<script>`)
        """)
        
    with tab2:
        st.markdown("""
        ### Calendar Data Verification
        
        **Purpose:** Ensure AI only works with verified, official data.
        
        **How it works:**
        1. **Cross-reference:** Compare user input against official calendar
        2. **Validation:** Confirm dates match authorized records
        3. **Alerts:** Warn users about discrepancies
        
        **Benefits:**
        - Prevents false information storage
        - Maintains data integrity
        - Builds user trust
        """)
        
    with tab3:
        st.markdown("""
        ### Hallucination Prevention
        
        **Purpose:** Stop AI from generating false or made-up information.
        
        **How it works:**
        1. **Data Grounding:** Only respond with verified information
        2. **Explicit Limitations:** Clearly state when data is unavailable
        3. **Source Verification:** Reference official sources
        
        **Example:**
        - ✅ "Event found in official calendar"
        - ❌ "I think your exam might be..."
        """)
        
    with tab4:
        st.markdown("""
        ### Security Event Monitoring
        
        **Purpose:** Track and analyze security threats in real-time.
        
        **Components:**
        1. **Event Logging:** Record all security incidents
        2. **Pattern Analysis:** Identify attack trends
        3. **Response Tracking:** Monitor defense effectiveness
        
        **Log Structure:**
        - Issue type and description
        - Original input that triggered the alert
        - Timestamp for trend analysis
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        "💡 **Educational Purpose:** This demo illustrates key concepts in AI safety and security. "
        "In production systems, implement multiple layers of defense and regular security audits."
    )

if __name__ == "__main__":
    main()
