---
title: MCP en skills
description: Standaardmanieren om agents tools, data en instructies te geven.
---

# MCP en skills

<p class="rm-lede">MCP is een standaardmanier om tools en databronnen aan elke AI-applicatie te koppelen; skills zijn verpakte instructies die een agent pas laadt als hij ze nodig heeft.</p>

<div class="rm-meta" markdown>
<span>Fase 3 van 9</span>
<span>Ongeveer 9,5 uur</span>
<span>Bouwt voort op: agents en tool calling</span>
</div>

!!! curating "Deze fase is nog niet af"
    De DataCamp-cursus, de workshop en de module van Anthropic Academy overlappen elkaar.

## Leren

- [Agent Skills vs MCP: What's the difference?](https://www.youtube.com/watch?v=6wdvSH61xGw&t=48s){ .rm-item .rm-refresh data-source="Video · Shaw Talebi" data-time="Ongeveer 20 min, vanaf 0:48" } Wat MCP en skills elk doen, waar ze verschillen en wanneer je welke gebruikt.
- [Introduction to Model Context Protocol (MCP)](https://www.datacamp.com/courses/introduction-to-model-context-protocol-mcp){ .rm-item data-source="Cursus · DataCamp" data-time="3 uur 11 min" } Bouw MCP-servers en koppel ze aan een LLM-toepassing, met oefeningen in de browser. Draait zonder API-sleutel.
- [Using and building MCP servers](https://pamelafox.github.io/github-copilot-mcp-tutorial/){ .rm-item .rm-exercise data-source="Workshop · Pamela Fox" data-time="Ongeveer 1 uur 50 min" } Verbind Copilot met bestaande MCP-servers en bouw zelf een Python-server met FastMCP. Werkt met het gratis Copilot-abonnement; test eerst of alles bij jou werkt.
- [Building with the Claude API: Model Context Protocol](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287780){ .rm-item data-source="Cursusmodule · Anthropic Academy" data-time="Ongeveer 2 uur" } Bouw een eigen MCP-server met tools, resources en prompts, en de client die ermee praat. Vereist een API-sleutel.
- [Agent Skills with Anthropic](https://www.deeplearning.ai/courses/agent-skills-with-anthropic){ .rm-item data-source="Cursus · DeepLearning.AI" data-time="2 uur 19 min" } Hoe skills werken, hoe ze zich verhouden tot tools, MCP en subagents, en hoe je ze zelf bouwt. Video's kijken kan gratis; de quiz vraagt om DeepLearning.AI Pro, en de lessen over de Claude API en de Agent SDK zelf nadoen om een API-sleutel.

## Interviewvragen

??? interview rm-refresh "Welk probleem lost MCP op?"
    Zonder standaard heeft elke AI-applicatie een eigen maatwerkkoppeling nodig voor elke tool of databron. MCP definieert één protocol: je bouwt één keer een **MCP-server** (bijvoorbeeld voor je database of ticketsysteem), en elke MCP-compatibele client (Claude, Copilot, je eigen agent) kan hem gebruiken. Het wordt vaak vergeleken met USB-C voor AI-tools.

??? interview rm-refresh "Wat is het verschil tussen een tool, een MCP-server en een skill?"
    Een **tool** is één functie die het model kan aanroepen. Een **MCP-server** is een programma dat een set tools (en data) aanbiedt aan elke compatibele client via een standaardprotocol. Een **skill** is een map met instructies, en eventueel scripts, die een agent vertelt *hoe* hij een bepaald soort taak uitvoert; de agent laadt hem alleen als dat relevant is, wat zijn context klein houdt.

??? interview rm-refresh "Wat zijn de securityrisico's van een MCP-server koppelen?"
    Een MCP-server kan code uitvoeren en bij data komen met alle rechten die je hem geeft, en zijn toolbeschrijvingen zijn tekst die het model leest. Een kwaadaardige of gecompromitteerde server kan dus instructies injecteren. Gebruik alleen servers die je vertrouwt, geef ze minimale rechten en controleer welke tools ze aanbieden.
