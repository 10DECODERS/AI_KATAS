Title: Why We Choose a Specific Prompt: A Chain of Thought (CoT) Approach
Date: 18.11.2024
Status: Accepted
Context:
In this chat application, we adopted the Chain of Thought (CoT) prompting technique to enhance the model's reasoning and step-by-step problem-solving capabilities. CoT prompts guide the model to break down complex tasks into sequential steps, reducing ambiguity and improving accuracy, particularly for multi-step or reasoning-heavy queries.
Decision:
We chose the CoT prompting strategy because it encourages structured thinking and enhances the model's ability to solve problems that require logical progression or reasoning. This approach contrasts with direct-answer prompts, which can lead to oversimplification or hallucinations in the responses.
Consequences:
Pros:
Improved Accuracy: CoT prompts help the model handle multi-step queries effectively by focusing on intermediate reasoning steps.
Transparency in Reasoning: Users can follow the logical flow of the solution, increasing trust and interpretability.
Reduced Errors: By explicitly breaking down problems, the model avoids common pitfalls like overlooking details or jumping to conclusions.
Cons:
Longer Responses: CoT generates more verbose outputs, which may not be ideal for scenarios requiring concise answers.
Increased Latency: Additional reasoning steps result in slightly slower response times.
Complexity in Prompt Design: Crafting effective CoT prompts requires careful design to ensure the model interprets them as intended.

ADR-011:Title: Why We Are Not Using LangChain
Date: 18.11.2024
Status: Accepted
Context:
In this chat application, we evaluated the use of LangChain for managing complex workflows, chaining calls between models, and handling interactions with external systems like databases or APIs. While LangChain is a powerful tool for such purposes, we found it unsuitable for our specific requirements due to its overhead and the need for tighter control over our application's logic and execution.
Decision:
We decided not to use LangChain and instead opted for custom-built workflows tailored to our application’s needs. This approach provides greater flexibility and performance optimization, aligning better with our goals.
Consequences:
Pros:
Tailored Solution: A custom-built workflow ensures greater alignment with our specific use cases and avoids unnecessary abstraction layers.
Reduced Overhead: Avoids the additional complexity and resource usage introduced by LangChain, leading to faster performance.
Flexibility: Provides direct control over model interactions, database queries, and API calls, enabling more precise optimizations.
Cons:
Development Time: Building and maintaining custom workflows requires more initial effort and ongoing support.
Less Out-of-the-Box Functionality: LangChain provides ready-made tools for tasks like document retrieval or memory management, which must now be implemented independently.
Steeper Learning Curve for Custom Approaches: Developers may need to spend extra time creating and documenting workflows for maintainability.
