# Annotation Layer Guide

This document explains the main annotation layers used in Tasvir Bankası. It is intended for external readers who want to understand what a structured JSONL record represents before requesting access to the full gated dataset.

---

## 1. Record-level concept

A Tasvir Bankası record represents a literary text unit enriched with narrative and linguistic metadata.

A record is not merely a raw passage. It is a structured observation about the narrative function of that passage.

A single text unit may be:

- scene-bearing,
- state-bearing,
- dialogue-bearing,
- tense-bearing,
- description-bearing,
- or a combination of these.

---

## 2. Scene-bearing textual units

### Purpose

The scene layer identifies whether a text unit participates in a scene or scene-adjacent structure.

### Typical evidence

- a stable setting,
- one or more characters situated in time and space,
- action unfolding within a local narrative frame,
- transition into or out of a scene,
- perceptual or descriptive anchoring.

### Important distinction

A scene-bearing unit is not necessarily action-heavy. A passage may be scene-relevant because it establishes the physical, psychological, or atmospheric conditions of a scene.

---

## 3. State-bearing textual units

### Purpose

The state layer captures passages that encode psychological, emotional, social, physical, or situational states.

### Typical evidence

- fear, hesitation, desire, fatigue, grief, uncertainty,
- social status,
- bodily condition,
- atmosphere of waiting,
- moral pressure,
- conflict without immediate action.

### Why this matters

Many literary passages are meaningful because they sustain a state rather than narrate an event. A purely event-based annotation model would underrepresent such passages.

---

## 4. Dialogue-bearing textual units

### Purpose

The dialogue layer marks speech-related evidence.

### Typical evidence

- direct speech,
- indirect speech,
- reported speech,
- speech verbs,
- addressee signals,
- turn-taking signals,
- quoted utterances,
- dialogue-adjacent narration.

### Important distinction

Dialogue-bearing does not always mean that a passage contains quotation marks. Turkish literary prose may contain reported, indirect, or embedded speech.

---

## 5. Tense-bearing textual units

### Purpose

The tense layer records temporal and tense-related evidence.

### Typical evidence

- past tense narration,
- present tense narration,
- habitual forms,
- reported past,
- conditional forms,
- narrative time shifts,
- temporal anchoring expressions.

### Why this matters for Turkish

Turkish morphology encodes tense, aspect, modality, evidentiality, and person in ways that are important for literary narration. Tense annotation helps preserve this narrative signal.

---

## 6. Morphology-oriented evidence

### Purpose

The morphology layer preserves linguistically relevant features that may support later NLP analysis.

### Possible evidence

- finite verb presence,
- verbal noun or participial forms,
- tense/aspect/modality markers,
- person marking,
- evidential markers,
- negation,
- derivational forms,
- suffix-based reference signals.

### Role in the dataset

Morphology is not treated as decoration. It supports interpretation of action, state, dialogue, tense, and implicit reference.

---

## 7. Descriptive evidence

### Purpose

The descriptive profile captures textual evidence that contributes to description.

### Typical evidence

- spatial description,
- atmosphere,
- physical objects,
- bodily description,
- environmental detail,
- perceptual evidence,
- figurative or comparison-based description,
- scene-setting description.

### Important distinction

Description is not simply “non-action.” In literary prose, description may carry narrative function by establishing mood, character perception, social position, symbolic environment, or scene transition.

---

## 8. Enriched descriptive evidence

### Purpose

The enriched descriptive layer records additional descriptive signals after filtering or enrichment.

### Possible uses

- distinguishing true descriptive evidence from lexical false positives,
- identifying description-bearing units with stronger confidence,
- flagging metaphor-like or comparison-like evidence,
- preserving annotation decisions for later inspection.

### Caution

Fields such as metaphor-related markers should be interpreted as evidence signals. They should not be treated as a complete literary theory or conceptual metaphor analysis.

---

## 9. Selection metadata

### Purpose

Selection metadata records the status of a record within the dataset construction and validation workflow.

### Possible functions

- split assignment,
- validation status,
- source tracking,
- selection reason,
- release-readiness status,
- public-preview versus full-dataset distinction.

### Why this matters

Selection metadata allows users to understand whether a record is part of a public smoke/probe subset, a train split, a curated evaluation seed, or another release category.

---

## 10. Curation ledger

### Purpose

The curation ledger records cases that required human review or semantic judgment.

### Typical decisions

- false positive removal,
- true metaphor marker resolution,
- gold-eval approval,
- ambiguous label confirmation,
- label correction,
- release-readiness decision.

### Why this matters

Literary annotation contains ambiguity. The curation ledger makes these judgments visible instead of hiding them inside final labels.

---

## 11. Event-bearing and non-event distinction

### Event-bearing unit

A text unit that represents an action, occurrence, or narrative event.

### Non-event unit

A text unit that represents state, description, emotion, atmosphere, or structural narrative material without a conventional event.

### Two-regime rule

The validation policy should not reject valid non-event descriptive or state-bearing units merely because they do not have a conventional event summary.

---

## 12. Example interpretation

A passage describing a dim room, a silent character, and a feeling of unease may be:

- scene-bearing because it establishes a location,
- state-bearing because it marks psychological tension,
- descriptive-evidence-bearing because it describes atmosphere and space,
- tense-bearing because it contains finite verbs or tense markers,
- non-event-bearing if no explicit action occurs.

This is why Tasvir Bankası uses layered annotation rather than a single label.

---

## 13. Summary

Tasvir Bankası models Turkish literary prose as layered narrative evidence.

The central idea is:

> A literary passage may function as scene, state, dialogue, time, morphology, description, or several of these at once.

This layered model is the main contribution of the project.
