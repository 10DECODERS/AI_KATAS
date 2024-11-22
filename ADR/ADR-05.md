Title: Embracing Transparency: Why We Chose Open-Source AI Models
Date: 15.11.2024
Status: Accepted

Context: 
We required an AI model to create SQL queries for structured data in our GenAI chat application. To guarantee adaptability, affordability, and compatibility with our use case, selecting the appropriate kind of AI model was essential. Because of their versatility and openness, open-source AI models have become a competitive alternative. To completely avoid data breaching.

Decision:
For our application, we choose to leverage open-source AI models. These models offer full access to their architecture, allowing for customisation and optimisation to produce SQL queries that meet the unique needs of the application.

Consequences:

Pros:

Enhance the privacy and security of the data by avoid using third party apis.
Able to fine tune in case of any specific needs.
Facilitates future expansion and flexibility by avoiding vendor lock-in.

Cons:

We should tune the prompt as precise as possible to get the feasible solution
For inference and fine-tuning, GPU infrastructure is needed, which could be expensive.
