# Tasvir Bankası: A Turkish Literary Scene-State-Description Dataset and Annotation Pipeline for Computational Narratology

**Author:** Furkan Yaşar  
**Release context:** Hugging Face gated dataset + GitHub public-preview pipeline + Zenodo publication record  
**Report type:** Technical report / preprint draft  
**Version:** Draft v0.1  
**Date:** 2026-06-07  

---

## Abstract

Tasvir Bankası is a Turkish literary annotation resource and reproducible pipeline for transforming rights-reviewed public-domain candidate Turkish prose into structured JSONL records. The project addresses a gap in Turkish literary NLP: while Turkish has important resources for syntax, morphology, semantic roles, discourse relations, named entities, and historical-language processing, there are few openly documented resources that model Turkish literary prose as layered narrative data. Tasvir Bankası represents literary text units through scene segmentation, state-bearing units, dialogue signals, tense/morphology, descriptive evidence, validation metadata, and curation-ledger decisions. Its main contribution is not the release of raw Turkish prose, but the conversion of literary prose into structured records suitable for computational narratology, digital humanities, annotation research, and non-commercial Turkish literary NLP. The full dataset is distributed as a gated non-commercial Hugging Face release; the GitHub repository provides the public-safe pipeline, schema, validation tools, documentation, and limited smoke/probe samples; and Zenodo provides the DOI-backed publication record. This report describes the research motivation, annotation model, pipeline boundary, validation policy, access design, limitations, and future evaluation plan for Tasvir Bankası.

**Keywords:** Turkish literary NLP; computational narratology; scene segmentation; literary annotation; descriptive evidence; Turkish prose; JSONL dataset; digital humanities; annotation pipeline.

---

## 1. Introduction

Literary prose contains information that is not captured adequately by treating text as an undifferentiated sequence of tokens. A passage may establish a scene, sustain an emotional state, mark a shift in narrative time, present direct or indirect speech, describe a physical environment, encode bodily or psychological conditions, or prepare a narrative function without presenting a conventional event. These phenomena are especially important in computational narratology and digital humanities, where the unit of analysis is not always a sentence, document, topic, or named entity, but often a scene, a state, a descriptive passage, a dialogue unit, or a transition between narrative functions.

Turkish literary prose is a particularly rich case for such work. Turkish morphology carries tense, aspect, modality, evidentiality, person, negation, and derivational information in compact forms. Literary narration may use implicit subjects, reported speech, verbal nouns, participles, embedded clauses, and tense shifts in ways that matter for interpretation. A dataset that only preserves raw text or document-level metadata cannot expose these narrative and linguistic layers systematically.

Tasvir Bankası is designed as a response to this representational gap. It models Turkish literary prose as structured JSONL records enriched with annotation layers for scene, state, dialogue, tense/morphology, descriptive evidence, source tracking, validation status, and curation decisions. The project’s public release is deliberately separated into three surfaces:

1. **Hugging Face gated dataset package:** the full non-commercial dataset release.
2. **GitHub public-preview pipeline package:** the public-safe pipeline, schemas, validators, documentation, and limited smoke/probe samples.
3. **Zenodo publication record:** the DOI-backed citation and manifest surface.

This separation is central to the project’s design. The dataset concerns literary material and therefore requires careful access, license, and source-rights framing. The GitHub repository is not the full dataset payload; it is the reproducibility and documentation surface for the annotation pipeline.

The current dataset card describes Tasvir Bankası as a gated non-commercial research dataset for Turkish literary scene, state, and description annotation, providing structured JSONL records derived from rights-reviewed public-domain candidate Turkish prose and including segmentation, dialogue, tense, scene-boundary, state, and descriptive evidence fields [R1]. The same card reports current release metrics of 2,172 train records, 92 curated gold-eval records, 98 curation-ledger records, and zero pending records [R1]. The GitHub release surface documents the public-safe pipeline package, including pipeline scripts, JSON schema files, validation tools, documentation, source-rights review materials, and limited gold-smoke and two-regime probe samples [R2].

The purpose of this report is to place those release surfaces into a coherent technical and academic argument. It explains why the project matters, what the annotation model represents, how the pipeline and validation policy are organized, what the release does and does not claim, and which next evaluation steps would make the resource stronger.

---

## 2. Motivation: Why Turkish Literary NLP Needs Layered Narrative Annotation

