---
title: Agents en tool calling
description: Laat een LLM in een loop zelf bepalen welke tools het aanroept, tot een taak klaar is.
---

# Agents en tool calling

<p class="rm-lede">Met prompting vertel je een model wat het moet zeggen. Met een agent laat je het model bepalen wat het moet <em>doen</em>: het kiest een tool, leest het resultaat en herhaalt dat tot de taak klaar is. Interviewers willen horen dat je het verschil kent, en wanneer een vaste workflow de betere keuze is.</p>

<div class="rm-meta" markdown>
<span>Fase 2 van 9</span>
<span>Ongeveer 3 uur</span>
<span>Bouwt voort op: LLM-basiskennis</span>
</div>

!!! curating "Deze fase is nog niet compleet"
    Er ontbreekt nog materiaal over tool calling in code en over agent-frameworks.

## Leren

- [Generative vs Agentic AI: Shaping the Future of AI Collaboration](https://www.youtube.com/watch?v=EDb37y_MhRw){ .rm-item .rm-refresh data-source="Video · IBM Technology" data-time="7 min" } Het verschil tussen generatieve AI, die antwoord geeft op een vraag, en agentic AI, die zelfstandig stappen zet en tools gebruikt om een doel te bereiken.
- [Introduction to AI Agents](https://www.datacamp.com/courses/introduction-to-ai-agents){ .rm-item data-source="Cursus · DataCamp" data-time="1 uur 30 min" } Een conceptuele introductie zonder code: de basis van agents, ontwerppatronen en architecturen, en hoe je agents verantwoord inzet.
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents){ .rm-item .rm-refresh data-source="Artikel · Anthropic" data-time="25 min" } De helderste uitleg van workflows tegenover agents, met de gangbare patronen bij naam genoemd.
- [Designing Agentic Systems with LangChain](https://www.datacamp.com/courses/designing-agentic-systems-with-langchain){ .rm-item data-source="Cursus · DataCamp" data-time="Ongeveer 1 uur, hoofdstuk 1" } Doe hoofdstuk 1, "The Essentials of LangChain agents": tool calling en ReAct-agents met praktische oefeningen. Draait zonder API-sleutel.

## Interviewvragen

??? interview rm-refresh "Wat is het verschil tussen een LLM-workflow en een agent?"
    In een **workflow** bepaalt de developer de volgorde van stappen in code: eerst ophalen, dan samenvatten, dan classificeren. Bij een **agent** bepaalt het model tijdens het draaien de volgende stap, en dus welke tool het aanroept, op basis van wat het tot nu toe heeft gezien. Workflows zijn voorspelbaar en goedkoop; agents kunnen open taken aan, maar zijn lastiger te testen en te beheersen. Een goed antwoord voegt toe: begin met een workflow en maak een onderdeel pas agentic als de stappen echt niet vooraf te bepalen zijn.

??? interview rm-refresh "Leg uit wat er gebeurt tijdens één tool call."
    1. Je stuurt het gesprek mee, plus een lijst met toolbeschrijvingen (naam, doel, JSON-schema van de argumenten).
    2. Het model antwoordt met een tool call in plaats van tekst: de naam van de tool en de argumenten als JSON.
    3. Jouw code valideert de argumenten en voert de tool uit.
    4. Je voegt het resultaat toe aan het gesprek en roept het model opnieuw aan.
    5. Het model roept nog een tool aan of geeft het eindantwoord.

??? interview rm-refresh "Hoe voorkom je dat een agent in productie ontspoort?"
    Noem meerdere lagen: een **maximaal aantal stappen** en een budget voor tokens of kosten; **argumenten valideren** voordat je iets uitvoert; tools de **minste rechten** geven die ze nodig hebben (waar mogelijk alleen-lezen); **menselijke goedkeuring** voor onomkeerbare acties zoals e-mails versturen of betalingen doen; en **elke stap loggen** (tracing), zodat je kunt zien waarom het misging.

??? interview "Hoe schrijf je een goede toolbeschrijving?"
    Behandel het als documentatie voor een nieuwe collega: een duidelijke naam, één zin over *wanneer* je de tool gebruikt (en wanneer niet), precieze namen en types voor de argumenten, en voorbeelden van geldige waarden. Houd het aantal tools klein en hun doelen duidelijk verschillend; overlappende tools zijn de meest voorkomende reden dat een model de verkeerde kiest.
