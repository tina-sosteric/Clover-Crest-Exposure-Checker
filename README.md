# Clover & Crest Credential Exposure Checker

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-learning%20project-orange)

My first Python project: a tool that checks which employees at a
(fictional) company were detected in a leaked password dump, scores how
urgent each case is, and runs a second, independent audit on top — are
our passwords weak in general, leak or no leak?

Built immediately after finishing Python basics and TryHackMe's
cybersecurity fundamentals (Pre Security and Cybersecurity 101 paths).

---

## 🎬 Interactive Walkthrough

**[▶ View the incident simulation](https://tina-sosteric.github.io/Clover-Crest-Exposure-Checker/CloverCrest-Security-Incident-Simulation.html)**

Steps through the scenario stage by stage, using the real numbers this
project's code actually produced.

---

## Table of Contents

- [Background](#background)
- [The Incident](#the-incident)
- [Content](#content)
- [Concepts](#concepts)
- [Sample Output](#sample-output)
- [Run the Project](#run-the-project)
- [Publishing the Simulation](#publishing-the-simulation)
- [Scope and Limitations](#scope-and-limitations)
- [Technical Choices](#technical-choices)
- [About Me](#about-me)

## Background

Built to put newly learned concepts into practice:
- Codecademy's **Learn Python 3**
- TryHackMe's **Pre Security** and **Cybersecurity 101**

As a fraud investigator also interested in cybersecurity, I
wanted a project that connected the two: review data, flag risk,
report on it — a similar basic shape as fraud investigations, just
applied to passwords instead of transactions.

The hashing/encryption content was also fresh from TryHackMe, so this
was a chance to implement it myself rather than leave it as theory.

**Note:** Clover & Crest is not a real company. SnuggleSync is not a
real product. Both are fictional, built to give the code a scenario to
work within.

## The Incident

Clover & Crest is a fictional company with 50 employees. Its systems
were never breached — but a number of employees signed up for a fake
dating app called SnuggleSync during work hours, using their Clover &
Crest work email and password to do it. SnuggleSync was in fact a
phishing site, and those credentials were later found circulating in a
leaked dump. A bug bounty researcher identified the leak and reported it
to Clover & Crest's security team.

Because this was not a breach of Clover & Crest's own systems, a blanket
password reset across all 50 employees would be a disproportionate
response. Instead, the response is scoped to the employees confirmed
present in the leaked dump. A second, independent audit is then run
against all 50 employees' password hashes — regardless of who was in the
dump — to assess password strength across the company more broadly.

## Content

| File | Purpose |
|---|---|
| `test_data.py` | Generates the fake company: 50 Faker-generated employees, hashed passwords, and a simulated leaked dump. Setup only — not part of the actual tool. |
| `exposure_check.py` | The tool itself. Cross-references the dump against the employee list, hashes each leaked password to check if it's still in use, scores severity, and writes an incident report. |
| John the Ripper *(separate mini-project)* | An independent audit of all 50 employees' password hashes, unrelated to the leak, using a real password-cracking tool and a wordlist. |

### Data Flow

```
generate fake employees & leaked dump (test_data.py)
              │
              ▼
   cross-match dump vs. employees (exposure_check.py)
              │
              ▼
  hash-compare matched employees → CRITICAL or MODERATE
              │
              ▼
     incident report (data_leak_report.txt)


   (separately, independent of the leak)

 export employee hashes → run John the Ripper → audit results
```

## Concepts

- Loops, functions, conditionals, dictionaries — Python fundamentals
- Dictionaries as fast lookup tables, for matching emails between two
  datasets
- File I/O — reading/writing CSV and plain-text files
- SHA-256 hashing
- **Verification vs. cracking** — `exposure_check.py` verifies a known
  candidate password against a hash; John the Ripper cracks a hash with
  no known candidate, by testing a wordlist against it
- **zxcvbn** — a real password-strength library, originally built by
  Dropbox
- **Faker** — generating realistic but non-identifying synthetic test
  data
- **John the Ripper** — a real, free password-auditing tool

## Sample Output

Real output from `exposure_check.py`:

```text
Total Employees:  50
Total Dump Entries:  37
Matches Detected:  5
CRITICAL: 3
MODERATE: 2
```

The report file (`data_leak_report.txt`):
```text
austin.pearson@clovercrest.test: CRITICAL
jacqueline.mathis@clovercrest.test: CRITICAL
kenneth.collins@clovercrest.test: CRITICAL
brandi.marks@clovercrest.test: MODERATE
bradley.lynn@clovercrest.test: MODERATE

The following accounts need forced reset:
austin.pearson@clovercrest.test
jacqueline.mathis@clovercrest.test
kenneth.collins@clovercrest.test
```

From the John the Ripper audit, run independently of the leak:
```text
37 out of 50 employee password hashes cracked using a common wordlist.
```

37 out of 50 — higher than I expected, even having picked half of those
passwords myself.

## Run the Project

### Requirements
- Python 3.10+
- `pip install faker zxcvbn`
- [John the Ripper](https://www.openwall.com/john/) — jumbo edition
  specifically, see note below

### Steps

```bash
# 1. Generate the fake company + leaked dump
python test_data.py

# 2. Run the exposure check
python exposure_check.py

# 3. Prepare hashes for John the Ripper
python export_hashes.py

# 4. Run the audit
john --format=Raw-SHA256 --wordlist=common_wordlist.txt internal_hashes.txt

# 5. Save the cracked results (this is the evidence worth committing)
john --show --format=Raw-SHA256 internal_hashes.txt > jtr_results.txt
```

**Note on John the Ripper:** the standard `apt install john` package on
Ubuntu only includes "core" John, which doesn't support raw hash formats
like `Raw-SHA256` — this cost me a fair amount of time chasing "Unknown
ciphertext format" errors before I figured out why. You need the
**jumbo** edition, built from source:

```bash
git clone https://github.com/openwall/john -b bleeding-jumbo john-jumbo
cd john-jumbo/src
./configure && make -sj4
```
Takes a few minutes to compile.

Once built, run it via the full path to the jumbo binary — plain `john`
will still point at the old core version if both are installed:
```bash
~/john-jumbo/run/john --format=Raw-SHA256 --wordlist=common_wordlist.txt internal_hashes.txt
~/john-jumbo/run/john --show --format=Raw-SHA256 internal_hashes.txt > jtr_results.txt
```

## Publishing the Simulation

The interactive HTML walkthrough can be published for free with
**GitHub Pages**:
1. Push this repo to GitHub
2. **Settings → Pages** → set source to your main branch
3. It'll go live at:
   `https://yourusername.github.io/repo-name/CloverCrest_Security_Incident_Simulation.html`
4. Update the link at the top of this README with that URL

## Scope and Limitations

- All data is entirely synthetic — no real people, no real company, no
  actual leaked credentials anywhere
- The CRITICAL/MODERATE scoring is deliberately simple, not a
  weighted, multi-factor model
- No automated tests
- The dataset is clean by design — real-world data is significantly
  messier than anything in this repo

## Technical Choices

- **Hashing instead of comparing plaintext** — reflects how real systems
  actually store passwords
- **Separating data generation from the tool** (`test_data.py` vs.
  `exposure_check.py`) — a real security tool doesn't generate its own
  test data as part of normal operation, so keeping them apart felt
  more honest
- **Scoping the response to confirmed-affected employees only** — this
  wasn't a breach of Clover & Crest's own systems, so a blanket reset
  would be disproportionate
- **Running the John the Ripper audit independently of the leak** —
  real security teams don't wait for an incident to reveal that
  passwords are weak; they check proactively

## Ethical Use

This project uses John the Ripper against passwords I generated myself,
on data I own, for educational purposes. It does not target, access,
or attempt to crack any real accounts, systems, or credentials
belonging to anyone else. If you use this code, only run it against
data and systems you own or are explicitly authorized to test.

## About Me

I'm a fraud investigator learning Python and cybersecurity
fundamentals, working toward a role that combines both. The match →
verify → score → report pattern in this project mirrors the same logic
used in fraud and account-risk workflows — applied here to password
data instead of transactions.

