# Workflow — Diagnose an Archetype

Use when: a problem recurs, effort produces plateau, a fix made it worse,
or "why does this keep happening" is the question.

1. Write the symptom in plain words — verbs and nouns, no jargon:
   e.g. "quick fix works, problem returns worse, we depend on the vendor".
2. Run `studio map "<symptoms>"`. Take the top suspect seriously even if
   it stings (the diagnosis usually names a structure someone owns).
3. Read the archetype: `studio archetype <id>`. Check the story against
   your situation; check the counterintuitive point explicitly — it is the
   sentence most likely to be true and least likely to be believed.
4. Verify with stocks/flows: name the stock the archetype predicts
   (e.g. Shifting-the-Burden predicts an atrophying internal-capability
   stock; Limits-to-Growth predicts a binding resource). If that stock
   is not measurably moving, suspect a different archetype.
5. Check the corpus for prior art: `studio search "<archetype> <domain>"`
   and `studio cards systems-thinking --grep <domain keyword>`.
6. Prescribe per the archetype's intervention — then add the discipline:
   - symptomatic fix? sunset clause + instrumented side effect.
   - fundamental fix? schedule and owner for the slow loop.
7. Report format:
   - Suspect: <archetype> (confidence, matched symptoms)
   - Stock evidence: <numbers/trend>
   - Counterintuitive check: <the uncomfortable sentence, and whether we accept it>
   - Intervention: <action + leverage rank + owner>
   - Falsifier: <observation within N weeks that kills this diagnosis>
