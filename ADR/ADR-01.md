Title: Balancing Precision and Memory: Why Conversations Reset After 10 Chats
Date: 15.11.2024
Status: Accepted

Context:
We typically rely on the prompt for memory in this Gen AI application. Prompts have a set token limit for each transaction, taking into account both the request and the response. We should be as specific as feasible in our prompts to avoid token limit problems and to deal with hallucinations.

Decision:
We chose an approach that summarizes each question and response. After every ten turns, the conversation begins again after the tenth interaction.

Consequences:

Pros:
It enhances the accuracy and reliability of the responses.
For every 10 interactions, the chat is reset to resist from hallucinations.
Keeping the communication as clear and concise.

Cons:
It begins a fresh conversation on the eleventh after the tenth chat's memory is full. So it is restricting us from retrieving previous memories.
