# Problem Solving Coach - MVP v0.1

A console prototype for evaluating one IS / IS-NOT field at a time.

The goal is **not** to auto-fill an 8D. The agent should:

- distinguish known / verify / pending / not-applicable information;
- challenge weak IS / IS-NOT comparisons;
- accept unknown information instead of inventing it;
- suggest practical actions to obtain missing evidence;
- keep differences separate from demonstrated root causes;
- ask one high-value follow-up question at a time.

## 1. Prerequisites

- Python 3.10+
- An OpenAI API key authorized for this prototype
- Approval from your organization's IT / InfoSec before using real confidential plant data

For early tests, use synthetic or anonymized cases.

## 2. Windows PowerShell setup

Open PowerShell in this folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Set the API key for the current PowerShell session:

```powershell
$env:OPENAI_API_KEY = "YOUR_KEY_HERE"
```

Optional: choose the model through an environment variable:

```powershell
$env:OPENAI_MODEL = "gpt-5.6-sol"
```

## 3. Run the interactive prototype

```powershell
python main.py
```

The program will ask you to select one of the 13 fields and enter:

- problem statement;
- defect / failure mode;
- IS;
- proposed IS-NOT;
- known difference (blank or unknown is valid);
- additional context.

It returns a structured evaluation with:

- field status;
- contrast quality;
- best current contrast;
- secondary contrasts;
- observed differences;
- missing information;
- suggested investigation actions;
- one next question;
- methodological warning;
- causal boundary reminder.

## 4. Run synthetic examples

```powershell
python run_examples.py
```

## 5. Why the project is split into files

- `question_specs.py` = what each of the 13 questions is trying to learn.
- `schemas.py` = the exact structure we require from the AI.
- `coach_agent.py` = the methodological constitution and AI call.
- `main.py` = simple console interface.
- `example_cases.py` = synthetic validation cases.

Keeping methodological knowledge separate from the UI will let us add Streamlit later without rewriting the core reasoning.

## 6. Next development step

Do **not** build the full UI yet. First run real-but-anonymized test cases and score the agent:

1. Did it choose the right status?
2. Did it reject or downgrade bad contrasts for the right reason?
3. Did it avoid inventing missing information?
4. Did it recommend a realistic way to obtain missing information?
5. Did it avoid declaring root cause?
6. Was its next question the most useful one?

Once this behavior is reliable, add persistent case state and then the Streamlit interface.
