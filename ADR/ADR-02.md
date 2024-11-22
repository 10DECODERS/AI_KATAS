Title: Ensuring Accuracy and Relevance: Why We Implemented a Query Validator
Date: 15.11.2024
Status: Accepted

Context: 
In this chat application, as we are dealing with structured data, we are converting user’s question to sql query to find the result. Sometimes LLMs may prone to generate sql queries with wrong table or column names or even syntactically incorrect queries. Before being executed, the resulting queries must be verified for accuracy because of inconsistent reasoning. Also we ensure that it only creates the DQL query to avoid sql injection vulnerabilities.

Decision:
We chose to implement the query validation after the generation of SQL queries by LLM.

Consequences:

Pros:

Reducing error by making sure that table and column names are accurate and syntactically correct.
The query is highly aligned with user’s question, it improves the accuracy.
It protects the data from sql injection attacks.
It also prevent from unexpected modification in data. 

Cons:

The execution of a query may be slowed down by extensive validation, especially for large queries. 
The user may encounter a delay if a query is denied because of a validation failure. We will make sure users understand the validation process and how to fix their input by giving them clear feedback about what went wrong.