Turkish NLP already contains several important resource families. Universal Dependencies provides syntactic annotation for Turkish, including multiple Turkish treebanks [R7]. Turkish PropBank / TRopBank provides predicate-argument information for Turkish verbs and semantic roles [R8]. Turkish FrameNet resources support frame-semantic representation [R9]. Turkish Discourse Bank provides discourse-relation annotation for Turkish texts [R10]. Historical Turkish and Ottoman Turkish have also received new foundational resources, including HisTR, OTA-BOUN, and the Ottoman Text Corpus [R6]. These resources are valuable foundations for linguistic NLP.

However, literary prose asks a different question. It is not sufficient to know only which token is a verb, which argument is an agent, or which discourse connective links two spans. Those analyses are necessary, but they do not directly answer literary-narrative questions such as:

- Is this passage functioning as a scene?
- Is it event-bearing or state-bearing?
- Does it establish atmosphere or physical setting?
- Does it contain direct, indirect, or speech-adjacent dialogue?
- Does it shift narrative time or tense?
- Does it describe a character, object, environment, or psychological condition?
- Is the passage meaningful even when it lacks a conventional event summary?

Existing literary NLP work in other languages demonstrates that these questions require specialized annotation. Scene segmentation has been introduced as a narrative-text segmentation task where scenes are characterized by continuity of narrated time, location, action focus, and character constellation [R3]. SceneML and ScANT model narrative scenes through explicit scene annotation frameworks [R4]. Quotation-attribution resources such as the Project Dialogism Novel Corpus annotate literary quotations for speaker, addressee, quotation type, referring expression, and character mentions [R5]. Recent narrative datasets such as Annotated Mystery Narratives include scene-level and narrative-level segmentation, as well as genre-specific tags such as clues and detective thoughts [R11]. These resources show that literary NLP often needs annotation units and labels that are specific to narrative form, not merely general syntax or classification.

Tasvir Bankası brings this general insight into Turkish literary prose. It does not attempt to replace Turkish UD, PropBank, FrameNet, Discourse Bank, or historical Turkish resources. Instead, it complements them by defining a narrative-layer representation: a passage can be scene-bearing, state-bearing, dialogue-bearing, tense-bearing, morphology-bearing, and descriptive-evidence-bearing at the same time.

The central claim is therefore methodological:

> Turkish literary prose should be represented not only as raw text, but as layered narrative evidence.

This claim is important for both computational and literary reasons. Computationally, structured JSONL records make it possible to define reproducible tasks such as dialogue-bearing detection, descriptive-evidence detection, scene-bearing classification, or event/state distinction. Literarily, the model respects the fact that many passages in prose are meaningful precisely because they are descriptive, atmospheric, psychological, or state-oriented rather than event-heavy.

---

## 3. Related Work

### 3.1 Scene segmentation and narrative annotation

Scene segmentation in fiction has been described as a task of dividing narrative text into scenes. Zehe et al. define a scene as a segment in which narrated time and discourse time are approximately aligned, the narration focuses on one action and location, and character constellations remain stable [R3]. This definition is useful for Tasvir Bankası because it gives scene annotation a technical basis: a scene is not just a paragraph, and it is not merely a topic segment. It is a narrative unit involving time, place, action focus, and character configuration.

SceneML and ScANT provide another relevant point of comparison. ScANT is a small corpus of scene-annotated narrative texts based on SceneML, an evolving framework for annotating scenes in narrative text [R4]. While ScANT is not Turkish, it is important because it demonstrates the feasibility of manually structured scene annotation and makes scene annotation a shareable dataset object.

Annotated Mystery Narratives extends this direction by combining narrative and scene-level annotation with genre-specific narrative tags such as acts, detective thoughts, clues, and other mystery-story functions [R11]. This is relevant to Tasvir Bankası because it shows that literary annotation can combine general narrative segmentation with domain-specific function labels.

Tasvir Bankası differs from these resources in language and layer focus. Its primary object is Turkish literary prose, and its distinctive emphasis is the scene-state-description triad: it explicitly preserves descriptive and state-bearing passages rather than forcing all records into an event-centered model.

### 3.2 Dialogue and quotation annotation in literary texts

Dialogue is a central component of literary structure. The Project Dialogism Novel Corpus (PDNC) provides a strong model for quotation attribution in English literary texts. It contains annotations for 35,978 quotations across 22 novels, including speaker, addressee, quotation type, referring expression, and character mentions [R5]. This kind of annotation demonstrates that literary dialogue requires more than detecting quotation marks; it requires tracking who speaks, to whom, how speech is introduced, and how characters are referred to inside and around the quotation.

