<!---[![cffconvert](https://github.com/nlesc/python-template/actions/workflows/cffconvert.yml/badge.svg)](https://github.com/nlesc/python-template/actions/workflows/cffconvert.yml)
[![sonarcloud](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/sonarcloud.yml/badge.svg)](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/sonarcloud.yml)
-->
[![markdown-link-check](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/markdown-link-check.yaml/badge.svg)](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/markdown-link-check.yaml) 
[![python-package](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/python-package.yml/badge.svg)](https://github.com/ptypes-nlesc/data-profiling/actions/workflows/python-package.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ptypes-nlesc_data-profiling&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ptypes-nlesc_data-profiling)

Python scripts for the https://research-software-directory.org/projects/ptypes project. This includes pre-processing scripts to clean, tokenize, remove stopwords, lemmatize, and sample as well data exploration utilities.

### Motivation
We want to associate stereotypes in online pornography (short text descripions) to the video tags they can be best described with. We also want to explore the tags and understand which tags are correlated and co-occur in the same video and why?

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
Coming soon

### Documentation



