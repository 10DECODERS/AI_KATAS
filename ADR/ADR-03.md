Title: Bridging Language and Databases: The Case for Text-to-SQL Conversion
Date: 15.11.2024
Status: Accepted

Context: 
In this GenAI chat application, we generate SQL queries to execute in a database. To do that, other llms can hallucinate with or instead of SQL queries. As the text-to-SQL model is specifically built to generate SQL queries, it usually generates the SQL query without any hallucination and also avoids syntactical incorrections.

Decision:
We chose to text to sql model which particularly build to convert natural language to sql queries instead of other LLM.

Consequences:

Pros:

Models like these are specifically designed to generate only DQL queries, minimizing the risks associated with DML queries.
While general-purpose LLMs provide greater versatility in addressing a wide range of inquiries, they lack the specialized knowledge in SQL query structure that dedicated models possess.

Cons:

The text-to-SQL model could produce queries that are excessively tailored to particular schemas or data patterns, resulting in issues when utilized with slightly different schemas. 
Unclear questions might not always be processed accurately.