Tasvir Bankası’s dialogue layer is less specialized than PDNC’s quotation-attribution framework, but it serves a related purpose: it identifies dialogue-bearing or speech-related evidence inside Turkish literary text units. For Turkish, this is particularly important because reported speech, embedded speech, indirect speech, and speech-adjacent narration may not be reducible to visible quotation punctuation.

### 3.3 Turkish NLP foundations

Turkish has multiple syntactic and semantic resources that can support later enrichment of Tasvir Bankası. Universal Dependencies lists multiple Turkish treebanks, including Turkish-BOUN, Turkish-IMST, Turkish-FrameNet, Turkish-PUD, and others [R7]. Turkish PropBank / TRopBank v2.0 provides predicate-argument information and semantic role annotation for Turkish verbs, with a much larger Turkish verb inventory than its earlier version [R8]. Turkish FrameNet aims to build a comprehensive Turkish frame-semantic resource compatible with Turkish PropBank and related lexical resources [R9]. Turkish Discourse Bank models Turkish discourse relations, including explicitly or implicitly conveyed relations [R10].

These resources are not literary scene datasets. Their relevance is infrastructural. They can support future versions of Tasvir Bankası by enriching predicate-argument structure, semantic frames, discourse relations, and syntactic analysis. In other words, they help answer questions inside a text unit; Tasvir Bankası asks how the text unit functions in literary narration.

### 3.4 Historical Turkish and Ottoman Turkish resources

Historical Turkish and Ottoman Turkish resources are especially relevant because Turkish literary prose often includes diachronic, orthographic, lexical, and stylistic variation. Recent work by Özateş et al. introduces foundational NLP resources and models for historical Turkish, including HisTR, OTA-BOUN, and the Ottoman Text Corpus [R6]. These resources show that historical Turkish NLP is becoming more structured and that future literary-NLP work can draw on NER, dependency parsing, POS tagging, and transliterated historical corpora.

Tasvir Bankası is compatible with this trajectory but focuses on a different representational layer. Where historical Turkish resources provide linguistic infrastructure, Tasvir Bankası provides narrative-function annotation for literary prose.

---


## 3A. Source Corpus Rationale: Why Sabahattin Ali and Sait Faik?

The source corpus rationale is a necessary part of Tasvir Bankası’s methodological framing. The project does not select Sabahattin Ali and Sait Faik Abasıyanık merely because they are convenient public-domain candidates. Their selection is better understood as the intersection of four criteria: rights caution, linguistic accessibility, literary representativeness, and computational suitability.

First, the selection is compatible with a cautious rights-review strategy. Turkish copyright law describes the general authorial protection period as the lifetime of the author plus 70 years after death [R12]. Sabahattin Ali died in 1948 [R13], and Sait Faik Abasıyanık died in 1954 [R14]. As of the 2026 release context, both authors therefore fall into a plausible public-domain candidate zone under the death-plus-70 framing. This report does not present that observation as a final legal determination. It only explains why these authors are reasonable starting points for a rights-reviewed, non-commercial literary NLP dataset.

Second, the language of these two authors is unusually suitable for a first Turkish literary NLP resource. A project that begins with public-domain Turkish prose could have selected older authors whose works are also valuable. However, not every public-domain candidate is equally appropriate for a first scene-state-description dataset. Earlier prose, including writers such as Hüseyin Rahmi Gürpınar, may contain heavier Ottoman Turkish vocabulary, older syntactic conventions, and stronger diachronic language noise. Such material is highly valuable for historical Turkish or Ottoman Turkish NLP, but it may introduce avoidable complexity into an initial dataset intended to model modern Turkish literary scene, state, dialogue, tense, and descriptive evidence. Tasvir Bankası therefore prioritizes authors whose language is closer to modern Turkish and more suitable for contemporary Turkish NLP preprocessing, annotation, and machine-learning experiments.

Third, Sabahattin Ali and Sait Faik provide strong literary representativeness across prose forms. Sabahattin Ali offers novelistic and short-story material with psychological interiority, social realism, dialogue, memory structure, scene continuity, and state-bearing narration. *Kürk Mantolu Madonna*, first published in 1943, has also reached international circulation in English translation, including through Penguin Classics / Penguin Modern Classics contexts [R15]. Sait Faik Abasıyanık, by contrast, is central to modern Turkish short fiction. Britannica describes him as one of the greatest modern Turkish short-story writers and emphasizes his distinctive contribution to Turkish prose fiction [R14]. Together, the two authors provide a balanced prose base: novel and short story; psychological narration and urban observation; social realism and atmosphere; dialogue and descriptive scene-setting.

