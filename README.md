<!---[![cffconvert](https://github.com/nlesc/python-template/actions/workflows/cffconvert.yml/badge.svg)](https://github.com/nlesc/python-template/actions/workflows/cffconvert.yml)
[![sonarcloud](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/sonarcloud.yml/badge.svg)](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/sonarcloud.yml)
-->
[![markdown-link-check](https://github.com/ptypes-nlesc/stereotype-map/actions/workflows/markdown-link-check.yaml/badge.svg)](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/markdown-link-check.yaml) 
[![python-package](https://github.com/ptypes-nlesc/stereotype-map/actions/workflows/python-package.yml/badge.svg)](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/python-package.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ptypes-nlesc_data-profiling&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ptypes-nlesc_data-profiling)

### Motivation
We aim to connect stereotypes found in online pornography (through short text descriptions) with the most relevant video titles and tags. Additionally, we seek to explore and analyze the tags to understand their correlations and the frequency of their co-occurrence within the same videos, along with the reasons behind these patterns.

### Requirements
Python 3.9+
Python environement can be isolated using venv.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Data setup
We expected data to be in a single csv file with each line containing a single video and columns containing meta data such as categories, upvotes, downvotes, and views.

### Examples

![alt text](https://github.com/ptypes-nlesc/stereotype-map/blob/main/plots/video_stereotype_graph.png)


### Documentation



