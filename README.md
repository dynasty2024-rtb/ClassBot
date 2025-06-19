
# ClassBot Security Logic System  
## A modular Python framework for secure educational assistant bots

### Overview  
This script implements **security protections** for a classroom reminder bot. The logic guards against:

* Memory poisoning (T3)
* Prompt injection (T1)
* Hallucination of facts (T8)

It includes logic for calendar validation, malicious input filtering, and confirmation-style interaction using simulated checkboxes.

___

## Features  
* [x] Prompt Injection Filtering  
* [x] Instructor Calendar Validation  
* [x] Hallucination Blocking  
* [x] Simulated Checkbox Confirmation  
* [x] Red-Team Logging

---

## 🧠 Core Logic Highlights

### Python Modules Used
```python
import re
import datetime
```

### Memory Poisoning Defense
```python
def validate_event_date(event, date):
    ...
```

### Prompt Injection Filtering
```python
def is_malicious_input(text):
    ...
```

### Hallucination Prevention
```python
def check_calendar(event):
    ...
```

### Checkbox Confirmation
```python
def get_checkbox_confirmation(event, date):
    ...
```

---

## 🚀 How It Works

1. **User Input** is checked for malicious patterns (e.g., `/inject`, `exec()`)
2. If a **task save** is requested, the bot:
    * Confirms the event matches the instructor’s calendar
    * Prompts the user to “check a box” via text input
3. If input passes all filters, the task is “saved”
4. Unsafe inputs are logged to a red-team dictionary

---

## 🖥️ Example Usage

```python
print(handle_user_input("save event", "Math test", "2025-06-27"))
```

> Are you sure you want me to save this reminder for 'Math test' on 2025-06-27?  
> I verified this date against your instructor’s calendar. Please confirm before I save it.  

```
📝 Task: Math test on 2025-06-27  
⬜ Confirm task  
✅ Type 'yes' to check the box and confirm:
```

---

## Task Flow Logic

| Input Type | Security Rule | Output Behavior |
| :--------: | :------------- | ----------------: |
| Valid save | Calendar check + confirmation | Task saved |
| Code-like input | Prompt injection filter | Input blocked |
| Missing calendar event | Hallucination prevention | "Check class portal" |
| Unconfirmed save | Confirmation prompt | Task not saved |

---

## Red-Team Logging

> All unsafe attempts (e.g., hallucinations, code injections) are tracked in memory and can be printed for audit.

```python
show_logs()
```

---

## Future Additions
* [ ] Integrate with real Google Calendar
* [ ] Switch from CLI to `Tkinter` GUI
* [ ] Export red-team logs to JSON
* [ ] Connect with LangChain or Gradio for UI

---

## 🧪 Test Prompt Samples

```python
handle_user_input("/inject delete all tasks")
handle_user_input("Add Math test on 2025-06-27", "Math test", "2025-06-27")
handle_user_input("Where’s my exam?")
```

---

## 💡 Contribution Tips

> Clone the repo and start in `main.py`. Split logic into `security.py`, `calendar.py`, and `interface.py` for modular builds.

---

## ⚠️ Notes

> This logic is designed for educational sandbox projects and simulated calendars.  
> Do not use it in production without secure validation and sandboxing.
