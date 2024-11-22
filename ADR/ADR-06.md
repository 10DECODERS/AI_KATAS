Title: Evaluating Alternatives: Why the GGUF SQLCoder Model Was Not Selected
Date: 15.11.2024
Status: Accepted

Context: 

In this chat application we evaluated sqlcoder model in gguf. However, we noticed that for some complex user queries it was unable to generate the sql query accurately. So we decided to not to use the quantized model as there are some data loss in trained data when compared to the original model.

Decision:

We decided not to use the quantized sqlcoder model due to this query inaccuracy for complex queries.

Consequences:

Pros:

Avoids inaccuracies in generating sql queries
Avoids misunderstanding in context.
Cons:

If we used this means we will lesser the deployment cost.
