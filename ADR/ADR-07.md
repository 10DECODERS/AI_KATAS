Title: Enhancing Interaction: The Role of Intent Understanding and Table Agents
Date: 18.11.2024
Status: Rejected

Context: 
In this chat application, we aimed to generate precise sql queries based on the user question. So we planned to use the vector database where we can save some sample questions under each indent and find which table to use for a specific user question. For the time being, we could not implement this. This method guarantees that the resulting SQL generation is contextually accurate and assists in identifying the tables that are best suited for the query.

Decision:
We decided not to use this intent matching as a pre-processing step before sending the user query for text to sql model. 

Consequences:

Pros:

It lowers the possibility of hallucinations
By reducing the size of the schema search space, intent mapping increases the SQL query's precision.

Cons:

It takes time and work to create a thorough set of training examples and specify intents.
Periodical updations for intents is necessary as use case or schema change happen.