Fourth, the two-author focus increases, rather than decreases, methodological seriousness. Tasvir Bankası is not built from an arbitrary dump of public-domain prose. It begins from a deliberately constrained corpus whose authors are both canonically significant and linguistically manageable. This constraint makes the annotation problem clearer. It reduces unnecessary historical-language noise, preserves literary value, and allows the first version of the dataset to focus on the annotation model itself: scene, state, dialogue, tense/morphology, and descriptive evidence.

This design choice also clarifies what the project is not doing. Tasvir Bankası is not a general survey of every public-domain Turkish author. It is not a historical Ottoman Turkish corpus. It is not a diachronic study of language change. Those are valuable future directions, but they require different source-selection principles and additional historical-language infrastructure. The first version of Tasvir Bankası instead builds a modern-Turkish literary core around two highly legible, canonically important prose writers.

The choice of Sabahattin Ali and Sait Faik is therefore not incidental. It establishes a controlled starting point for Turkish literary NLP by combining rights caution, modern-language proximity, genre coverage, literary significance, and computational tractability. Future versions may extend the source pool to older public-domain authors, including heavier Ottoman-influenced prose, but that expansion should be treated as a separate diachronic or historical-Turkish extension rather than as the first-stage core of the scene-state-description model.

## 4. Dataset Design

### 4.1 Record-level unit

A Tasvir Bankası record represents a text unit enriched with narrative and linguistic metadata. The record is not just an excerpt. It is a structured observation about the function of that excerpt inside literary prose.

A record may carry multiple kinds of evidence:

- scene evidence,
- state evidence,
- dialogue evidence,
- tense evidence,
- morphology evidence,
- descriptive evidence,
- selection and validation metadata,
- curation status.

This design avoids a single-label reduction of literary text. A passage may be both descriptive and scene-bearing. A passage may be state-bearing without being event-bearing. A dialogue-adjacent passage may contain no direct quote but still preserve speech evidence. A passage may shift tense or point of view while also maintaining scene continuity.

### 4.2 Why JSONL?

JSONL is used because each line can represent one independently validated record. This is appropriate for dataset construction, downstream processing, partial inspection, and machine learning workflows. JSONL also allows the dataset to preserve nested field families without forcing all annotations into flat CSV columns.

The use of JSONL does not exclude other formats. Future work may export selected layers into CSV, TEI XML, or annotation-platform formats. But JSONL is the most practical core representation for reproducible NLP pipelines.

### 4.3 Field families

The dataset card lists representative field families such as:

```text
scene_segments
scene_source
scene_edge
state_identity_profile
descriptive_profile
descriptive_profile_enriched
descriptive_profile_enriched_filtered
dialogue
tense
morphology
selection_metadata
```

These field families correspond to the project’s central design idea: literary prose should be represented through multiple narrative and linguistic evidence channels rather than one coarse label.

---

## 5. Annotation Model

### 5.1 Scene-bearing units

A scene-bearing unit is a passage that participates in a local narrative configuration. It may involve characters, location, time, perception, action, or atmosphere. It does not need to be action-heavy. A scene-setting description can be scene-bearing even when no dramatic action occurs.

This is important because Turkish literary prose often uses description to establish the conditions of a scene. A quiet room, a street at dusk, a character’s posture, or a crowd’s mood may all be necessary for scene construction.

### 5.2 State-bearing units

A state-bearing unit encodes a psychological, physical, social, moral, emotional, or situational state. It may represent fear, hesitation, fatigue, desire, uncertainty, bodily condition, social pressure, or atmosphere.

State-bearing passages are central to the dataset because they protect literary meaning from being reduced to event extraction. A passage in which nothing “happens” may still be narratively important because it sustains a state.

### 5.3 Dialogue-bearing units

Dialogue-bearing units contain direct speech, indirect speech, reported speech, speech-adjacent narration, speech verbs, or other dialogue signals. The layer should not be interpreted narrowly as quotation-mark detection. In Turkish literary prose, dialogue may be embedded, indirect, or syntactically integrated into narration.

### 5.4 Tense and morphology

Tense and morphology are not peripheral metadata for Turkish. Turkish inflection carries information about time, aspect, modality, evidentiality, person, negation, and subordination. These signals can affect whether a passage is read as present narration, recollection, habitual state, reported event, possibility, obligation, desire, or conditional structure.

