---
source: https://www.youtube.com/watch?v=J2rQTJby8XM
video_id: J2rQTJby8XM
channel: Data with Baraa
title: "The Data Movie | Data Literacy Explained Visually"
scraped: 2026-08-28
tags: [data literacy, data architecture, data roles, ai engineering, content]
---
# The Data Movie | Data Literacy Explained Visually

This video visually maps the modern data ecosystem, distinguishing data roles, layered data architecture, analytical foundations, and the components of AI systems.

## Procedure / models distilled
- A data analyst acts as a bridge between raw data and business decisions by answering critical business questions with data.
- Data analyst workflow: gather data from databases, spreadsheets, and APIs; clean, organize, and transform it; visualize insights; and present findings as a story to stakeholders.
- A data architect designs the blueprint of a scalable data system organized into layers such as bronze (raw data), silver (cleaned data), and gold (optimized analytics-ready data).
- A data engineer builds automated data pipelines that move data from source systems through the bronze, silver, and gold layers quickly and reliably.
- A BI developer turns one-off analyst reports into secure, interactive dashboards connected to the gold layer so they refresh automatically and remain available 24/7.
- A data scientist builds and trains predictive models to answer future-oriented questions such as churn prediction or scenario planning.
- Classify data fields as dimensions when they are used for grouping, and as measures when they are numeric and meaningful to aggregate.
- Apply separation of concerns in data architecture by assigning unique responsibilities to each layer and avoiding duplicated functionality across layers.
- Maintain a data catalog that documents tables, columns, and relationships so consumers can understand and reuse data products without repeated explanations.
- An AI engineer builds systems that connect AI models, company data, tools, and user interfaces to solve real business problems.
- Prompt engineering means communicating with AI models through detailed instructions, context, role definitions, examples, and iterative refinement.
- RAG connects company data to LLMs by converting text into embeddings, storing them in a vector database, and retrieving the closest matches via semantic search before generating a response.
- AI agents extend LLMs by first reasoning and then taking real actions such as querying databases, calling APIs, updating records, or triggering workflows.
- MCP provides a safe, standardized layer between AI agents and external systems to avoid risky direct database connections and the need to build custom connectors for every tool.

## Failure modes named
- Decisions based on opinions or gut feelings lead to confusion, wasted resources, and bad business outcomes.
- Manual data extraction by analysts does not scale and can crash systems, take hours or days, and delay answers by weeks.
- One-time analyst reports can become recurring manual work when multiple users request them daily.
- Data analysts lack the tools to answer predictive questions about the future.
- Mixing responsibilities across architecture layers violates separation of concerns and creates duplication.
- Loading some source systems directly to the silver layer while others land in bronze creates overlapping ingestion.
- Without a data catalog, every consumer repeatedly asks the same questions about columns, tables, and relationships.
- Relying solely on closed-source APIs like OpenAI means losing control, paying high token costs, and letting company data leave the environment.
- Connecting AI agents directly to production databases creates security risk.
- Building custom connectors for each external system wastes significant time and effort.

## Studio relevance
01 intake - helps the studio map a client's data ecosystem, identify the right roles and layers in play, and ask informed questions during discovery.
