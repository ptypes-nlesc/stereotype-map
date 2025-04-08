<!---[![cffconvert](https://github.com/nlesc/python-template/actions/workflows/cffconvert.yml/badge.svg)](https://github.com/nlesc/python-template/actions/workflows/cffconvert.yml)
[![sonarcloud](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/sonarcloud.yml/badge.svg)](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/sonarcloud.yml)
-->
[![markdown-link-check](https://github.com/ptypes-nlesc/stereotype-map/actions/workflows/markdown-link-check.yaml/badge.svg)](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/markdown-link-check.yaml) 
[![python-package](https://github.com/ptypes-nlesc/stereotype-map/actions/workflows/python-package.yml/badge.svg)](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/python-package.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ptypes-nlesc_data-profiling&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ptypes-nlesc_data-profiling)
[![RSD](https://img.shields.io/badge/rsd-ptypes-blue)](https://research-software-directory.org/projects/ptypes)
[![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/ptypes-nlesc/stereotype-map)
[![github license badge](https://img.shields.io/github/license/ptypes-nlesc/stereotype-map)](https://github.com/ptypes-nlesc/stereotype-map)
[![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu)


## 💡 Motivation

This project investigates how gendered and racialized stereotypes are produced, reinforced, or contested through the metadata of online pornographic content.
By analyzing a large-scale dataset of video titles and tags from PornHub, the goal is to examine how classificatory systems—such as tags and titles participate in the construction and circulation of stereotypes.
In this way we can better understand how stereotypes are not only embedded in video content but also reinforced through digital infrastructures and linguistic classifications. 

## 🧠 Methodology Overview

This project analyzes metadata from over **200,000 PornHub videos** published between 2008 and 2018, focusing on **titles and tags** as classificatory tools that shape content visibility and access. The dataset also includes additional metadata such as:

- Publication date  
- View counts  
- Upvotes and downvotes  
- Production information  
- Actor details  

---

### 🔧 Preprocessing

Standard text preprocessing steps were applied to ensure data quality and consistency:

- Tokenization of titles and tags  
- Lowercasing of text  
- Removal of stopwords, special characters, and non-informative tokens  
- Deduplication of near-identical entries  

These steps ensured that the analysis focused on linguistically meaningful content.

---

### 🧩 NLP Techniques

We adapted short-text NLP techniques to analyze the **structural and semantic properties** of the metadata:

- **Part-of-Speech (POS) Tagging**  
  Identifies grammatical roles and recurring syntactic patterns.

- **Dependency Parsing**  
  Examines how **gendered** and **racialized** terms are positioned within phrases, revealing structural relationships.

- **Bigram and Trigram Modeling**  
  Captures frequently occurring word sequences and stereotypical expressions.

- **Co-occurrence Analysis**  
  Tracks patterns between gendered and racialized terms across time and content categories.


### Requirements
Python >=3.9 and <3.13
Python environment can be isolated using venv.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Data setup
We expected data to be in a single csv file with each line containing a single video and columns containing meta data such as categories, upvotes, downvotes, and views.

### Examples

![alt text](https://github.com/ptypes-nlesc/stereotype-map/blob/main/plots/heatmap_distilroberta-base-paraphrase-v1.png)

### Documentation



