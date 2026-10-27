# Reflection

The supplied handout does not include the four reflection question prompts. These answers address its stated learning outcomes and can be adapted if the instructor provides different prompts.

1. **What is static code analysis, and how did it help?**
   Static analysis checks source code without running it. Pylint and Flake8 surfaced maintainability and formatting problems; Bandit identified risky XML-RPC and unsafe HTML handling. The review also exposed auction-rule bugs that required reading the code and demo output because a linter cannot determine the intended business rules.

2. **Which tool was most useful, and why?**
   Bandit was most useful for quickly locating security-sensitive code paths, especially disabled template escaping and treating user text as safe HTML. Pylint and Flake8 were useful for making the file easier to maintain and consistently formatted.

3. **What issues did the tools miss, and how were they found?**
   The tools did not know the auction's rules. Running the demo showed that a seller could win their own item, bids below the reserve were accepted, equal bids replaced the leader, and a valid 9:30 AM bid was rejected because times were compared as strings. Reading the output and tracing the logic found these defects.

4. **How does static analysis improve code quality and maintainability?**
   It gives repeatable feedback before code is deployed and helps a team spot risky patterns early. Clear names, narrow error handling, documentation, and consistent formatting also make code easier to review. It still needs to be combined with execution and domain-specific reasoning because tools cannot infer every requirement.