The morphology-oriented layer therefore supports narrative interpretation. It is also a bridge toward Turkish UD, PropBank, and FrameNet resources.

### 5.5 Descriptive evidence

The descriptive profile captures evidence that a passage performs description. This may include spatial description, atmospheric detail, physical objects, bodily features, environmental conditions, perceptual cues, figurative language, comparison, or scene-setting material.

Description is not treated as filler. In literary prose, description often performs narrative work: it locates a character, establishes mood, slows narrative time, encodes social status, externalizes psychological state, or prepares symbolic resonance.

### 5.6 Enriched and filtered descriptive evidence

The enriched descriptive layers allow additional descriptive signals to be preserved after filtering and false-positive control. This is necessary because lexical triggers alone may be misleading. A word that looks descriptive in one passage may not function as descriptive evidence in another.

Metaphor-related fields should be interpreted cautiously. A field such as `descr_metaphor` should be read as evidence for metaphor, simile, analogy, comparison, or figurative-marker behavior. It should not be overinterpreted as a full conceptual-metaphor analysis.

### 5.7 Selection metadata and curation ledger

Selection metadata records validation and release status. The curation ledger records cases that required semantic judgment, such as false-positive removal, metaphor-marker resolution, or approval for gold-eval inclusion.

This is a key transparency mechanism. Literary annotation always contains ambiguous cases. Instead of hiding them, Tasvir Bankası records them as curation decisions.

---

## 6. Pipeline Architecture

The public GitHub repository functions as the reproducibility surface for the annotation pipeline. It contains pipeline scripts, schemas, validation tools, documentation, source-rights review materials, and limited smoke/probe JSONL samples [R2]. The release notes state explicitly that the full gated Hugging Face dataset payload is not included in the GitHub release [R2].

A simplified conceptual flow is:

```text
Rights-reviewed Turkish literary prose
        |
        v
Text-unit preparation
        |
        v
Scene / non-scene decision
        |
        +--> dialogue signals
        +--> tense / morphology
        +--> state identity
        +--> descriptive evidence
        +--> curation ledger
        |
        v
Schema-validated JSONL records
```

The most important architectural boundary is the separation between:

- **construction pipeline**, which produces and validates structured records;
- **dataset release**, which distributes the full gated data package;
- **public preview**, which allows external inspection without exposing the full dataset payload.

This separation is methodologically mature because it allows the project to be visible and reproducible while retaining access control over the full literary dataset.

---

## 7. Validation Policy

### 7.1 Schema validation

Validation ensures that records follow the expected JSON structure and that required fields are present under the correct conditions. This protects the dataset from becoming an informal collection of heterogeneous records.

### 7.2 Two-regime validation

One of Tasvir Bankası’s important design decisions is the two-regime validation policy for `brief_summary`.

The Hugging Face card states that `brief_summary` is not globally mandatory for every record. Event-bearing scenes are expected to include it, but non-event, state, emotion, description, or structural-fallback segments may omit it when accepted alternate evidence fields are present [R1].

This is a strong design choice because it respects literary structure. If every valid record were required to have an event-style summary, descriptive and state-bearing units would be unfairly penalized. The two-regime policy makes it possible to keep non-event literary units in the dataset without forcing them into event summaries.

### 7.3 Gold-eval policy

The full dataset includes 92 curated gold-eval records, but the dataset card specifies that this file is a label-level evaluation seed rather than a full-record benchmark-grade gold corpus [R1]. This qualification is important and should be preserved in all academic descriptions.

A mature formulation is:

> The gold-eval subset provides label-level curated evidence for evaluation and inspection, but it should not be treated as a fully verified benchmark-grade annotation of every field in every record.

This avoids overclaiming and increases trust.

### 7.4 Curation ledger

The curation ledger preserves human review decisions and currently reports zero pending records [R1]. This is important because it indicates that ambiguous cases were not simply discarded or silently altered. They were routed through a review layer.

---

## 8. Release Metrics and Current Dataset Status

According to the public Hugging Face dataset card, the current full dataset release reports:

| Split / component | Count |
|---|---:|
| Train records | 2,172 |
| Curated gold-eval records | 92 |
| Human curation ledger records | 98 |
| Pending queue | 0 |

These figures position Tasvir Bankası as a pilot but non-trivial resource. It is large enough to support exploratory classification tasks and schema inspection, but it should not be described as a large-scale mature benchmark.

