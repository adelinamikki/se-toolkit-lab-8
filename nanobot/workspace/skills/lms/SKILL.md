---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS skill

This skill teaches the agent how to use LMS-specific tools and how to ask follow-up questions when a lab is required.

## Available tools

- `lms_health`: check LMS backend health and item count.
- `lms_labs`: list all labs available in the LMS.
- `lms_learners`: list all learners registered in the LMS.
- `lms_pass_rates`: get pass rates for a lab.
- `lms_timeline`: get submission timeline for a lab.
- `lms_groups`: get group performance for a lab.
- `lms_top_learners`: get the top learners for a lab.
- `lms_completion_rate`: get completion rate for a lab.
- `lms_sync_pipeline`: trigger the LMS sync pipeline.

## Strategy

- If the user asks about scores, pass rates, completion, groups, timeline, top learners, or lab-specific results without naming a lab, call `lms_labs` first.
- Do not show scores or analytics tables before the user chooses a lab. The first response should be a lab selection prompt, not a score report.
- When multiple labs are available, ask the user to choose one. Use each lab title as the user-facing label and the lab identifier as the value.
- Let the shared `structured-ui` skill decide how to present the choice on supported channels.
- If the user asks for a generic overview of available labs, use `lms_labs` and summarize the results.
- If the user asks "what can you do?", explain that you can query LMS health, list labs, list learners, and fetch lab-specific analytics via the LMS tools.
- If the user asks for learner data, use `lms_learners` unless they specifically want top learners for a lab, in which case use `lms_top_learners`.

## Lab parameters

- Always treat the lab identifier as required for `lms_pass_rates`, `lms_timeline`, `lms_groups`, `lms_top_learners`, and `lms_completion_rate`.
- If the user does not provide a lab identifier, call `lms_labs` and present a lab selector.
- Prefer the lab title from `lms_labs` output as the label. If that output includes a better identifier, use it instead.

## Formatting

- Format numeric results clearly:
  - percentages as `%`
  - counts as whole numbers
  - rates as `X/Y` and percentages when available
- Keep the response concise and avoid long narrative explanations.
- If the tool result is a list, summarize the most important items first.

## Examples

- For requests about overall LMS health, use `lms_health` and report whether the backend is healthy plus the current item count.
- For requests about lab analytics without a lab name, call `lms_labs` first and ask the user to choose a lab.
- For requests about scores or completion for a specific lab, call the matching lab tool directly.
- For "what can you do?", mention the available LMS tools and note that lab-specific analytics need a lab selection.
