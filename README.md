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

### Motivation
We aim to connect stereotypes that are found in online pornography (through short text descriptions) and videos that contain that stereotype (titles and tags). Additionally, we seek to explore and analyse the tags: 
- to understand their correlations;
- the frequency of their co-occurrence within the same videos;
- the reasons behind these patterns.

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