The correct academic status is therefore:

> a structured pilot research resource with a reproducible annotation pipeline and curated label-level evaluation seed.

---

## 9. Rights, Access, and Licensing

Tasvir Bankası is released as a gated non-commercial research dataset. The Hugging Face access notice states that the dataset is provided for research, education, reproducibility review, and non-commercial evaluation only, and that commercial model training, resale, paid text-generation products, commercial derivative dataset production, and author-style cloning or imitation services are not permitted without explicit written permission from the author [R1].

This access model is appropriate for literary data. Literary corpora can be misused for style imitation, unauthorized commercial dataset construction, or author-cloning systems. A gated non-commercial release reduces those risks while preserving academic visibility.

The rights framing should remain cautious. Source texts are described as rights-reviewed public-domain candidates, but the release does not constitute legal determination [R1]. This limitation is not a weakness; it is a necessary legal and ethical boundary.

---

## 10. Use Cases

Tasvir Bankası can support several research directions.

### 10.1 Computational narratology

The dataset can support computational study of scenes, states, descriptions, dialogue, and narrative transitions in Turkish prose. It provides a structured basis for asking how Turkish literary passages function narratively.

### 10.2 Digital humanities

Digital humanities researchers can use the schema as a model for building inspectable literary corpora that preserve scene, descriptive, and state-bearing units.

### 10.3 Turkish literary NLP

The dataset can be converted into measurable tasks such as:

- dialogue-bearing detection,
- descriptive-evidence detection,
- scene-bearing classification,
- event-bearing versus state-bearing distinction,
- tense/morphology distribution analysis.

### 10.4 Annotation schema research

The project provides a case study in designing annotation schemas for non-English literary prose. Its two-regime policy is especially relevant for representing non-event literary units.

---

## 11. Baseline Evaluation Plan

This report does not claim completed benchmark results. Instead, it proposes baseline experiments that can be added in the next research-readiness stage.

### 11.1 Dialogue-bearing detection

**Task:** Given a text unit, predict whether it is dialogue-bearing.  
**Why first:** Dialogue signals are easier to define than atmosphere or metaphor and can be explained clearly to NLP reviewers.  
**Baselines:** majority baseline, rule baseline, TF-IDF + logistic regression, Turkish transformer baseline.  
**Metrics:** accuracy, precision, recall, F1, macro-F1.  
**Error analysis:** indirect speech, reported speech, missing quotation marks, overreliance on punctuation.

### 11.2 Descriptive-evidence detection

**Task:** Given a text unit, predict whether it contains descriptive evidence.  
**Why important:** This task highlights the dataset’s distinctive contribution.  
**Baselines:** lexical rules, TF-IDF + logistic regression, Turkish transformer baseline.  
**Error analysis:** confusion between emotion and description, false positives from adjectives, difficulty with figurative description.

### 11.3 Scene-bearing classification

**Task:** Given a text unit, classify whether it is scene-bearing.  
**Why important:** Scene modeling is central to computational narratology.  
**Baselines:** majority baseline, heuristic cues, TF-IDF + logistic regression, Turkish transformer baseline.  
**Error analysis:** scene-setting descriptions, summary passages, short fragments, state-bearing passages.

### 11.4 Event-bearing versus state-bearing distinction

**Task:** Predict whether a passage primarily functions as event-bearing or state-bearing.  
**Why important:** This tests the theoretical core of the project.  
**Recommended first step:** Start with a binary label rather than an ambitious multi-class setup.

These experiments should be reported as baseline demonstrations, not final benchmarks. The correct claim would be:

> These experiments show that Tasvir Bankası annotation layers can be operationalized as measurable Turkish literary NLP tasks.

---

## 12. Limitations

A mature technical report must state limitations clearly.

1. **Pilot scale:** The dataset is a carefully engineered pilot resource, not a large-scale community benchmark.
2. **Gold-eval scope:** The curated gold-eval subset is label-level and should not be treated as full-record benchmark-grade annotation.
3. **Access limitation:** The full dataset is gated, which protects rights and usage boundaries but reduces frictionless reproducibility.
4. **Source-rights boundary:** Rights review is documented, but it is not legal advice or a universal jurisdictional determination.
5. **Schema transfer:** The schema is designed for Turkish literary prose and may require adaptation for poetry, drama, contemporary copyrighted fiction, oral narratives, or other languages.
6. **Metaphor scope:** Metaphor-related fields are evidence markers, not a complete conceptual-metaphor annotation framework.
7. **Evaluation maturity:** Baseline experiments are planned but should be added before submission to a dataset/resource venue.
8. **Community validation:** External review by Turkish NLP, digital humanities, and literary scholars would strengthen the project.

