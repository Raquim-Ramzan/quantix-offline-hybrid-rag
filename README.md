# 🔬 Quantix Sovereign Hybrid RAG: Empirical Benchmarks & Research Artifacts

> **Official Evaluation Harness, Raw Benchmark Datasets, Hardware Diagnostics, and Research Manuscripts for the Quantix Zero-Network Sovereign Hybrid RAG Platform.**

---

## 💻 Primary Hardware Testbed: Lenovo LOQ 15IAX9E

> [!IMPORTANT]
> All empirical benchmarks, latency traces, peak memory resident set size (RSS) profiling, and retrieval/QA evaluations reported in **`Quantix_Offline_Hybrid_RAG_Draft_2.0`** were measured on this physical host machine using native diagnostic hooks (`fastfetch`, Node.js `process.memoryUsage()`, and high-resolution performance timers).

```
╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║                                 TESTBED HARDWARE SPECIFICATION                            ║
╠═══════════════════════════════════════════════════════════════════════════════════════════╣
║  • Host System:         Lenovo LOQ 15IAX9E (Model 83LK / IdeaPad Gaming)                  ║
║  • Hostname:            RAQUIM                                                            ║
║  • Processor (CPU):     12th Gen Intel(R) Core(TM) i5-12450HX (8 Cores, 12 Threads)       ║
║                         - Base Frequency: 2.69 GHz | Max Boost: 4.40 GHz                  ║
║                         - Architecture: x86_64-v3 | 12MB Intel Smart Cache               ║
║  • Discrete GPU:        NVIDIA GeForce RTX 2050 (4.0 GB GDDR6 Dedicated VRAM)             ║
║                         - VRAM Total: 4,154,458,112 bytes | Driver: 32.0.16.1088          ║
║                         - Target Capability Tier: Tier 1–2 (Quantix Dynamic Router)       ║
║  • Integrated GPU:      Intel(R) UHD Graphics 770 (Shared RAM: 6.0 GB)                   ║
║  • System Memory (RAM): 12.0 GB DDR5 RAM (12,595,355,648 bytes physical)                 ║
║  • Primary Storage:     512 GB NVMe PCIe 4.0 SSD (NTFS Windows-SSD, 434 GB used)         ║
║  • Display:             1920 × 1080 Full HD @ 144.00 Hz (BOE0C29, 120 DPI)               ║
║  • Operating System:    Windows 11 Home Single Language (Build 25H2 / 26100.8655)         ║
║  • Kernel / Shell:      WIN32_NT 10.0.26200 / PowerShell 7.6.3 (pwsh)                     ║
║  • Diagnostic Tool:     fastfetch v2.38.0 (Windows Native x64 Package)                    ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
```

---

## 📁 Repository & Folder Architecture

```
offline_hybrid_rag_benchmarks/
├── README.md                           # Master Benchmark & Replication Guide (This Document)
├── hardware_profile/                   # Native Host Diagnostics & Hardware Metadata
│   ├── fastfetch_raw.json              # Raw JSON output from native Fastfetch system scan
│   └── system_specifications.md        # Comprehensive hardware tiering & memory architecture
├── raw_data/                           # Raw Empirical Benchmark Results (JSON & CSV)
│   ├── latency_benchmarks.json         # Subsystem latency percentiles (Min, Med, p95, p99)
│   ├── latency_benchmarks.csv          # Tabular latency breakdowns
│   ├── memory_rss_scaling.json         # Peak RSS (GB) vs. corpus scale (1M to 27.2M entries)
│   ├── memory_rss_scaling.csv          # Tabular memory scaling metrics
│   ├── retrieval_qa_evaluations.json   # NQ-Open & TriviaQA accuracy, Recall@k, EM, F1
│   ├── retrieval_qa_evaluations.csv    # Tabular QA metrics across 5 configurations
│   └── ablation_studies.json           # Raw ablation traces (ZIM removal, TypedArray vs GC)
├── scripts/                            # Benchmark Execution & Verification Harnesses
│   ├── evaluate_hybrid_rag.py          # Master evaluation harness reproducing all paper tests
│   ├── zim_typed_array_indexer.py      # Algorithm 1: In-place typed-array binary search engine
│   └── rrf_fusion_evaluator.py         # Reciprocal Rank Fusion scoring module (k = 60)
└── papers_and_reports/                 # Peer-Review Drafts & Research Manuscripts
    ├── Quantix_Offline_Hybrid_RAG_Draft_2.0.docx  # Formatted Word manuscript (IEEE template)
    └── Quantix_Offline_Hybrid_RAG_Draft_2.0.md    # Markdown reference manuscript
```

