---
title: LLM-security
description: Hoe LLM-applicaties worden aangevallen, en hoe je de schade beperkt.
---

# LLM-security

<p class="rm-lede">Het traineeship behandelde security in het algemeen. LLM's brengen nieuwe problemen mee: tekst in een document kan een instructie worden, en een model kan lekken wat het te zien kreeg. Deze fase behandelt de risico's die interviewers je verwachten te kunnen noemen.</p>

<div class="rm-meta" markdown>
<span>Fase 7 van 8</span>
<span>Ongeveer 3 uur</span>
<span>Bouwt voort op: de securitymodule van het traineeship</span>
</div>

## Leren

- [OWASP's Top 10 Ways to Attack LLMs: AI Vulnerabilities Exposed](https://www.youtube.com/watch?v=gUNXZMcd2jU){ .rm-item .rm-refresh data-source="Video · IBM Technology" data-time="25 min" } Een rondgang langs de OWASP Top 10 voor LLM-applicaties: hoe elke aanval werkt en hoe je je ertegen verdedigt.
- [AI Security: Defend LLM Apps Against the OWASP LLM Top 10](https://www.udemy.com/course/ai-security-defend-llm-apps-against-the-owasp-llm-top-10/){ .rm-item data-source="Cursus · Udemy" data-time="Ongeveer 1 uur 50 min, geselecteerde secties" } Volgt de OWASP-lijst van 2025, met per risico een uitleg en een lab. Let op: de cursus is nieuw en heeft nog geen reviews.
- [Lakera Agent Breaker](https://play.lakera.ai/agent-breaker){ .rm-item .rm-exercise data-source="Oefening · Lakera" data-time="30–45 min" } Probeer in de browser agents te misleiden met prompt injection. Er is geen sleutel of installatie nodig.

## Interviewvragen

??? interview rm-refresh "Wat is prompt injection?"
    Tekst die het model als instructie behandelt, terwijl die uit een onbetrouwbare bron komt: een gebruikersbericht, een webpagina, een e-mail of een opgehaald document. "Negeer je eerdere instructies en…" is het klassieke voorbeeld. *Indirecte* prompt injection, verstopt in content die de applicatie ophaalt, is het lastigere geval, omdat de gebruiker het nooit heeft getypt.

??? interview rm-refresh "Hoe verdedig je je tegen prompt injection?"
    Er bestaat geen volledige oplossing, dus beperk wat een geslaagde aanval kan aanrichten: geef het model en zijn tools de **minste rechten**, vraag **menselijke goedkeuring** voor risicovolle acties, houd onbetrouwbare content duidelijk gescheiden van instructies, **valideer output** voordat je erop handelt, en monitor op ongebruikelijk gedrag. Zeg er duidelijk bij dat alleen prompts filteren niet genoeg is.

??? interview rm-refresh "Welke privacykwesties spelen er als je data naar een LLM-provider stuurt?"
    Persoonsgegevens of vertrouwelijke data verlaten je omgeving, dus je moet weten waar ze worden verwerkt (in de EU?), of de provider ze opslaat of erop traint, en of dat past binnen de AVG en de contracten met je klant. Maatregelen: zakelijke overeenkomsten zonder training op jouw data, hosting in de EU, en persoonsgegevens verwijderen voordat ze worden verstuurd.