These limitations are not reasons to withhold the project. They define the proper academic boundary of the release.

---

## 13. Recommended Scholarly Framing

Tasvir Bankası should be described as:

> a Turkish literary scene-state-description dataset and annotation pipeline for computational narratology and Turkish literary NLP.

A more detailed formulation is:

> Tasvir Bankası provides structured JSONL records for Turkish literary prose, with layers for scene segmentation, state-bearing textual units, dialogue signals, tense/morphology, and descriptive evidence.

Avoid describing it as:

- a full benchmark-grade gold corpus,
- a general Turkish LLM training dataset,
- a style-cloning resource,
- an author-imitation dataset,
- a commercial model-training corpus,
- a complete literary-theory annotation framework.

The strongest scholarly claim is:

> Tasvir Bankası introduces a reproducible, non-commercial, scene-state-description annotation model for Turkish literary prose, addressing the lack of openly documented narrative-function datasets in Turkish literary NLP.

---

## 14. Future Work

The next development stage should prioritize research-readiness:

1. **Technical report completion:** Convert this draft into a formal PDF/preprint or workshop-ready paper.
2. **Baseline experiments:** Implement dialogue-bearing and descriptive-evidence detection baselines.
3. **Schema documentation:** Add a field-by-field annotation guide with examples.
4. **Public preview expansion:** Provide a small set of rights-safe illustrative examples for inspection.
5. **External feedback:** Request feedback from Turkish NLP, computational narratology, digital humanities, and Turkish literature researchers.
6. **Interoperability:** Explore mappings to TEI, CATMA, BRAT standoff annotation, or INCEpTION-compatible formats.
7. **Model cards and task cards:** Define explicit tasks derived from the annotation layers.
8. **Versioning:** Maintain clear distinction between pipeline version, dataset version, and publication record.

The most important short-term objective is not to enlarge the dataset immediately. It is to make the existing resource academically inspectable, reproducible, and citable.

---

## 15. Conclusion

Tasvir Bankası provides a structured annotation model and pipeline for Turkish literary prose. Its contribution lies in treating literary text not as raw material for style imitation or general language modeling, but as a field of layered narrative evidence. By distinguishing scene-bearing, state-bearing, dialogue-bearing, tense-bearing, morphology-bearing, and descriptive-evidence-bearing units, the project offers a concrete path toward Turkish computational narratology.

The current release is best understood as a pilot research resource with a gated full dataset, a public-safe pipeline package, a Zenodo-backed citation record, and a documentation framework for reproducibility. It should not be overclaimed as a mature benchmark, but it is already strong enough to support a technical report, portfolio presentation, workshop submission, and small baseline experiments.

Its core value is clear:

> Tasvir Bankası makes Turkish literary prose computationally inspectable at the level of scenes, states, descriptions, dialogue, time, and narrative function.

---


## Appendix: Should This Rationale Be Added to the Hugging Face Dataset Card?

Yes, a shortened version of the source-corpus rationale should be added to the Hugging Face dataset card. The full technical version belongs in this report, but the dataset card should contain a concise explanation because many readers will inspect the Hugging Face page before reading the GitHub documentation or the technical report.

The Hugging Face version should be shorter and less argumentative. It should not become a long literary essay, and it should not make an absolute legal claim. The safest phrasing is to state that the dataset uses rights-reviewed public-domain candidate prose and that Sabahattin Ali and Sait Faik were selected because they combine post-mortem rights-review suitability, modern Turkish readability, literary significance, prose-form coverage, and annotation suitability.

Recommended Hugging Face subsection:

```markdown
## Source corpus rationale

The initial Tasvir Bankası release focuses on rights-reviewed public-domain candidate prose by Sabahattin Ali and Sait Faik Abasıyanık.

This source choice is methodological rather than incidental. Both authors fall within a plausible death-plus-70 public-domain candidate window under the Turkish copyright framework, although this release does not constitute a legal determination. Their prose is also relatively close to modern Turkish compared with older Ottoman-influenced public-domain prose, making it more suitable for a first Turkish literary NLP resource focused on scene, state, dialogue, tense/morphology, and descriptive evidence.

The two-author focus provides genre and narrative-function coverage across novelistic prose, short fiction, psychological narration, dialogue, urban observation, atmosphere, and description. The release therefore does not attempt to process arbitrary public-domain Turkish prose. It begins with a controlled modern-Turkish literary core before extending to more historically or linguistically complex source pools in future versions.
```