---

## 📊 Summary of Benchmark Results

### 1. Subsystem Latency Distribution (Lenovo LOQ Testbed)
* **ZIM Lexical Lookup (`Uint32Array` / `Uint16Array`)**: Median **38.4 ms** (p95: 48.2 ms, p99: 64.1 ms) across 27,243,180 records.
* **On-Demand Text Extraction & Cleaning**: Median **22.6 ms** per article chunk.
* **LanceDB In-Process Vector Query**: Median **18.6 ms** (768-dimensional `nomic-embed-text-v1.5`).
* **Okapi BM25 Sparse Search**: Median **9.4 ms**.
* **RRF Rank Fusion ($k = 60$)**: Median **2.1 ms**.
* **End-to-End Local RAG (Gemma-2-2B / RTX 2050)**: Median **890 ms** (Time-to-First-Token: **78 ms**).

### 2. Peak Resident Memory (RSS) Scaling
| Corpus Size (Records) | Naive JS String Heap | kiwix-js Browser | libzim (C++) | Quantix Typed-Array |
| :--- | :--- | :--- | :--- | :--- |
| **1,000,000 (1M)** | 0.42 GB | 0.18 GB | 0.14 GB | **0.11 GB** |
| **5,000,000 (5M)** | 1.28 GB | 0.44 GB | 0.36 GB | **0.28 GB** |
| **15,000,000 (15M)** | 2.94 GB | 0.92 GB | 0.78 GB | **0.69 GB** |
| **27,243,180 (Full 27.2M)** | 4.85 GB *(Crash/OOM)* | 1.45 GB | 1.32 GB | **1.18 GB (Bounded)** |

### 3. Retrieval & QA Generation Quality (NQ-Open + TriviaQA)
| Configuration | Recall@5 | Recall@10 | MRR@10 | Exact Match (%) | Token F1 (%) | LLM Judge (1-5) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Dense-Only (LanceDB)** | 78.4% | 83.2% | 0.724 | 41.2% | 58.6% | 3.82 / 5.00 |
| **Lexical-Only (BM25)** | 71.9% | 76.8% | 0.681 | 36.8% | 52.1% | 3.54 / 5.00 |
| **ZIM Title Only (kiwix-js)** | 64.2% | 70.1% | 0.612 | 31.5% | 46.7% | 3.21 / 5.00 |
| **Hybrid (Dense + BM25)** | 86.5% | 91.4% | 0.804 | 46.8% | 64.5% | 4.18 / 5.00 |
| **Quantix Full Hybrid RAG** | **94.2%** | **97.1%** | **0.884** | **52.6%** | **71.8%** | **4.62 / 5.00** |

---

## 🛠️ Quick Reproduction Commands

```bash
# Navigate to the benchmark suite
cd offline_hybrid_rag_benchmarks/scripts

# 1. Run the master evaluation suite (measures latency, memory RSS, and RRF quality)
python evaluate_hybrid_rag.py

# 2. Test Algorithm 1: Typed-Array in-place binary search & range scan
python zim_typed_array_indexer.py --query "Quantum superposition"

# 3. Test Reciprocal Rank Fusion scoring
python rrf_fusion_evaluator.py
```
