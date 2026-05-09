# Prompt Iterations

This document captures the evolution of the prompt used for generating structured interview summaries from raw interview transcripts.

The goal was to improve:
- consistency
- grounding
- handling of vague transcripts
- seniority inference
- reduction of hallucinations
- structured output quality

---

## Iteration 1

### Prompt

```text
Analyze the following interview transcript and provide:

1. Topics covered
2. Candidate profile
3. Candidate summary

Transcript:
{transcript}

### Input 1
#### Sample Transcript 1

### Output 1
![Iteration 1 Output](assets/Screenshot 2026-05-09 at 9.06.23 AM.png)
![Iteration 1 Outout2](assets/Screenshot 2026-05-09 at 9.06.43 AM.png)

## Iteration 2

### Prompt

```text
You are an expert interview evaluator.

Analyze the interview transcript and generate:

## Topics Covered
- Main themes discussed

## Candidate Profile
- Likely role
- Estimated seniority
- Short justification

## Candidate Summary
- Background
- Technical strengths
- Communication quality
- Potential weaknesses

IMPORTANT:
- Use only information explicitly stated or strongly implied.
- Do not hallucinate leadership experience or technical expertise.
- If information is unclear, mention uncertainty.

Transcript:
{transcript}
```
### Input 2
#### Sample Transcript 1
### Output 2
![Iteration 2 Output1](assets/Screenshot 2026-05-09 at 9.26.33 AM.png)
![Iteration 2 Output2](assets/Screenshot 2026-05-09 at 9.26.42 AM.png)

## Iteration 3 (Final Version)
### Prompt

```text
You are an expert interview analyst.

Your task is to analyze an interview transcript and generate a structured evaluation summary.

IMPORTANT RULES:
1. Only use information explicitly stated or strongly implied in the transcript.
2. Do NOT hallucinate experience, skills, or achievements.
3. If information is missing or unclear, explicitly mention uncertainty.
4. If the transcript is too short or vague, still produce the best possible analysis while acknowledging limitations.
5. Keep the tone professional, concise, and evidence-based.
6. Avoid repeating the same information across sections.

You must generate the following sections:

# 1. Topics Covered
Identify the major themes discussed during the interview.
Use concise bullet points.

Examples:
- System design
- Leadership experience
- Team collaboration
- Machine learning fundamentals
- Conflict resolution
- Career goals

# 2. Candidate Profile
Infer the most suitable candidate profile based on the transcript.

Include:
- Likely role
- Approximate seniority level
- Short justification (2–4 sentences)

Examples:
- Backend Engineer — Mid-Level
- Data Scientist — Junior
- Product Manager — Senior

Be careful with seniority assumptions.
If uncertain, explicitly say so.

# 3. Candidate Summary
Write a concise summary (3–6 sentences) covering:
- Background
- Strengths
- Communication quality
- Technical or domain strengths
- Potential concerns or gaps
- Overall impression

If weaknesses are identified, present them professionally and constructively.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

## Topics Covered
- topic 1
- topic 2

## Candidate Profile
Role: ...

Justification:
...

## Candidate Summary
...

INTERVIEW TRANSCRIPT:
--------------------
{transcript}
```
### Input 3
#### Sample Transcript 1

### Output 3
![Iteration 3 Output1](assets/Screenshot 2026-05-09 at 9.28.40 AM.png)

The final prompt worked well across both provided transcripts because it balanced:

structure
grounding
inference flexibility
concise formatting

The biggest improvement came from explicitly restricting hallucinations while still allowing reasonable inference from candidate responses.

I also found that preserving transcript formatting and speaker structure improved output quality significantly compared to aggressively compressing the transcript before prompting.

### Iteration 1

    * Too generic and overly confident.

### Iteration 2

    * Better grounding but too conservative.

### Iteration 3

    * Balanced recruiter-style evaluation with stronger structure and evidence-based reasoning.