This Hugging Face addition would improve reader trust because it answers a natural question:

> Why these authors, and why not any public-domain Turkish prose?

The recommended location in the dataset card is after the dataset summary and before the data structure / splits section. It should not replace the existing rights and license sections. It should only add a source-selection explanation.

## References

**[R1]** Yaşar, F. (2026). *Tasvir Bankası: Turkish Literary Scene-State-Description Dataset*. Hugging Face dataset card.  
https://huggingface.co/datasets/Kon-tiki-ship/tasvir-bankasi-turkish-literary-scene-state-description-dataset

**[R2]** Yaşar, F. (2026). *Tasvir Bankası Turkish Literary Annotation Pipeline*. GitHub public-preview repository and release notes.  
https://github.com/Kon-tiki-ship/tasvir-bankasi-turkish-literary-annotation-pipeline

**[R3]** Zehe, A., Konle, L., Dümpelmann, L. K., Gius, E., Hotho, A., Jannidis, F., Kaufmann, L., Krug, M., Puppe, F., Reiter, N., Schreiber, A., Wiedmer, N. (2021). *Detecting Scenes in Fiction: A New Segmentation Task*. EACL 2021.  
https://aclanthology.org/2021.eacl-main.276/

**[R4]** Alrashid, T., Gaizauskas, R., and collaborators. (2023). *ScANT: A Small Corpus of Scene-Annotated Narrative Texts*. CEUR / ORDA dataset documentation.  
https://ceur-ws.org/Vol-3370/paper15.pdf  
https://orda.shef.ac.uk/articles/dataset/ScANT_A_Small_Corpus_of_Scene-Annotated_Narrative_Texts/21517908

**[R5]** Vishnubhotla, K., Hammond, A., & Hirst, G. (2022). *The Project Dialogism Novel Corpus: A Dataset for Quotation Attribution in Literary Texts*. LREC 2022.  
https://aclanthology.org/2022.lrec-1.628/

**[R6]** Özateş, Ş. B., Tıraş, T. E., Adak, E. E., Doğan, B., Karagöz, F. B., Genç, E. E., & Bilgin Taşdemir, E. F. (2025). *Building Foundations for Natural Language Processing of Historical Turkish: Resources and Models*. arXiv.  
https://arxiv.org/abs/2501.04828

**[R7]** Universal Dependencies. *Turkish UD overview*.  
https://universaldependencies.org/tr/

**[R8]** Kara, N., et al. (2020). *TRopBank: Turkish PropBank V2.0*. LREC 2020.  
https://aclanthology.org/2020.lrec-1.336/

**[R9]** Marşan, B., et al. (2021). *Building the Turkish FrameNet*. Global WordNet Conference.  
https://aclanthology.org/2021.gwc-1.14.pdf

**[R10]** Zeyrek, D., & Erolcan Er, M. (2022). *A Description of Turkish Discourse Bank 1.2 and an Examination of Common Dependencies in Turkish Discourse*.  
https://ceur-ws.org/Vol-3315/paper04.pdf

**[R11]** Heyns, N., & Van Zaanen, M. (2025). *Annotated Mystery Narratives Data Set*. Journal of Open Humanities Data.  
https://openhumanitiesdata.metajnl.com/articles/10.5334/johd.391


**[R12]** Republic of Türkiye Ministry of Culture and Tourism, Directorate General of Copyright. *General Questions: Copyright protection period*.  
https://telifhaklari.ktb.gov.tr/TR-332449/genel-sorular.html

**[R13]** Encyclopaedia Britannica. *Sabahattin Ali*.  
https://www.britannica.com/biography/Sabahattin-Ali

**[R14]** Encyclopaedia Britannica. *Sait Faik Abasıyanık*.  
https://www.britannica.com/biography/Sait-Faik-Abasiyanik

**[R15]** Penguin / Penguin Modern Classics listing context for *Madonna in a Fur Coat*.  
https://www.penguin.co.uk/books/445081/madonna-in-a-fur-coat-by-ali-sabahattin/9780241422267

**[R16]** Britannica. *Modern Turkish literature*.  
https://www.britannica.com/art/Turkish-literature/Modern-Turkish-literature

