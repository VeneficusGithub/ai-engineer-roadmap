---
title: LLM-basiskennis
description: Hoe large language models van buitenaf werken, en hoe je er een aanroept vanuit code.
---

# LLM-basiskennis

<p class="rm-lede">Voordat je iets bouwt bovenop een LLM, moet je weten wat je aanroept: wat een token is, waarom dezelfde prompt verschillende antwoorden kan geven, hoe je betrouwbaar structured output krijgt en wat een embedding is.</p>

<div class="rm-meta" markdown>
<span>Fase 1 van 8</span>
<span>Ongeveer 2 uur</span>
<span>Bouwt voort op: je data science-achtergrond</span>
</div>

!!! curating "Zo kom je aan je API-sleutel"
    Voor de module van Anthropic in deze fase heb je een API-sleutel nodig. Die krijg je waarschijnlijk via een workspace bij Anthropic, maar die is nog niet ingericht. Zodra dat zo is, lees je hier hoe je aan je sleutel komt.

## Leren

- [Large Language Models explained briefly](https://www.youtube.com/watch?v=LPZh9BOjkQs){ .rm-item .rm-refresh data-source="Video · 3Blue1Brown" data-time="8 min" } Een korte, visuele uitleg van hoe een LLM het volgende woord voorspelt, en hoe training en transformers daarbij helpen.
- [Building with the Claude API: Getting Started with Claude](https://www.coursera.org/learn/building-with-the-claude-api#modules){ .rm-item data-source="Cursusmodule · Anthropic via Coursera" data-time="Ongeveer 2 uur" } Module 1 van de cursus: je eerste aanroepen van de Claude API in Python, gesprekken over meerdere beurten, system prompts, temperature, streaming en structured output. De cursus is gratis, maar je hebt een API-sleutel nodig; zie de melding bovenaan deze pagina.

## Interviewvragen

??? interview rm-refresh "Wat is een token, en waarom doet dat ertoe voor kosten en limieten?"
    Een token is een stukje tekst dat het model leest en schrijft, vaak een deel van een woord; in het Engels gemiddeld ongeveer vier tekens. Modellen rekenen per input- en outputtoken af, en het context window (hoeveel tekst in één verzoek past) wordt gemeten in tokens. Lange prompts en lange antwoorden kosten dus meer en kunnen tegen de limiet aanlopen.

??? interview rm-refresh "Wat doet temperature?"
    Het bepaalt hoeveel willekeur er is als het model het volgende token kiest. Een lage temperature (bijna 0) laat bijna altijd het meest waarschijnlijke token winnen, wat consistente antwoorden geeft: goed voor extractie en classificatie. Een hogere temperature spreidt de keuze, wat gevarieerdere output geeft: handig voor brainstormen. Het maakt het model niet meer of minder "correct".

??? interview rm-refresh "Hoe krijg je betrouwbaar JSON uit een LLM?"
    Gebruik de **structured output**-functie van de provider met een JSON-schema (bijvoorbeeld via Pydantic), zodat het antwoord in die vorm moet passen. Valideer het daarna alsnog in code, en bepaal wat er gebeurt als het misgaat: opnieuw proberen of terugvallen op iets anders. Alleen in de prompt om JSON vragen werkt meestal, en dat is niet goed genoeg voor productie.
