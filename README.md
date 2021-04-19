# Analysis of data about particulate emissions in Sardinia

[![sardiniasustainability](https://circleci.com/gh/sardiniasustainability/air-quality.svg?style=svg)](https://app.circleci.com/pipelines/github/sardiniasustainability/air-quality)
* PDF (Sardinian) [![Latest version (Sardinian PDF)](https://img.shields.io/badge/download-latest-blue)](https://circleci.com/api/v1.1/project/github/sardiniasustainability/air-quality/latest/artifacts/0/tmp/pdf_sardinian/notes_srd.pdf)
* PDF (English) [![Latest version (English PDF)](https://img.shields.io/badge/download-latest-blue)](https://circleci.com/api/v1.1/project/github/sardiniasustainability/air-quality/latest/artifacts/0/tmp/pdf_english/notes_eng.pdf)

## Prerequisites
* To run the scripts, you'll need Python3 and Conda. 
* To generate the PDFs, you'll need to have a LaTex distribution.

## Running the scripts
```
cd python
# Activate environment
conda env create -n data-science -f environment.yml
source activate data-science
# Run scripts
python yearly_data_analysis.py
python daily_data_analysis.py
cd ..
```
The result can be seen in the generated folder called `figures`.

## Generating the PDFs
```
mkdir /tmp/pdf_sardinian /tmp/pdf_english
latexmk -output-directory=/tmp/pdf_sardinian -pdf notes_srd.tex
latexmk -output-directory=/tmp/pdf_english -pdf notes_eng.tex
```