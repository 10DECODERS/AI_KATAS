Title: Why We Are Doing Query Validation Before Execution
Date: 19.11.2024
Status: Accepted
Context:
[Provide a brief explanation of the issue, decision-making process, and the background of why query validation before execution is necessary.]
Decision:
We chose to validate SQL queries before execution to ensure their accuracy, relevance, and security, preventing errors and safeguarding the database.
Consequences:
Pros:
Prevents syntactical errors and ensures compatibility with the database schema.
Confirms table and column names are valid, reducing runtime errors.
Improves query relevance by aligning it with user intent.
Restricts queries to safe operations, preventing unintended data modifications.
Cons:
Validation can increase response time, especially for complex queries.
Users may face delays if validation fails, requiring clear feedback to correct their input.