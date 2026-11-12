---
title: RAG en vectordatabases
description: Laat een LLM vragen over je eigen documenten beantwoorden door eerst de relevante delen op te halen.
---

# RAG en vectordatabases

<p class="rm-lede">Met retrieval-augmented generation laat je een LLM vragen over je eigen documenten beantwoorden. In plaats van te hopen dat het model het antwoord weet, doorzoek je eerst je eigen documenten en geef je het model de relevante passages om op te antwoorden.</p>

<div class="rm-meta" markdown>
<span>Fase 4 van 8</span>
<span>Ongeveer 4 uur</span>
<span>Bouwt voort op: LLM-basiskennis</span>
</div>

!!! curating "Deze fase is nog niet compleet"
    Er ontbreekt nog materiaal over vectordatabases en RAG-evaluatie.

## Leren

- [What is Retrieval-Augmented Generation (RAG)?](https://www.youtube.com/watch?v=T-D1OfcDW1M){ .rm-item .rm-refresh data-source="Video · IBM Technology" data-time="7 min" } Een korte uitleg van waarom een LLM zonder RAG verouderde of verzonnen antwoorden geeft, en hoe ophalen uit je eigen bronnen dat oplost.
- [Retrieval Augmented Generation (RAG) with LangChain](https://www.datacamp.com/courses/retrieval-augmented-generation-rag-with-langchain){ .rm-item data-source="Cursus · DataCamp" data-time="Ongeveer 2 uur, hoofdstuk 1–2" } Bouw een RAG-toepassing met LangChain en verbeter daarna de architectuur. Hoofdstuk 3 (Graph RAG) kun je overslaan. Draait zonder API-sleutel.
- [Building with the Claude API: RAG and Agentic Search](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287763){ .rm-item data-source="Cursusmodule · Anthropic Academy" data-time="Ongeveer 2 uur" } Chunkingstrategieën, embeddings, de volledige RAG-flow, zoeken op trefwoorden met BM25 en een pipeline met meerdere indexen. Vereist een API-sleutel. Anthropic heeft geen eigen embeddingmodel, dus daarvoor gebruik je een andere aanbieder of een gratis model op je eigen laptop.

## Interviewvragen

??? interview rm-refresh "Leg RAG uit aan een niet-technische stakeholder."
    Het model is als een slimme nieuwe collega die onze documenten nog nooit heeft gezien. RAG betekent: voordat die collega antwoord geeft, zoekt hij eerst de meest relevante pagina's op in ons archief en baseert hij zijn antwoord daarop, het liefst met bronvermelding. Zo blijven antwoorden gebaseerd op onze eigen informatie en actueel, zonder het model opnieuw te trainen.

??? interview rm-refresh "Hoe kies je een chunkgrootte?"
    Er is geen universeel beste grootte; het is een afweging. Kleine chunks matchen precies met vragen maar verliezen context; grote chunks houden context vast maar verwateren de match en nemen meer van de prompt in beslag. Begin bij de structuur van het document (alinea's, secties), voeg wat overlap toe en **meet** daarna de kwaliteit van het ophalen op echte vragen met een paar groottes, in plaats van te gokken.

??? interview rm-refresh "Je RAG-systeem geeft verkeerde antwoorden. Hoe zoek je uit waarom?"
    Splits het probleem in tweeën. Controleer eerst het **ophalen**: werden voor de foute vragen de juiste passages überhaupt opgehaald? Zo niet, kijk dan naar chunking, het embeddingmodel, of voeg zoeken op trefwoorden (hybrid) en reranking toe. Als de juiste passages *wel* werden opgehaald, zit het probleem in het **genereren**: de prompt, het model, of te veel irrelevante context. Maak een kleine set testvragen met bekende antwoorden, zodat je elke verbetering kunt meten.
