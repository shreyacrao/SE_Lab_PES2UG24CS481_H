\# Static Code Analysis — Issues and Fixes



The line numbers below refer to the original, uncorrected `student\_grade\_system.py` and match the baseline reports.



| \*\*Issue\*\* | \*\*Type\*\* | \*\*Line(s)\*\* | \*\*Description\*\* | \*\*Fix Approach\*\* |

|---|---|---:|---|---|

| MD5 hashing (`hashlib.md5`) | Security — High | 49 | Bandit B324 identified use of a weak hashing algorithm. | Replaced MD5 with SHA-256 using `hashlib.sha256()`. |

| Shell command execution (`os.system`) | Security — High | 60 | Bandit B605 flagged shell execution, which can introduce command-execution risks. | Removed the shell command and printed the export message directly in Python. |

| Use of `eval()` | Security — Medium | 44 | Bandit B307 and Pylint W0123 flagged evaluation of a string as Python code. | Removed `eval()` and calculated the GPA directly using numeric operations. |

| Predictable random PIN | Security — Low | 53 | Bandit B311 flagged use of the standard pseudo-random generator for a PIN. | Replaced `random.randint()` with `secrets.randbelow()`. |

| Hard-coded portal token | Security — Low | 64 | Bandit B105 flagged a token-like string embedded in source code. | Removed the hard-coded token demonstration. |

| Mutable default list argument | Bug risk | 15 | Pylint W0102 flagged `\[]` as a default argument, which can retain shared state between calls. | Changed the default to `None` and initialized a new list inside the function. |

| Bare exception with ignored error | Reliability / code quality | 26–27 | Bandit B110, Pylint W0702, and Flake8 E722 flagged a broad exception handler that silently ignored errors. | Removed the broad exception-handling pattern and validated inputs. |

| File handling without explicit encoding/context manager | Reliability | 57 | Pylint W1514 and R1732 flagged missing explicit encoding and use without a context manager. | Used `with open(filename, "w", encoding="utf-8")` to ensure the file closes automatically. |

| Unused imports, variables, and style issues | Code quality / style | 6, 19, 31, 32, 34, 43, 75 | Pylint and Flake8 reported an unused `json` import, unused variables, comparison to `None`, long lines, and missing final newline. | Removed unused names, used `is None`, wrapped long lines, and added a final newline. |



\## Verification After Fixes



The corrected program was executed successfully and exported `grade\_sheet.txt`.



\- \*\*Pylint:\*\* 5.51/10 before; 10.00/10 after.

\- \*\*Bandit:\*\* 6 findings before (2 High, 1 Medium, 3 Low); no issues identified after.

\- \*\*Flake8:\*\* 8 findings before; no linting issues reported after.



Baseline reports are saved in `reports/before/`. Final reports are saved in `reports/after/`.



