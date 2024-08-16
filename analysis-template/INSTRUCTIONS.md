# Analysis template

This is a template for a bioimage analysis.

## Experimental conditions

Describe the experimental conditions.

## Usage

How to run the analysis, input files, output files, dependencies, etc.

## File structure

```bash
analysis-template/
├── data/
│   ├── raw/
│   │   ├── image1.tif
│   │   ├── image2.tif
│   │   └── image3.tif
│   └── processed/
│       ├── image1_processed.tif
│       ├── image2_processed.tif
│       └── image3_processed.tif
├── results/
│   ├── ROI/
│   │   ├── image1.tif
│   │   ├── image2.tif
│   │   └── image3.tif
│   └── features.csv
├── src/
│   ├── analysis.py
│   └── utils.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Pipeline

[//]: https://mermaid.js.org/intro/

```mermaid
graph LR
    pre[Preprocessing] --> seg[Segmentation] --> ext[Feature extraction] --> mining[Data Mining]
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
