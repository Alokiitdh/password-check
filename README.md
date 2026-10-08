# Password Breach Checker (Pwned Passwords API)

A lightweight, privacy-preserving command-line utility built in Python to check whether your passwords have ever appeared in a known data breach using the official [Have I Been Pwned](https://haveibeenpwned.com/) Passwords API.

---

## 🔒 Privacy & Security: How It Works ($k$-Anonymity)

This tool **never** transmits your actual password or its complete hash over the internet. Instead, it utilizes a cryptographic technique known as **$k$-Anonymity**:

```
[ Your Password ]
       │
       ▼
 [ SHA-1 Hash ] ──> e.g. CBFDA 700CE55088E96F896AA659FD9B70E2F2717
       │
       ├─ Prefix (First 5 characters: "CBFDA") ──> Sent to API
       │
       └─ Tail (Remaining 35 characters) ───────> Kept locally on your machine
```

### Step-by-Step Breakdown (Example: `password123`)

1. **Local Hashing:**
   The password `'password123'` is converted into its 40-character SHA-1 hexadecimal hash:
   `CBFDA700CE55088E96F896AA659FD9B70E2F2717`

2. **Hash Splitting:**
   * **Prefix (5 chars):** `CBFDA`
   * **Tail (35 chars):** `A700CE55088E96F896AA659FD9B70E2F2717`

3. **API Range Query:**
   The tool queries `https://api.pwnedpasswords.com/range/CBFDA`. The API returns a list of *all* compromised hash tails that begin with `CBFDA` along with their leak counts:
   ```text
   0018G63F38D97D87140B48633F0721E6589:1
   A700CE55088E96F896AA659FD9B70E2F2717:284241
   FFF12A9724CFE932A2FBE46A42EAE3FE484:3
   ```
   *Because hundreds of different passwords share that same 5-character prefix, the API server never knows which password you are querying.*

4. **Local Matching:**
   The script scans the server's response locally for your matching tail (`A700CE...`). If found, it outputs the total number of times that specific password has appeared in breaches.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+ (or [`uv`](https://github.com/astral-sh/uv))
* `requests` library

### Installation

Clone the repository or save `main.py` locally, then install dependencies:

```bash
pip install requests
```

Or using `uv`:

```bash
uv pip install requests
```

---

## 💻 Usage

Pass one or more passwords as command-line arguments:

```bash
python main.py password123 hello superSecretP@ssw0rd!
```

Or with `uv`:

```bash
uv run main.py password123 hello superSecretP@ssw0rd!
```

### Example Output

```text
'password123' was found 284241 times! You should change this password.
'hello' was found 339943 times! You should change this password.
'superSecretP@ssw0rd!' is safe!
```

---

## ⚠️ Security Note on Command-Line History

Passing raw passwords directly as CLI arguments may leave them in your terminal's history file (`.bash_history`, `.zsh_history`, or PowerShell history). For sensitive passwords, consider reading from a file or piping them securely via standard input.