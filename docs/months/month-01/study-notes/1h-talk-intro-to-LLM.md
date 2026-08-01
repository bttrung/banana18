## [1hr Talk] Intro to Large Language Models
Link: https://www.youtube.com/watch?v=zjkBMFhNj_g

### The talk’s key takeaways

**What LLMs Really Are**
- A large language model can be viewed as two main artifacts: a huge parameter file (e.g., 70B parameters ≈ 140 GB for LLaMA 2 70B) and relatively small code that implements the network and runs those parameters to generate text.

- Training creates a lossy `compression of the internet`: massive text (≈ tens of terabytes) is distilled into parameters via next‑token prediction, so the model stores a gestalt of world knowledge rather than exact copies of documents.

**Core Training and Behavior**
- The basic training objective is to predict the next word, but solving this well forces the model to internalize rich facts, concepts, and relationships about the world in its weights.

- After training, the model `dreams` internet‑like documents when prompted—sometimes factually correct, sometimes hallucinated—because it samples from the learned text distribution rather than retrieving exact stored pages.

**From Base Model to Assistant**
- There is a first stage, pre‑training on large, messy internet text, producing a base model that is good at free‑form generation but not aligned to user needs.

- A second, cheaper stage, fine‑tuning on curated question–answer conversations written or supervised by humans, transforms the base generator into a helpful assistant while reusing the pre‑trained knowledge.

**Additional Alignment Stage (RLHF)**
- A third optional stage uses comparison data (humans ranking alternative answers) rather than writing answers from scratch, enabling reinforcement learning from human feedback (RLHF) to further shape behavior.

- This approach leverages the fact that humans often find it easier to judge which answer is better than to author a perfect answer themselves.

**Closed vs Open Models and Evaluation**
- Strongest models today tend to be closed‑weight systems served via APIs or web UIs, while open‑weight models (e.g., LLaMA 2 variants) are slightly weaker but fully inspectable and fine‑tunable.

- Crowdsourced “arena” evaluations, analogous to chess ELO, reveal that proprietary systems currently lead in quality, with open models chasing but offering more flexibility for customization.

**Scaling Laws and the AI “Gold Rush”**
- Performance on next‑word prediction—and correlated real‑world benchmarks—improves in a predictable way as you scale two variables: number of parameters and amount of training data.

- Because these scaling laws show no clear saturation, organizations can reliably get better models simply by using larger compute clusters and more data, driving massive investment in GPUs and training runs.

**Tool Use and Agentic Behavior**
- Modern LLMs increasingly solve tasks by orchestrating tools (web browsers, calculators, Python interpreters, image generators) rather than “thinking” only in text.

- This tool‑calling ability makes them closer to general problem‑solving engines that can search, compute, visualize, and create media in response to natural language instructions.

**Multimodality**
- LLMs are becoming multimodal: they can not only produce text but also see images, generate images, and handle audio (speech‑to‑speech interfaces), broadening the range of tasks they can tackle.

- Examples include reading a hand‑drawn UI mockup and writing working HTML/JS code, or conversing with users via voice in real time.

**System 1 vs System 2 Aspirations**
- Current models mostly operate in a “System 1” mode - fast, pattern‑based responses with a fixed per‑token compute budget.

- A key research frontier is giving them “System 2” capabilities: the ability to spend more time reasoning (e.g., exploring trees of thoughts) to trade latency for higher accuracy when the user is willing to wait.

**Self‑Improvement Challenges**
- In contrast to systems like AlphaGo, which can self‑improve by playing games against themselves with a clear win/loss reward, LLMs lack a simple, universal reward signal for arbitrary language tasks.

- Self‑improvement may be feasible in narrow domains with well‑defined rewards, but in general‑purpose language use it remains an open challenge.

**Customization and “App Store” Models**
- There is growing emphasis on customizing a general LLM into many specialist models (or “GPTs”) tailored to particular workflows or domains.

- Current customization levers include instructions and retrieval over user‑provided files; future directions likely include domain‑specific fine‑tuning and more sophisticated specialization.

**LLM as a New Operating System**
- Karpathy argues it is more accurate to think of an LLM as the kernel of a new operating system than as a simple chatbot.

- In this analogy, the LLM orchestrates memory (context window, external storage), tools (code, browsers, media generators), and multiple “expert” agents, much like a traditional OS coordinates CPU, RAM, disk, and processes.

**Emerging Security Issues**
- LLMs introduce new security challenges analogous to but distinct from traditional OS security, including jailbreaks, prompt injection, and data poisoning/backdoor attacks.

- Attackers can, for example, bypass safety via role‑play prompts, encoded inputs, hidden instructions in documents or images, and poisoned training data containing trigger phrases, while defenders continuously patch and harden systems in a cat‑and‑mouse dynamic.
