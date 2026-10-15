\# Reflection — Static Code Analysis



\## 1. What is static code analysis?



Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, and style violations early, before the code is deployed.



\## 2. What are the differences between Pylint, Bandit, and Flake8?



Pylint checks code quality, naming conventions, missing documentation, unused variables, and potential programming mistakes. Bandit focuses on common security weaknesses. Flake8 checks Python style and linting issues, such as line length and unused imports. Using all three provides broader coverage.



\## 3. Which issues did you prioritize, and why?



I prioritized the high- and medium-severity security findings: MD5 hashing, shell command execution, and `eval()`. These patterns can introduce security risks. I then fixed the low-severity findings involving random PIN generation and a hard-coded token, along with code-quality and style issues.



\## 4. How did static analysis improve the program, and what did you learn?



The baseline reports identified issues that were not necessarily obvious when running the program. After the fixes, the program still executed successfully and exported the grade sheet. Pylint improved from 5.51/10 to 10.00/10, Bandit reported no issues, and Flake8 reported no linting issues. I learned that each tool checks a different aspect of code quality and that rerunning the tools is important to verify fixes.



