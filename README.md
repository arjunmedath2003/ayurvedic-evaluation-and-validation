
# Ayurvedic Evaluation and Validation Using Bioinformatics and Deep Learning

An integrated computational framework for evaluating Ayurvedic formulations using **bioinformatics, protein–protein interaction networks, network clustering, pathway enrichment analysis, and Retrieval-Augmented Generation (RAG)**.

The project aims to bridge traditional Ayurvedic knowledge with modern computational biology by investigating the biological relevance of medicinal formulations and providing an evidence-oriented question-answering system.

----------

## Overview

Ayurveda contains extensive knowledge of medicinal plants, phytochemicals, and multi-ingredient formulations. However, systematically evaluating the biological relevance of these formulations and connecting traditional knowledge with molecular-level evidence remains a challenging task.

This project proposes an automated framework that combines biological data analysis and language models to support the computational evaluation of Ayurvedic formulations.

The framework consists of three major components:

1.  **Phytochemical and Bioinformatics Analysis:** Extracts phytochemical information and predicted protein targets associated with medicinal plants and Ayurvedic formulations.
    
2.  **Protein Network Analysis:** Constructs protein–protein interaction (PPI) networks, identifies functional clusters, and performs pathway enrichment analysis to investigate potential biological associations.
    
3.  **RAG-Based Ayurvedic Query System:** Integrates Ayurvedic literature and bioinformatics findings into a retrieval-based knowledge system that generates context-aware responses to domain-specific questions.
    

## System Architecture

```
flowchart TD
    A[Medicinal Plants and Ayurvedic Formulations]

    A --> B[Phytochemical Data Collection]
    B --> C[Phytochemical-Target Associations]
    C --> D[Protein Target Identification]

    D --> E[Protein-Protein Interaction Network]
    E --> F[Network Clustering]
    F --> G[Functional Cluster Identification]
    G --> H[KEGG Pathway Enrichment]

    H --> I[Biological Evidence Dataset]

    J[Ayurvedic Literature and Formulation Data]
    J --> K[Document Processing and Chunking]

    I --> L[Knowledge Base Integration]
    K --> L

    L --> M[Text Embedding Generation]
    M --> N[FAISS Vector Database]
    N --> O[Semantic Retrieval]
    O --> P[Large Language Model]
    P --> Q[Context-Aware Response]
```

## Methodology

### 1. Phytochemical Data Collection

The initial stage focuses on collecting phytochemical information associated with medicinal plants used in Ayurvedic formulations.

-   Uses the **IMPPAT (Indian Medicinal Plants, Phytochemistry and Therapeutics) database** as a source of phytochemical information.
    
-   Identifies phytochemical compounds associated with medicinal plants.
    
-   Collects predicted human protein targets associated with the identified compounds.
    
-   Organizes the collected information for downstream bioinformatics analysis.
    

### 2. Protein–Protein Interaction Network Construction

To investigate the biological relationships between identified protein targets, protein–protein interaction networks are constructed.

-   Uses the **STRING database** for human protein–protein interaction information.
    
-   Maps protein identifiers to their corresponding biological information.
    
-   Extracts interactions between identified target proteins.
    
-   Constructs interaction networks for individual medicinal plants and formulations.
    

### 3. Network Clustering and Functional Analysis

The constructed PPI networks are analyzed to identify groups of functionally related proteins.

Multiple clustering algorithms were investigated, including:

-   Louvain
    
-   Leiden
    
-   Infomap
    
-   Spectral Clustering
    
-   Affinity Propagation
    
-   Markov Clustering (MCL)
    
-   RNSC
    

Clustering approaches are evaluated using silhouette-based analysis to identify suitable network partitioning strategies.

The selected clusters are subsequently mapped to biological pathways to understand their potential functional relevance.

### 4. KEGG Pathway Enrichment Analysis

Functional enrichment analysis is performed to investigate the biological pathways associated with the identified protein clusters.

-   Maps protein identifiers to UniProt identifiers.
    
-   Performs pathway enrichment using KEGG-related annotations.
    
-   Uses enrichment resources such as Enrichr and DAVID.
    
-   Evaluates pathway associations using statistical significance measures, including p-values.
    

The resulting information provides a biological context for understanding the potential molecular associations of Ayurvedic formulations.

### 5. Automated Ayurvedic Analysis

The outputs from phytochemical analysis, protein interaction networks, clustering, and pathway enrichment are consolidated into a structured knowledge base.

This stage connects:

-   Ayurvedic formulations and their constituent medicinal plants.
    
-   Phytochemical compounds identified in those plants.
    
-   Predicted human protein targets.
    
-   Protein interaction networks and functional clusters.
    
-   Associated biological pathways.
    

The integrated dataset provides the biological evidence used by the downstream retrieval system.

### 6. Retrieval-Augmented Generation (RAG) System

