# Baseline Experiment Plan

This document proposes small baseline experiments for Tasvir Bankası. The purpose is not to establish a final benchmark, but to demonstrate that the annotation layers can be converted into measurable Turkish literary NLP tasks.

---

## 1. General evaluation principle

The first experiments should be simple, reproducible, and clearly limited.

The goal is to show that Tasvir Bankası can support task definitions such as:

- dialogue-bearing detection,
- descriptive-evidence detection,
- scene-bearing classification,
- event-bearing versus state-bearing distinction.

The first experiments should avoid overclaiming. They should be presented as baseline demonstrations, not as definitive benchmarks.

---

## 2. Recommended first task: dialogue-bearing detection

### Task

Given a Turkish literary text unit, predict whether it is dialogue-bearing.

### Why this task first?

Dialogue-bearing detection is easier to explain than more interpretive tasks such as metaphor or atmosphere detection. It also provides a useful entry point for literary NLP, character interaction analysis, and speech representation.

### Input

A text unit.

### Output

Binary label:

```text
dialogue_bearing = true / false
```

### Baselines

| Baseline | Description |
|---|---|
| Majority baseline | Always predict the majority class |
| Rule baseline | Use quotation marks, speech verbs, or dialogue punctuation |
| TF-IDF + logistic regression | Lightweight supervised text baseline |
| Turkish transformer baseline | Fine-tuned Turkish language model |
| Optional LLM zero-shot | Exploratory, not primary benchmark |

### Metrics

- accuracy,
- precision,
- recall,
- F1,
- macro-F1,
- confusion matrix.

### Error analysis questions

- Does the model miss indirect speech?
- Does it over-detect quotation-like punctuation?
- Are speech verbs reliable?
- Does reported speech cause confusion?
- Are short fragments harder than long fragments?

---

## 3. Second task: descriptive-evidence detection

### Task

Given a Turkish literary text unit, predict whether it contains descriptive evidence.

### Why this task?

This task highlights the original contribution of Tasvir Bankası. Many Turkish NLP datasets do not explicitly model description-bearing literary passages.

### Input

A text unit.

### Output

Binary label:

```text
descriptive_evidence = true / false
```

### Baselines

| Baseline | Description |
|---|---|
| Majority baseline | Always predict the majority class |
| Lexical rule baseline | Use adjective, location, object, perception, or atmosphere markers |
| TF-IDF + logistic regression | Lightweight supervised baseline |
| Turkish transformer baseline | Fine-tuned Turkish language model |

### Metrics

- precision,
- recall,
- F1,
- macro-F1.

### Error analysis questions

- Does the model confuse emotional state with description?
- Does it over-detect adjectives?
- Are spatial descriptions easier than psychological descriptions?
- Does figurative description cause false negatives?
- Do non-event passages behave differently from event-bearing passages?

---

## 4. Third task: scene-bearing versus non-scene classification

### Task

Given a text unit, predict whether it is scene-bearing or non-scene.

### Why this task?

Scene segmentation is central to computational narratology. This task tests whether the dataset can support a scene-level modeling problem.

### Input

A text unit.

### Output

Binary label:

```text
scene_bearing = true / false
```

### Baselines

- majority baseline,
- paragraph-length heuristic,
- location/person/action cue rule baseline,
- TF-IDF + logistic regression,
- Turkish transformer baseline.

### Error analysis questions

- Are descriptive scene-setting passages classified correctly?
- Are short scene fragments missed?
- Are summary passages confused with scenes?
- Do state-bearing non-event passages produce false positives?

---

## 5. Fourth task: event-bearing versus state-bearing distinction

### Task

Given a text unit, predict whether it primarily functions as event-bearing or state-bearing.

### Why this task?

This task is conceptually important because literary prose often sustains states rather than narrating actions.

### Input

A text unit.

### Output

Possible labels:

```text
event_bearing
state_bearing
mixed
other
```

### Recommended simplification

For the first baseline, reduce the task to binary classification:

```text
event_bearing = true / false
```

or:

```text
state_bearing = true / false
```

Avoid a complex multi-class setup until annotation reliability is better documented.

---

## 6. Recommended experiment order

The recommended order is:

1. Dialogue-bearing detection
2. Descriptive-evidence detection
3. Scene-bearing classification
4. Event-bearing versus state-bearing distinction

This order moves from more observable textual signals toward more interpretive narrative functions.

---

## 7. Minimal reporting template

Each experiment should be reported with the following structure:

```markdown
## Task name

### Task definition

### Dataset split

### Label definition

### Baselines

### Metrics

### Results

| Method | Accuracy | Precision | Recall | F1 | Macro-F1 |
|---|---:|---:|---:|---:|---:|

### Error analysis

### Limitations
```

---

## 8. Minimal reproducibility requirements

Each baseline experiment should specify:

- input file,
- label field,
- train/eval split,
- preprocessing,
- model or rule definition,
- random seed,
- evaluation metric,
- output report path.

Recommended output files:

```text
experiments/dialogue_bearing_baseline/
experiments/descriptive_evidence_baseline/
experiments/scene_bearing_baseline/
reports/baseline_results_v0.1.md
```

---

## 9. Suggested first implementation

The first implementation should be a simple rule baseline plus majority baseline for dialogue-bearing detection.

Reason:

- easy to explain,
- easy to reproduce,
- low computational cost,
- useful for technical report,
- avoids premature heavy model training.

Suggested rule cues:

- quotation marks,
- colon after speaker-like expression,
- speech verbs,
- question/exclamation structures near quoted text,
- reported speech markers.

The report should clearly state that this is a baseline, not a final model.

---

## 10. Recommended caution

Do not overstate the baseline results.

Correct phrasing:

> These experiments demonstrate that Tasvir Bankası annotation layers can be operationalized as measurable Turkish literary NLP tasks.

Avoid:

> These experiments establish a definitive benchmark for Turkish literary scene understanding.

---

## 11. Expected contribution to the technical report

The baseline section should support one claim:

> The dataset is not only an archival annotation resource; it can also be converted into reproducible NLP tasks.
