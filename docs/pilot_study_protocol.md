# Pilot Study Protocol: Manual Validation of Supply Chain Construct Scores

**Project**: Corporate Text Pipeline - Supply Chain Constructs Measurement  
**Purpose**: Validate LLM-generated construct scores against expert human judgment  
**Status**: Protocol for pilot study design  
**Team Members**: Katelyn (PhD Student - Coordinator), Lachlan (Undergraduate RA)

---

## Table of Contents
1. [Study Overview and Objectives](#overview)
2. [Theoretical Framework](#framework)
3. [Sample Selection](#sample)
4. [Scoring Rubric and Dimensions](#rubric)
5. [Step-by-Step Instructions](#instructions)
6. [Data Recording and Submission](#recording)
7. [Timeline and Deliverables](#timeline)
8. [Quality Control](#quality)

---

## Study Overview and Objectives {#overview}

### Purpose
Before deploying LLM-based scoring on our full sample of firm-year observations, we need to validate that:
1. Our scoring rubrics produce reliable scores when applied by human coders across all measured constructs
2. Different coders interpret the rubrics consistently (inter-rater reliability)
3. We understand what "high" vs "low" scores look like in practice for each construct
4. The eventual LLM scores correlate with human expert judgment

### What You'll Do
Each team member will independently:
1. Read 10-K excerpts from a sample of firms (sample size and selection determined by PhD student)
2. Score **multiple supply chain constructs** using our rubrics (see Theoretical Framework for full list)
3. Document notable examples and edge cases
4. Meet to discuss discrepancies and refine the rubrics if needed

### Research Context
We are measuring both:
- **Transparency constructs** (our primary outcomes): How much firms disclose about their supply chains
- **Mechanism constructs** (moderators in our analysis): Supply chain management practices that may explain transparency changes

The pilot validates scoring for all constructs simultaneously.

### Roles and Coordination
- **Katelyn (PhD Student)**: Coordinates pilot study, designs sampling strategy, develops detailed rubrics, leads calibration, analyzes results
- **Lachlan (RA)**: Participates in scoring and calibration process
- **PI**: Reviews final validation report and approves methodology

### Time Commitment
- Varies based on sample size selected by PhD student
- Typical range: 8-15 hours per person for scoring + meetings

---

## Theoretical Framework

### What Are We Measuring?

This project measures **supply chain constructs** - characteristics of firms' supply chain disclosures and management practices - derived from 10-K filings.

**Data Source**: We focus on 10-K filings (annual reports to the SEC), specifically:
- Item 1 (Business Description)
- Item 1A (Risk Factors)  
- Item 7 (MD&A - Management Discussion & Analysis)

These sections contain the majority of supply chain-related disclosures.

### Constructs to Be Measured

Our research measures **multiple constructs** related to supply chain management and transparency. The pilot study will validate scoring for all constructs.

#### **Primary Outcome: Supply Chain Transparency Measures**

**1. Supply Chain Transparency (Aggregate)** (0-10)
> The degree to which the firm publicly discloses information about the environmental and social impacts and risks associated with its upstream supply chain operations.

**2. Environmental Supply Chain Transparency** (0-10)
> The degree to which the firm publicly discloses information about the environmental impacts and risks associated with its upstream supply chain operations (e.g., waste, resource use, emissions).

**3. Social Supply Chain Transparency** (0-10)
> The degree to which the firm publicly discloses information about the social impacts and risks associated with its upstream supply chain operations (e.g., poor working conditions, child labor, lack of fair wages).

**4. Supply Base Transparency (Aggregate)** (0-10)
> The degree to which the firm publicly discloses information about the environmental and social impacts and risks associated with its supply base (i.e., its tier 1 suppliers).

#### **Mechanism Variables: Supply Chain Management Practices**

These constructs help explain *how* and *why* firms become more transparent:

**5. Digital Transformation** (0-10)
> The strategic adoption and integration of digital technologies that reshape a firm's operations and supply chain (e.g., processes, data flows, decision-making), through implementing enterprise systems and/or partnering with technology providers, to digitize operations, connect data across production processes and suppliers, and enable new real-time visibility capabilities.

**6. Supplier Audits** (0-10)
> A systematic evaluation, typically conducted on-site, of a supplier's processes, systems, operations, and practices to verify conformance to defined environmental and social standards, assessing capability to meet requirements consistently.

**7. Supplier Code of Conduct** (0-10)
> A formal set of standards and expectations specifying practices (e.g., social, environmental, operational) that suppliers are expected to adhere to. Serves as a formal management tool to communicate minimum acceptable behaviors and performance requirements.

**8. Supply Base Reconfiguration** (0-10)
> Modification of supplier base through termination or restructuring of existing suppliers in response to unacceptable behavior or performance (e.g., violations of social or environmental standards). Unlike routine supplier changes driven by cost, this serves as a governance mechanism aimed at mitigating sustainability-related risks.

**9. Supplier Development** (0-10)
> Efforts to improve suppliers' capabilities, performance, and compliance (including social and environmental aspects) through activities such as training, knowledge transfer, and collaboration.

---

### Scoring Note

Each construct is scored independently on a 0-10 scale. The PhD student will develop specific scoring rubrics for each construct based on these definitions, informed by the theoretical framework and pilot testing.

---

## Sample Selection

### Sampling Strategy

**Katelyn will design and implement the sampling strategy**, considering:
- Representation of different expected construct levels (high/medium/low)
- Diversity across industries within manufacturing
- Variation in firm sizes
- Coverage of different time periods in our data

### Key Considerations for Sampling

The sample should balance:
- **Statistical validity**: Sufficient size for correlation analysis with eventual LLM scores
- **Feasibility**: Manageable given time constraints (~20-30 minutes per firm)
- **Heterogeneity**: Coverage of the variation we expect to see in the full dataset

### Your Assignment

Katelyn will provide:
- A finalized list of CIK-Year combinations to score
- Links to or instructions for accessing the relevant 10-K filings
- Any stratification information (e.g., "This group is high-disclosure firms")

**Note**: The sampling strategy, including final sample size and selection criteria, should be documented by Katelyn in the validation report.

---

## Scoring Rubric and Guidelines {#rubric}

### General Scoring Guidelines

**Scale**: All constructs scored 0-10
- **0-2**: No meaningful disclosure or evidence
- **3-4**: Minimal disclosure (vague statements, no specifics)
- **5-6**: Moderate disclosure (some concrete info, but limited)
- **7-8**: Strong disclosure (detailed, specific, quantified)
- **9-10**: Exceptional disclosure (comprehensive, verified, detailed)

### What Counts as "Disclosure" or "Evidence"?

✅ **DOES COUNT:**
- Specific supplier names, locations, or identifiers
- Quantitative metrics (e.g., "95% of suppliers audited")
- Concrete policies with implementation details
- Evidence of monitoring/auditing programs
- Discussion of supply chain risks with mitigation strategies
- Third-party certifications or partnerships with NGOs
- Specific examples of programs or initiatives

❌ **DOES NOT COUNT:**
- Boilerplate statements (e.g., "We expect suppliers to follow our code of conduct")
- Aspirational statements without evidence (e.g., "We are committed to sustainability")
- Generic risk factors without supply-chain-specific details
- Legal compliance statements without additional disclosure

---

## Detailed Rubrics for Each Construct

**Note**: The PhD student will develop detailed, construct-specific scoring rubrics during pilot study design. Below are illustrative examples to guide rubric development.

### Example Rubric Template

For each construct, the rubric should specify:
1. **What to look for** - specific text indicators
2. **Score anchors** - examples of text that would score 0-2, 3-4, 5-6, 7-8, 9-10
3. **Edge cases** - how to handle ambiguous situations
4. **Section guidance** - where in 10-K to find relevant info

---

### Illustrative Rubric: Environmental Supply Chain Transparency

**What to look for:**
- Scope 3 emissions (supply chain carbon footprint)
- Supplier environmental standards or audits
- Water usage/pollution by suppliers
- Waste management practices upstream
- Sustainable sourcing (e.g., recycled materials, certified sources)
- Energy efficiency in supply chain

**Scoring Guide:**

| Score | Description | Example Text |
|-------|-------------|--------------|
| 0-2 | No environmental supply chain disclosure | "We comply with environmental regulations." |
| 3-4 | Vague statements | "We encourage suppliers to be environmentally responsible." |
| 5-6 | Some specific initiatives | "We are working with suppliers to reduce packaging waste in our supply chain." |
| 7-8 | Quantified metrics or multiple initiatives | "We measured Scope 3 emissions across our top 50 suppliers (80% of spend). We identified a 12% reduction opportunity." |
| 9-10 | Comprehensive with verification | "We achieved CDP Supply Chain score of A-. Third-party verified Scope 3 reduction of 15% since 2015. Supplier environmental audits disclosed on our website." |

---

### Illustrative Rubric: Supplier Audits

**What to look for:**
- Mention of audit programs
- Frequency of audits
- Number/percentage of suppliers audited
- Types of audits (announced vs unannounced)
- Audit results or findings
- Third-party auditors mentioned
- Corrective action programs

**Scoring Guide:**

| Score | Description |
|-------|-------------|
| 0-2 | No mention of supplier audits |
| 3-4 | Generic mention (e.g., "We audit suppliers") |
| 5-6 | Some specifics (e.g., "Annual audits of tier-1 suppliers") |
| 7-8 | Detailed program with metrics (e.g., "Conducted 200 audits in 2019; 15 suppliers in remediation") |
| 9-10 | Comprehensive program with published results and third-party verification |

---

### PhD Student Task: Develop Full Rubrics

The PhD student should create detailed scoring rubrics for all 9 constructs following this template:

**For each construct:**
1. List specific indicators to look for in text
2. Provide 3-5 example quotes for each score level (0-2, 3-4, 5-6, 7-8, 9-10)
3. Document edge cases and how to score them
4. Note which 10-K sections are most relevant
5. Test rubrics on 2-3 example firms before distributing to RA

These detailed rubrics will be shared with the RA before scoring begins.

### General Scoring Guidelines

**Scale**: All dimensions scored 0-10
- **0-2**: No meaningful disclosure
- **3-4**: Minimal disclosure (vague statements, no specifics)
- **5-6**: Moderate disclosure (some concrete info, but limited)
- **7-8**: Strong disclosure (detailed, specific, quantified)
- **9-10**: Exceptional disclosure (comprehensive, verified, multi-tier)

### What Counts as "Disclosure"?

✅ **DOES COUNT:**
- Specific supplier names, locations
- Quantitative metrics (e.g., "95% of suppliers audited")
- Concrete policies with implementation details
- Evidence of monitoring/auditing
- Discussion of supply chain risks with mitigation strategies
- Third-party certifications or partnerships with NGOs

❌ **DOES NOT COUNT:**
- Boilerplate statements (e.g., "We expect suppliers to follow our code of conduct")
- Aspirational statements without evidence (e.g., "We are committed to sustainability")
- Generic risk factors without supply-chain-specific details
- Legal compliance statements without additional disclosure

---

## Dimension-Specific Rubric

### 1. Overall Transparency Score (0-10)

**Your holistic judgment**: How transparent is this firm about its supply chain?

**Scoring Guide:**

| Score | Description | Examples |
|-------|-------------|----------|
| 0-2 | No disclosure | No mention of supply chain practices beyond generic risk factors |
| 3-4 | Minimal | Brief mention of supplier relationships; vague sustainability claims |
| 5-6 | Moderate | Names key suppliers or regions; discusses some specific initiatives |
| 7-8 | Strong | Detailed disclosure of supplier base, metrics on compliance, multi-tier visibility |
| 9-10 | Exceptional | Comprehensive supplier list, quantified impacts, third-party verified, multi-tier |

**Consider:**
- Volume of information disclosed
- Specificity and detail
- Credibility (verified vs. claimed)
- Breadth (environmental + social + depth)

---

### 2. Environmental Transparency (0-10)

**Question**: How much does the firm disclose about environmental impacts in its supply chain?

**Look for:**
- Scope 3 emissions (supply chain carbon footprint)
- Supplier environmental standards or audits
- Water usage/pollution by suppliers
- Waste management practices upstream
- Sustainable sourcing (e.g., recycled materials, certified wood)
- Energy efficiency in supply chain

**Scoring Guide:**

| Score | Description |
|-------|-------------|
| 0-2 | No environmental supply chain disclosure |
| 3-4 | Vague statements (e.g., "We encourage suppliers to be environmentally responsible") |
| 5-6 | Some specific initiatives mentioned (e.g., "Working with suppliers to reduce packaging waste") |
| 7-8 | Quantified metrics (e.g., "Supply chain emissions decreased 15% since 2015") or multiple initiatives |
| 9-10 | Comprehensive disclosure with verification (e.g., CDP Supply Chain score, third-party audits) |

**Example - Score 3:**
> "We are committed to environmental sustainability throughout our supply chain."

**Example - Score 7:**
> "In 2018, we measured Scope 3 emissions across our top 50 suppliers, representing 80% of our procurement spend. We identified a 12% reduction opportunity and are working with 30 suppliers on energy efficiency improvements."

---

### 3. Social Transparency (0-10)

**Question**: How much does the firm disclose about labor practices and social impacts in its supply chain?

**Look for:**
- Labor conditions at supplier facilities
- Worker safety and health initiatives
- Fair wages and working hours
- Prevention of child or forced labor
- Freedom of association
- Supplier audits on social compliance
- Diversity and inclusion in supply chain
- Community impacts

**Scoring Guide:**

| Score | Description |
|-------|-------------|
| 0-2 | No social supply chain disclosure |
| 3-4 | Generic code of conduct for suppliers without implementation details |
| 5-6 | Some specifics (e.g., "We audit suppliers annually for labor compliance") |
| 7-8 | Detailed disclosure with metrics (e.g., "89% of suppliers passed labor audits; 15 suppliers in remediation") |
| 9-10 | Comprehensive with third-party verification (e.g., Fair Labor Association certification, published audit results) |

**Example - Score 4:**
> "All suppliers must comply with our Supplier Code of Conduct, which prohibits child labor and requires safe working conditions."

**Example - Score 8:**
> "We conducted 347 social compliance audits across our global supplier base in 2019. Of these, 12 suppliers were found to have working hour violations, and we worked with them to implement corrective action plans. We publicly disclose audit results on our website and partner with the Fair Wear Foundation for independent verification."

---

### 4. Supply Chain Depth (0-10)

**Question**: How far upstream does the firm's disclosure extend?

**Tiers Explained:**
- **Tier-1**: Direct suppliers (who the firm buys from directly)
- **Tier-2**: Suppliers' suppliers
- **Tier-3+**: Further upstream (e.g., raw material producers)

**Scoring Guide:**

| Score | Description |
|-------|-------------|
| 0-3 | Only discusses own operations; no upstream disclosure |
| 4-5 | Mentions Tier-1 suppliers generally (no names/details) |
| 6 | Discloses some Tier-1 supplier information (names, locations, or practices) |
| 7-8 | Discloses Tier-1 comprehensively AND mentions Tier-2 suppliers |
| 9-10 | Multi-tier disclosure to raw materials; full supply chain mapping |

**Example - Score 4:**
> "We work with suppliers globally to source components for our products."

**Example - Score 7:**
> "We have mapped our Tier-1 and Tier-2 suppliers for critical raw materials. Our supplier list, available on our website, includes 200+ Tier-1 facilities and 50+ Tier-2 raw material suppliers in high-risk regions."

---

### 5. Verification Level (0-10)

**Question**: How credible is the disclosed information? Is it verified by third parties?

**Scoring Guide:**

| Score | Description |
|-------|-------------|
| 0-2 | No disclosure or only unsubstantiated claims |
| 3-4 | Self-reported information; vague statements |
| 5-6 | Self-reported but with some specific metrics/examples |
| 7-8 | Some third-party verification mentioned (audits, certifications) |
| 9-10 | Comprehensive third-party verification; recognized certifications (ISO, B-Corp, Fair Trade, etc.) |

**Look for:**
- Third-party audits (e.g., "Ernst & Young audited our supplier compliance")
- Certifications (e.g., "Fair Trade Certified," "B-Corp," "ISO 14001")
- Industry standards (e.g., "Member of Accord on Fire and Building Safety")
- NGO partnerships (e.g., "Partner with WWF for sustainable sourcing")

**Example - Score 5:**
> "We conduct internal audits of our suppliers and have found 95% compliance with our standards."

**Example - Score 9:**
> "Our supply chain practices are independently audited by KPMG, and we hold B-Corp certification. We are members of the Fair Labor Association and publicly disclose all audit findings on our transparency portal."

---

## Step-by-Step Instructions {#instructions}

### Before You Begin

**1. Review the construct definitions**
- Carefully read the 9 construct definitions in the Theoretical Framework section
- These are the working definitions developed by Katelyn
- Familiarize yourself with what each construct measures

**2. Set up your workspace**
- Create a folder for pilot study materials
- Await instructions from Katelyn on sample and materials
- Prepare to download the scoring template when provided

**3. Calibration (First Subset)**
- Katelyn and Lachlan will each score the same initial subset of firms independently
- Meet to compare scores and discuss discrepancies
- Refine understanding of the rubrics
- Proceed with remaining firms in sample

**Note**: Katelyn will coordinate timing, materials distribution, and meeting scheduling.

---

### Scoring Process for Each Firm

**Step 1: Access the 10-K Filing**
- Open the SEC EDGAR link provided in `pilot_sample.csv`
- Download or view the HTML/text version

**Step 2: Navigate to Key Sections**
Focus on these sections (where supply chain disclosures typically appear):
- **Item 1 - Business**: Describes supply chain structure
- **Item 1A - Risk Factors**: Discusses supply chain risks
- **Item 7 - MD&A**: May discuss supply chain initiatives/impacts

**Pro tip**: Use `Ctrl+F` (or `Cmd+F`) to search for keywords:
- "supplier", "supply chain", "upstream"
- "labor", "working conditions", "child labor"
- "carbon", "emissions", "environmental", "sustainability"
- "audit", "compliance", "verification"

**Step 3: Read and Extract Relevant Information**
- Copy relevant paragraphs into a document for reference
- Note page numbers or section names
- Look for both qualitative and quantitative information

**Step 4: Score Each Dimension**
- Use the rubrics above
- Assign scores 0-10 for each of the 5 dimensions
- Write brief justification (2-3 sentences) for each score

**Step 5: Note Examples and Edge Cases**
If you encounter:
- Excellent examples of transparency → note for later discussion
- Unclear cases → flag for team discussion
- Interesting practices → document for qualitative insights

**Step 6: Record Your Scores**
Enter into `pilot_scoring_template.xlsx` (see Data Recording section below)

---

### Time Management

**Per firm**: Aim for 20-30 minutes
- 10 min: Reading relevant sections
- 5 min: Extracting key information
- 10 min: Scoring + justifications
- 5 min: Recording data

**Total time**:
- 25 firms × 25 min = ~10 hours of scoring
- +2 hours calibration meeting
- +2 hours documentation and submission
- **Total: ~12-15 hours**

---

## Data Recording and Submission {#recording}

### Scoring Template

Use the provided Excel file: `pilot_scoring_template.xlsx`

**Columns:**
1. `Coder_ID`: Your initials (e.g., "JD" for PhD student, "AS" for RA)
2. `CIK`: From pilot_sample.csv
3. `Year`: From pilot_sample.csv
4. `Firm_Name`: For reference
5. `Overall_Score`: 0-10
6. `Environmental_Score`: 0-10
7. `Social_Score`: 0-10
8. `Depth_Score`: 0-10
9. `Verification_Score`: 0-10
10. `Overall_Justification`: 2-3 sentence explanation
11. `Environmental_Justification`: 2-3 sentence explanation
12. `Social_Justification`: 2-3 sentence explanation
13. `Depth_Justification`: 2-3 sentence explanation
14. `Verification_Justification`: 2-3 sentence explanation
15. `Notable_Examples`: Any interesting quotes or practices
16. `Edge_Cases`: Anything unclear or difficult to score
17. `Time_Spent_Minutes`: How long you spent on this firm
18. `Date_Scored`: When you scored it

### Example Row

| Coder_ID | CIK | Year | Firm_Name | Overall_Score | Overall_Justification |
|----------|-----|------|-----------|---------------|---------------------|
| JD | 0000051143 | 2018 | IBM | 7 | IBM discloses Tier-1 supplier list with locations, reports on supplier diversity metrics, and mentions environmental audits. However, lacks quantitative environmental metrics and limited Tier-2 visibility. |

### Submission

**When complete:**
1. Save your Excel file as: `pilot_scores_[YourInitials].xlsx`
2. Upload to the shared Google Drive folder OR GitHub repo (in `data/pilot/`)
3. Notify PI that scoring is complete

---

## Timeline and Deliverables

**Note**: Katelyn will set the specific timeline and deadlines for the pilot study. Below is a general template.

### Phase 1: Preparation and Calibration

**Katelyn's Tasks:**
- [ ] Design sampling strategy and select firms
- [ ] Develop detailed scoring rubrics for all 9 constructs
- [ ] Prepare sample file with CIK-Year combinations and 10-K links
- [ ] Create scoring template spreadsheet
- [ ] Distribute materials to Lachlan
- [ ] Schedule calibration meeting

**Both Katelyn and Lachlan:**
- [ ] Review this protocol thoroughly
- [ ] Review the 9 construct definitions
- [ ] Set up workspace and download materials
- [ ] Score initial subset of firms independently (size determined by Katelyn)

**Calibration Meeting (Both):**
- [ ] Compare scores for initial subset
- [ ] Discuss discrepancies (aim for within 2 points on 0-10 scale)
- [ ] Clarify interpretation of rubrics
- [ ] Refine approach if needed
- [ ] Document any rubric adjustments

### Phase 2: Full Scoring

**Both:**
- [ ] Score remaining firms in sample
- [ ] Document notable examples and edge cases
- [ ] Submit completed scoring template to Katelyn

### Phase 3: Analysis and Reporting (Katelyn)

- [ ] Calculate inter-rater reliability (correlation, Cohen's kappa)
- [ ] Identify firms with largest score discrepancies
- [ ] Summarize notable examples across constructs
- [ ] Draft validation report for PI
- [ ] Present findings to team

---

## Deliverables

### 1. Completed Scoring Templates (Both)
- `pilot_scores_[Initials].xlsx` with all 25 firms scored

### 2. Validation Report (PhD Student, 2 pages)

**Section 1: Inter-Rater Reliability**
- Correlation between coders for each dimension
- Average difference in scores
- Interpretation: Are we reliable?

**Section 2: Descriptive Statistics**
- Distribution of scores (mean, SD, range) for each dimension
- Which firms scored highest/lowest?
- Which dimensions show most/least transparency?

**Section 3: Qualitative Insights**
- 3-5 notable examples of transparency practices
- 3-5 edge cases or challenges in scoring
- Patterns observed (e.g., larger firms more transparent?)

**Section 4: Recommendations**
- Any rubric refinements needed?
- Any additional dimensions to consider?
- Readiness assessment for LLM scoring

### 3. Calibration Meeting Notes (Both)
- Document of agreed-upon interpretations from calibration meeting

---

## Quality Control {#quality}

### Self-Check Before Submitting

**For each firm, ask yourself:**
- [ ] Did I read all three key sections (Items 1, 1A, 7)?
- [ ] Are my scores consistent with the rubric?
- [ ] Did I justify each score with specific examples from the text?
- [ ] Did I differentiate between "aspirational statements" and "concrete disclosure"?
- [ ] Did I note any edge cases or uncertainties?

### Red Flags to Watch For

**Scoring too high:**
- Giving credit for vague commitments without evidence
- Confusing "visibility" (internal knowledge) with "transparency" (external disclosure)
- Being impressed by quantity of text rather than quality of disclosure

**Scoring too low:**
- Missing relevant disclosures in other sections
- Expecting perfection (few firms score 9-10)
- Discounting legitimate, verified disclosures

### Inter-Rater Agreement Targets

After calibration, we aim for:
- **Correlation** > 0.70 between coders
- **Average difference** < 2 points on the 0-10 scale
- **Perfect agreement** (within 1 point) on >60% of firms

If these targets aren't met, we'll have a second calibration meeting.

---

## Resources and Support

### Key References
- **Bateman, A., & Bonanni, L. (2019)**. "What Supply Chain Transparency Really Means." *Harvard Business Review*.
- **Sodhi, M. S., & Tang, C. S. (2019)**. "Research opportunities in supply chain transparency." *Production and Operations Management*, 28(12), 2946-2959.

### Example Companies with High Transparency
(For reference - not in pilot sample)
- **Patagonia**: Footprint Chronicles showing multi-tier supply chain
- **Everlane**: Discloses cost breakdown and factory information
- **Nike**: Manufacturing map with all contract factories

### Questions?
- **Technical (scoring process)**: Katelyn
- **Conceptual (construct definitions)**: Katelyn or PI
- **Logistics (accessing files, deadlines)**: PI

---

## Appendix A: Pilot Sample Design Considerations

The PhD student should document their sampling strategy in the validation report, including:

**Sample Size Justification:**
- Statistical power considerations
- Time/resource constraints
- Minimum needed for reliability analysis

**Stratification Variables (if applicable):**
- Expected transparency level (how determined?)
- Industry categories
- Firm size categories
- Time period distribution

**Selection Method:**
- Random sampling within strata
- Purposive sampling rationale
- Any exclusion criteria

**Sample Characteristics:**
- Final distribution across stratification variables
- Any deviations from intended design and why

---

## Appendix B: Scoring Decision Tree

**When in doubt, use this decision tree:**

```
Does the firm mention supply chain at all?
├─ NO → Score 0-1
└─ YES → Is the mention specific (names, numbers, practices)?
    ├─ NO (vague/aspirational) → Score 2-4
    └─ YES → Are there quantitative metrics or multi-tier disclosure?
        ├─ NO → Score 5-6
        └─ YES → Is there third-party verification?
            ├─ NO → Score 7-8
            └─ YES → Score 9-10
```

---

**Good luck! This pilot study is crucial for validating our measurement approach. Take your time, be thoughtful, and don't hesitate to flag uncertainties.**
