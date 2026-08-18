# 🖥️ Host System Hardware Profile & Diagnostics

This benchmark suite was evaluated on the physical host machine detailed below. The hardware profile was captured using native `fastfetch` runtime execution.

## 1. Physical Host System
* **Manufacturer:** LENOVO
* **Model Family:** LOQ 15IAX9E (Model 83LK / IdeaPad Gaming)
* **SKU:** `LENOVO_MT_83LK_BU_idea_FM_LOQ 15IAX9E`
* **Host Name:** `RAQUIM`

## 2. Central Processing Unit (CPU)
* **Processor:** 12th Gen Intel(R) Core(TM) i5-12450HX
* **Core Configuration:** 8 Physical Cores (4 Performance Cores + 4 Efficient Cores), 12 Logical Threads
* **Clock Speeds:** 2.69 GHz Base Clock, 4.40 GHz Maximum Turbo Boost
* **Microarchitecture:** `x86_64-v3`
* **L3 Cache:** 12 MB Intel Smart Cache

## 3. Graphics & Acceleration (GPU)
* **Discrete Dedicated GPU:** NVIDIA GeForce RTX 2050
  * **Dedicated VRAM:** 4.0 GB GDDR6 (4,154,458,112 bytes)
  * **Driver Version:** 32.0.16.1088 (WDDM 3.2)
  * **CUDA Compute Capability:** 8.6 (Ampere Architecture, 2048 CUDA Cores)
  * **Quantix Hardware Capability Tier:** **Tier 1–2 (Optimal for Gemma-2-2B / Llama-3.1-8B Q4_K_M)**
* **Integrated GPU:** Intel(R) UHD Graphics 770 (Shared System Memory: 6.0 GB)

## 4. System Memory & Storage
* **Physical RAM:** 12.0 GB DDR5 RAM (12,595,355,648 bytes)
* **Storage Device:** 512 GB NVMe PCIe 4.0 SSD (NTFS Volume `Windows-SSD`)
* **Pagefile / Virtual Memory:** 16.0 GB Swapfile (`C:\pagefile.sys`)

## 5. Software & Execution Environment
* **Operating System:** Microsoft Windows 11 Home Single Language (64-bit, Build 25H2 / 26100.8655)
* **Node.js Runtime:** v20.14.0 (V8 Engine v12.4.254.20)
* **Electron Framework:** v30.0.9
* **Shell:** PowerShell v7.6.3 (pwsh)
* **LLM Engine:** Ollama v0.3.4 (llama.cpp backend with CUDA acceleration)
* **Vector Engine:** `@lancedb/lancedb` v0.6.14 (Apache Arrow in-process)
