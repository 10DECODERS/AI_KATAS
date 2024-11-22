Title: Why We Didn’t Go for Query Routing
Date: 19.11.2024
Status: Rejected
Context:
In this chat  application, we considered using query routing to dynamically distribute database queries and improve performance. However, the approach was inconsistent when generating specific routes using open-source LLMs. This made query routing unreliable for our needs, leading us to choose a simpler, more predictable query execution method instead.
Decision:
We decided not to implement query routing because its complexities, inefficiencies, and inconsistency with open-source LLMs outweighed its potential benefits for our specific use case.
Consequences:
Pros:
Simplifies the architecture by avoiding the need for an intermediary system to handle query distribution.
Reduces potential latency caused by routing queries to different systems.
Avoids the complexity of maintaining routing logic, especially as the schema evolves.
Ensures queries are directly validated and executed without unnecessary rerouting, improving performance.
Cons:
Missed opportunities for dynamic query distribution based on workload, which could optimize system performance in specific scenarios.
May limit flexibility for handling advanced database setups, such as read replicas or sharded systems, in the future.
