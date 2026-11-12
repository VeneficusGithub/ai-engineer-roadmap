---
title: Multi-agent systemen
description: Meerdere agents die samenwerken, en waarom dat vaak niet het antwoord is.
---

# Multi-agent systemen

<p class="rm-lede">Multi-agent systemen verdelen een taak over meerdere gespecialiseerde agents. Ze kunnen grote, parallelle onderzoekstaken aan, maar vermenigvuldigen ook de kosten en het aantal plekken waar het mis kan gaan. Interviewers willen vooral horen dat je weet wanneer je ze <em>niet</em> moet gebruiken.</p>

<div class="rm-meta" markdown>
<span>Fase 5 van 8</span>
<span>Ongeveer 1 uur</span>
<span>Bouwt voort op: agents</span>
</div>

## Leren

- [Multi-Agent Systems Explained](https://www.youtube.com/watch?v=sWH0T4Zez6I){ .rm-item .rm-refresh data-source="Video · IBM Technology" data-time="8 min" } Een korte uitleg van hoe meerdere agents samenwerken.
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system){ .rm-item data-source="Artikel · Anthropic" data-time="15 min" } Hoe Anthropic een orchestrator met parallelle subagents bouwde, waarom dat ongeveer 15 keer zoveel tokens kost als een chat, en waarom het slecht past bij taken waarin agents van elkaar afhangen.
- [Introduction to subagents](https://anthropic.skilljar.com/introduction-to-subagents){ .rm-item data-source="Cursus · Anthropic Academy" data-time="40 min" } Wanneer subagents helpen en wanneer niet, met veelgemaakte fouten om te vermijden. De cursus is gratis en gaat over Claude Code: de lessen volg je zonder API-sleutel, maar zelf proberen vraagt om toegang tot Claude Code.

## Interviewvragen

??? interview rm-refresh "Wanneer zou je meerdere agents gebruiken in plaats van één?"
    Als een taak uiteenvalt in **onafhankelijke delen die parallel kunnen draaien**, zoals meerdere onderwerpen tegelijk onderzoeken, of als de context van één agent zou overlopen. Elke sub-agent werkt in zijn eigen context en geeft een korte samenvatting terug aan een orchestrator. Voor taken waarin elke stap afhangt van de vorige is één agent eenvoudiger en betrouwbaarder.

??? interview rm-refresh "Wat zijn de nadelen van multi-agent systemen?"
    Veel hogere **tokenkosten** (elke agent heeft zijn eigen context), meer **plekken waar het misgaat**, agents die werken met **inconsistente informatie**, en veel lastiger **debuggen** en evalueren. Veel problemen die multi-agent lijken, los je beter op met één agent met goede tools, of met een vaste workflow.

??? interview rm-refresh "Beschrijf het orchestrator–worker-patroon."
    Een **orchestrator**-agent deelt de taak op in deeltaken, geeft elke deeltaak aan een **worker**-agent (vaak parallel) en voegt de resultaten samen. Workers krijgen alleen de context die ze voor hun deel nodig hebben. De orchestrator beslist of het samengevoegde resultaat goed genoeg is of dat er meer werk nodig is.