A RAG-based question-answering system is developed to retrieve relevant information from Ayurvedic knowledge sources and computational bioinformatics results.

**Knowledge Base Preparation**

-   Processes Ayurvedic formulation information and biological analysis results.
    
-   Converts structured and unstructured information into retrievable text chunks.
    
-   Combines Ayurvedic knowledge with protein target, cluster, and pathway information.
    

**Embedding Generation**

Multiple embedding models are explored for semantic representation:

-   `all-mpnet-base-v2`
    
-   `bge-large`
    
-   `e5-large-v2`
    

**Vector Database**

-   Uses FAISS for efficient vector similarity search.
    
-   Stores generated embeddings and their corresponding document chunks.
    
-   Retrieves relevant contextual information based on user queries.
    

**Language Model Integration**

Multiple language models are investigated for response generation, including:

-   Phi-3 Mini
    
-   Mistral
    
-   Llama
    
-   Qwen
    
-   DeepSeek
    

The retrieved context is supplied to the selected language model to generate responses grounded in the available knowledge base.

**Retrieval Pipeline**

1.  User submits a question related to an Ayurvedic formulation.
    
2.  The question is converted into a semantic embedding.
    
3.  FAISS retrieves the most relevant knowledge chunks.
    
4.  Retrieved information is passed to the language model as context.
    
5.  The model generates a response using the retrieved information.
    
## Repository Structure

```
ayurvedic-evaluation-and-validation/
│
├── automation/
│   └── Automated analysis workflows
│
├── data_collection/
│   └── Data collection and preprocessing
│
├── dataset/
│   └── Ayurvedic and bioinformatics datasets
│
├── rag/
│   └── RAG-related resources and implementation
│
├── clustering.ipynb
│   └── Protein interaction network clustering
│
├── csv_to_protein.ipynb
│   └── Protein identifier mapping and processing
│
├── embedding.ipynb
│   └── Text embedding generation
│
├── rag model.ipynb
│   └── RAG pipeline implementation
│
├── rag model test.ipynb
│   └── RAG model experimentation and testing
│
├── review2_results.ipynb
│   └── Experimental analysis and review results
│
├── test_questions.json
│   └── Test questions for evaluating the query system
│
└── THE AYURVEDIC FORMULARY OF INDIA.pdf
    └── Reference material
```

## Experimental Evaluation

The framework involves experimentation across multiple stages:

-   Comparison of network clustering algorithms using silhouette-based evaluation.
    
-   Analysis of protein interaction networks and their functional clusters.
    
-   Investigation of biological pathways associated with Ayurvedic formulations.
    
-   Comparison of embedding models for semantic retrieval.
    
-   Evaluation of different language models for context-aware answer generation.
    
-   Assessment of retrieval and response quality using a predefined set of test questions.
    

The experiments help identify suitable configurations for integrating traditional Ayurvedic knowledge with computational biological evidence.

The project uses the following scientific resources:

-   **IMPPAT:**  [Indian Medicinal Plants, Phytochemistry and Therapeutics](https://cb.imsc.res.in/imppat/)
    
-   **STRING:**  [Protein–Protein Interaction Database](https://string-db.org/)
    
-   **UniProt:**  [Protein Knowledgebase](https://www.uniprot.org/)
    
-   **KEGG:**  [Kyoto Encyclopedia of Genes and Genomes](https://www.genome.jp/kegg/)
    
-   **Enrichr:**  [Gene Set Enrichment Analysis](https://maayanlab.cloud/Enrichr/)
    
-   **DAVID:**  [Database for Annotation, Visualization and Integrated Discovery](https://davidbioinformatics.nih.gov/)
    

## Research Scope and Limitations

This project is a computational research framework intended to explore potential biological associations between Ayurvedic formulations and molecular pathways.

-   Predicted protein targets and PPI associations do not establish direct biological interactions or therapeutic efficacy.
    
-   Pathway enrichment indicates statistical associations and requires further biological interpretation.
    
-   Computational findings should be validated through appropriate experimental and clinical studies.
    
-   RAG-generated responses depend on the quality, coverage, and reliability of the underlying knowledge sources.
    

**This framework is intended for research and educational purposes and is not a substitute for professional medical advice or clinical validation.**

## Acknowledgements

This project was developed as an undergraduate honours research project at the **Indian Institute of Information Technology Kottayam (IIIT Kottayam)**.

Special thanks to our project supervisor, **Dr. Manu Madhavan**, for his guidance and support throughout the research.

----------

**Project:** Ayurvedic Evaluation and Validation Using Bioinformatics and Deep Learning  
**Institution:** Indian Institute of Information Technology Kottayam  
**Repository:**  [ayurvedic-evaluation-and-validation](https://github.com/arjunmedath2003/ayurvedic-evaluation-and-validation)
