Title: Ensuring Accuracy and Relevance: Why We Implemented a Query Validator
Date:19.11.2024
Status: Accepted
Context:
[Provide a brief explanation of the issue, decision-making process, and the background of why query validation is relevant and necessary in this application.]
Decision:
We chose to implement the query validation after the generation of SQL queries by the LLM to ensure their accuracy, security, and alignment with user intent.
Consequences:
Pros:
Reduces errors by ensuring table and column names are accurate and syntactically correct.
Aligns queries with the user's questions, improving overall accuracy and relevance.
Prevents unexpected modifications to the data, ensuring data integrity.
Cons:
Extensive validation for large queries may slow down execution times.
Users may encounter delays if a query is denied due to validation failures. Clear feedback will be provided to help users understand and fix issue
