# Frameworks — data (F159–F169)

## F159 · Filter data to the one valuable insight
**Also known as:** The SAFE Process (Edwards); Data Information Knowledge Wisdom (DIKW) Pyramid (Lo Duca)
**Use when:** Turning a large pile of numbers into a talk, report or dashboard for decision-makers who are not data specialists.
**Avoid when:** A stakeholder explicitly asks for the full unfiltered data dump (Edwards). Also not suited to gigabyte-scale analytics or heavy exploration, where dedicated BI tools fit better (Lo Duca).
**Steps:**
1. Source and clean the data: run the numbers or gather existing datasets, then fix missing values, formats and outliers.
2. Analyse what the data means for this audience: check their goals, public statements and role pressures, and filter out irrelevant categories. Compute comparable metrics (for example percentage change instead of raw counts).
3. Isolate the single fact, figure or insight of highest value to them. This becomes the payoff of the story (Edwards).
4. Cut everything without meaning for the audience. Remove charts from the main deck, using a naive colleague to help you let go, or move them to a leave-behind appendix (Edwards).
5. Add context: background, causes, benchmarks, annotations and images matched to the audience (Lo Duca's knowledge layer).
6. Close with an ethically grounded next step and a call to action (Lo Duca's wisdom layer); see F168.
**Common mistakes:** Keeping every chart because it took effort to make. Showing raw totals when a normalized metric carries the insight.
**Example:** A hospital analyst has 40 charts on ambulance response times. She learns the board cares about penalty fees, so she finds that night-shift delays in one district triggered 80% of fines. The deck opens with that finding, and the other 39 charts go into an appendix. A colleague who knows nothing of the project reads the deck and points out two more slides to cut.
**Sources:** Edwards; Lo Duca

## F160 · Data story arc
**Also known as:** Data Storytelling Arc Mapped to DIKW (Lo Duca)
**Use when:** A visualization needs to read as a complete story and not as an isolated chart.
**Steps:**
1. Extract the main point first: find and isolate the central insight in the data.
2. Build background and a hook around it: add scene-setting context and a notable turning-point observation that frames the problem or opportunity.
3. Prompt reflection and next steps: leave the audience room to think, then present concrete actions or calls to action.
4. Lay out the finished piece in reader order: background, then insight, then action. The author discovers the insight first, but the reader should not meet it first.
**Common mistakes:** Presenting the chart in the order you built it, so the reader gets the insight with no context.
**Example:** A city planner finds that bike-lane collisions fell 30% on streets with painted buffers. She builds the main chart, then adds a subtitle about the neighborhood that lobbied for buffers and a photo of a school route as the hook. Next to the chart she places a three-street rollout map for the coming year. Readers see the context, then the drop, then the plan.
**Sources:** Lo Duca

## F161 · Insight extraction lenses
**Also known as:** Four Insight-Extraction Strategies (Lo Duca)
**Use when:** You hold a cleaned dataset and must decide which story is worth telling.
**Avoid when:** You only have automated charts and no domain knowledge: the lenses need experience to tell cause from chance (Lo Duca).
**Steps:**
1. Connections: pick out the key data points (aggregated metrics above all), tie them into a pattern and drop what does not matter.
2. Coincidences: stay skeptical of aligned events. Ignore one-offs, investigate repeats in the raw time series, and test whether an earlier variable could be the cause.
3. Curiosity: probe anomalies, outliers, missing values, gaps and sudden spikes, looking from several outside angles.
4. Contradictions: challenge places where the data disagrees with a common assumption to expose a hidden driver (for example a price rise that lifts sales through perceived value or scarcity).
**Common mistakes:** Treating a one-time alignment of events as a cause.
**Example:** A library analyst totals weekly loans per branch, a connection that shows the two riverside branches growing while the rest stay flat. Loans spike once after a storm, a one-off she ignores, but the dip recurs every August and she checks the raw series for a cause. A gap of missing Tuesdays at one branch prompts a curiosity check, and it traces to a broken door counter. The contradiction is that a fine increase did not reduce loans, which points her to automatic renewals as the hidden driver.
**Sources:** Lo Duca

## F162 · Hero, guide and adversary in data
**Also known as:** Story Characters Framework: Hero, Guide, Adversary (Lo Duca)
**Use when:** Designing a data story before choosing colors, annotations or framing.
**Steps:**
1. Choose the hero: the main subject of the story (a person, product, process or place, never the analyst). State early what the hero wants so the audience wonders whether it will get it.
2. Name the guide: the mentor, dataset or insight that helps the hero reach the goal.
3. Pick the adversary: a comparison entity of the exact same type as the hero, such as a competitor, a benchmark, or the hero at another time or place.
**Common mistakes:** Leaving the hero's goal undefined, so nobody cares about the comparison.
**Example:** A regional train line is the hero, and it wants to reach 95% on-time arrivals. Its own 2019 record is the adversary, drawn as a grey line behind the current one. A rider survey is the guide, showing which delays riders notice most. The chart title says the line is closing the gap.
**Sources:** Lo Duca

## F163 · Chart choice by data relationship
**Also known as:** Three Levels of Storytelling & Chart Selection (Lo Duca); Andy Kirk's CHRT(S) (Feigenbaum)
**Use when:** Selecting a chart family for a specific relationship in the data and a specific audience goal.
**Avoid when:** Tables from different sources have incompatible samples and cannot be merged into one chart (Feigenbaum). Pie or donut charts fail with more than two or three slices or near-identical sizes (Lo Duca).
**Steps:**
1. Decide the level: inform (just the insight), communicate (tuned to a given audience) or inspire (adds an action that people will retell) (Lo Duca).
2. Name the relationship in the data and pick from the matching family. Lo Duca: single number (big number, donut, waffle); parts of a whole (pie, donut, 100% stacked bar); comparison (bar, column, slope graph, dumbbell); trend (line, small multiples, stacked area); survey outcomes (stacked bars); distribution (histogram, box plot); relationship (scatter, bubble, heatmap); spatial (choropleth, dot density); flow (Sankey, chord).
3. Cross-check with Kirk's five families (Feigenbaum): categorical (bar, pictogram), hierarchical (treemap, stacked bar), relational (network, Sankey), temporal (line, slope graph, Gantt), spatial (heat map, flow map).
4. For multi-select survey results that total over 100%, use separate single-value charts, not one pie.
**Common mistakes:** Picking the chart before naming the relationship; forcing a part-to-whole chart on data that does not sum to a whole.
**Example:** A school district wants to show three things to its board. Test scores over five years are a trend, so she draws a line chart with one line per school. The budget split among salaries, buildings and supplies is parts of a whole, so she uses a 100% stacked bar. Commute times are a distribution, so she uses a histogram, and she titles the last chart with a request for a new bus route to move the piece from communicate to inspire.
**Sources:** Lo Duca; Feigenbaum

## F164 · Data audience literacy tiers
**Also known as:** Audience Calibration Taxonomy (Lo Duca); Five Levels of Data Literacy (Feigenbaum)
**Use when:** One insight must go to several audiences (public, board, specialists, funders) in different versions.
**Steps:**
1. Place the reader on a tier. Lo Duca has three: general public, executives, professionals. Feigenbaum has five: novice, generalist, colleague, expert, trustee or funder.
2. General public or novice: simple, precise language, visual appeal, a simple ratio, personal relevance, brevity and a link to more. Remove baselines, complex axes and dense statistics.
3. Executives or generalists: lead with the key trend, the baseline and the recommendation, in their domain language, with uncluttered charts.
4. Professionals, colleagues and experts: exact values, method, assumptions, limits, references and shorthand. Experts care about how more than what, so expect method questions.
5. Funders and trustees: clarity, brevity, the challenge paired with decision options, emotion, and a framing that helps them look good.
6. Build one version per tier and link the lighter versions to the deeper ones.
**Common mistakes:** Sending one version to everyone. Assuming educated readers will push through a dense chart when they are short on time or confidence (Feigenbaum).
**Example:** A school district finds absences cluster on Mondays after long weekends. Parents, as novices, get one ratio (one child in six misses that Monday) and a link to the full report. Teachers, as colleagues, get the weekly pattern by grade with the method noted. The district's foundation, as funder, gets the problem in two sentences, two options to fund, and a framing it can announce as its own win.
**Sources:** Lo Duca; Feigenbaum

## F165 · Prompt schemas for generative AI
**Also known as:** Prompt Engineering Schemas for GenAI Assistants (Lo Duca)
**Use when:** Using an AI assistant to produce titles, subtitles, commentary, annotations, images or chart code for a data story.
**Avoid when:** You are not prepared to check the output by hand: results vary between runs and can invent nonexistent library methods (Lo Duca).
**Steps:**
1. Text prompt: state the role (entertainer, educator, informer, inspirer, invitor to action or relationship builder), the audience, the topic (scenario, data and insight, with source text set off in angle brackets) and the output type (title, subtitle, commentary or annotation) with an exact length limit.
2. Image prompt: state the subject, enriched with adjective, emotion, background and color, then the style (photograph, digital art, cartoon, an artist's style).
3. Code prompt: write the task as a sequence of comment lines: imports and data load, then data transformations, then one mark with its encodings and conditions, then layout, then save.
4. Read the output, edit it and test the code before use.
**Common mistakes:** Pasting AI output into a chart without inspection.
**Example:** A leisure-centre manager is making a poster for swimmers about how busy the lanes get by hour. Her text prompt casts the assistant as an educator, names the audience as members with no data background, gives the pool's six-week entry counts with the note that lanes are emptiest from 2 to 4 p.m., and asks for one annotation of at most 18 words. For the poster image she asks for a calm, nearly empty lane under afternoon light, pale blue, as a watercolor, and for the chart she writes comment lines from loading the counts to saving a bar chart as HTML. She trims the annotation, fixes one axis label the generated code got wrong, and only then prints.
**Sources:** Lo Duca

## F166 · Base model, fine-tuning or retrieval
**Also known as:** LLM Extension Criterion: Base Prompting vs. Fine-Tuning vs. RAG (Lo Duca)
**Use when:** An off-the-shelf assistant lacks your private facts, up-to-date data or a steady house format for stories that recur.
**Avoid when:** The model needs no special domain knowledge. Then use the standard assistant, optionally with custom instructions.
**Steps:**
1. Ask whether the model must know specific domain, product or proprietary information. If not, stay with the base model.
2. For recurring stories with a fixed title and annotation structure for the same audience, fine-tune: prepare at least 10 prompt and completion pairs in JSONL, train, and benchmark against the base model.
3. For long external documents or live product knowledge, use retrieval: load the documents, split into overlapping chunks, embed them in a vector database, and query with a strict context-only prompt at temperature 0.
4. Check licenses on any scraped training source.
**Common mistakes:** Scraping unlicensed content for training data (Lo Duca).
**Example:** A regional bank publishes the same monthly branch-traffic chart with a fixed title and annotation format, so analysts fine-tune a model on 24 past title and annotation pairs. For notes on its lending-policy handbook, which is long and revised often, they load the handbook into a retrieval pipeline and ask for answers from that context only. A general headline helper with no bank-specific knowledge stays on the base model.
**Sources:** Lo Duca

## F167 · Emotion and placement in data visuals
**Also known as:** Visual Emotion Matrix & Strategic Placement (Lo Duca)
**Use when:** Styling a chart, choosing imagery, or laying out a multi-panel story.
**Avoid when:** You are tempted to combine opposing moods in one static chart. Split them behind an interactive selector.
**Steps:**
1. Pick an emotion quadrant by energy and mood (adapted from Decker): high energy positive (bright, vibrant), high energy negative (dark, threatening), low energy positive (light, calm), low energy negative (muted, somber). Use it for palette and image keywords.
2. Place overview text and sources at the top, never images, which distract. Put deeper background, emotional photos and secondary charts on the left. Put short callouts, baselines and icons inside the chart without covering data.
3. Put a short action directive in the title. Put detailed recommendations, allocation charts, roadmaps or interactive boxes to the right or below the chart.
**Common mistakes:** A cheerful palette on a loss chart; a photo placed above the overview text.
**Example:** A wildlife park charts a rise in weekend visitors, a high-energy positive story. The line is bright orange, and a photo of children at the otter pool sits on the left. The overview text and source are at the top, a short callout about the record Saturday sits inside the chart, and the title asks readers to add shuttle buses. A roadmap of the shuttle rollout sits below the chart.
**Sources:** Lo Duca

## F168 · Next steps, call to action and ethical check
**Also known as:** Next Steps, Call to Action (CTA), & Ethical Anchoring (Lo Duca)
**Use when:** Finalizing recommendations and auditing any AI-assisted data story before release.
**Avoid when:** You plan to rely on the AI check alone: bias and hallucination cannot be fully removed, so a human must judge (Lo Duca).
**Steps:**
1. Define what to do by category: awareness, collaboration, advocacy and policy, training, strategic action, or engagement and communication.
2. Choose how people act: learn (links), share (buttons), act (specific steps), follow a roadmap (timeline), interact (simulation or click filters), or get support (FAQ, contact).
3. Reframe the next steps under an ethical lens (adapted from Berengueres): utilitarianism, duty, virtue, or care. Verify the result by hand.
4. Audit every AI-generated asset against four pillars: human rights and dignity, peaceful and just societies, diversity and inclusiveness, environmental flourishing.
5. Credit data sources, AI tools and any retrieval or fine-tuning documents under the title, under the chart, under the next steps or at the side.
**Common mistakes:** Releasing an AI-made image or caption unchecked.
**Example:** A county health office charts flu hospitalizations by age group. The next step is an act mechanism: a short list of three steps for parents, with a link to clinic hours. The analyst asks the assistant to reframe the message under care ethics, edits the result by hand, and checks the AI-made illustration for diversity in the people shown. Credits for the data and the AI tool sit under the chart.
**Sources:** Lo Duca

## F169 · Data and advocacy story patterns
**Also known as:** Data Storytelling & 1–2 Minute Advocacy Frameworks (Bowles)
**Use when:** Presenting research or metrics at work, or giving short advocacy testimony without a full stage slot.
**Avoid when:** Piling on statistics: too many collapse the emotional focus, so treat data as seasoning (Bowles).
**Steps:**
1. For a data presentation, choose one pattern: open with a personal story that sets the why before the slides; let one long story serve as the backbone with data points placed along it; or insert a short story mid-deck at one critical metric.
2. For a 1 to 2 minute advocacy piece, shrink the main event scene to about 60 seconds and add only the two or three background facts a newcomer cannot do without.
3. Tailor details to the listeners (lawmakers, nurses, parents) and add 1 or 2 sharp figures that show scale.
4. End with an explicit ask.
**Common mistakes:** Drowning the human moment in numbers.
**Example:** A school nurse has two minutes before a county board. She describes one afternoon when a student's inhaler was locked in a cabinet and the office was empty. She adds that 1 in 9 students at her school has asthma and the clinic is staffed two days a week. She asks the board to fund a full-time nurse.
**Sources:** Bowles
