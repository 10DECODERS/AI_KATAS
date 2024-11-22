Title: Saving the column descriptions in vector database
Date: 18.11.2024
Status: Proposed
Context:
In the suggested method, column descriptions are created for every database table and saved in a vector database. The necessary tables would be found during query routing, and the vector database's column descriptions would be taken out to help with SQL query generation. This method uses thorough column descriptions taken from sample data to increase accuracy, especially when working with categorical data.
Decision:
Due to implementation complexity and scheduling restrictions, this technique is currently rejected. Without incorporating a vector database for column descriptions at this time, the team will concentrate on quicker, easier ways to increase the accuracy of query creation.
Consequences:
Pros:
More thorough column descriptions may help the model comprehend the data schema better, resulting in SQL queries that are more accurate.
The handling of particular data types may be further enhanced by using sample data to identify columns as categorical.
Cons:
Current project timeframes cannot accommodate the resource-intensive task of creating and maintaining column descriptions for every table.
The vector database would need to be updated in order to implement any schema changes, which would increase operational complexity.
