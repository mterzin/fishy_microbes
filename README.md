# No-take marine reserves promote oligotrophic reef bacterioplankton communities across the Great Barrier Reef

This repository contains the code for the statistical analysis, machine learning, and integration of microbial and environmental data for the manuscript:

> **Title:** No-take marine reserves promote oligotrophic reef bacterioplankton communities across the Great Barrier Reef
> **Authors:** Marko Terzin<sup>1,2,3,*</sup>, Steven J. Robbins<sup>4</sup>, Kim-Anh Lê Cao<sup>5</sup>, Sara C. Bell<sup>1</sup>, Katherine E. Dougan<sup>4</sup>, Julian Zaugg<sup>4</sup>, Renee K. Gruber<sup>1</sup>, Michael J. Emslie<sup>1</sup>, Daniela M. Ceccarelli<sup>1</sup>, Samuel Chaffron<sup>6,7</sup>, Philip Hugenholtz<sup>4</sup>, Nicole S. Webster<sup>1,4,8</sup>, David G. Bourne<sup>1,2,3</sup>, Yun Kit Yeoh<sup>1,3</sup>, Patrick W. Laffy<sup>1,3,*</sup>
>
> <sup>1</sup>Australian Institute of Marine Science, PMB no3 Townsville MC, Townsville QLD 4810<br>
> <sup>2</sup>College of Science and Engineering, James Cook University, Townsville, 4811.<br>
> <sup>3</sup>AIMS@JCU, James Cook University, Townsville QLD 4811<br>
> <sup>4</sup>Australian Centre for Ecogenomics, School of Chemistry and Molecular Biosciences, The University of Queensland, St Lucia, QLD 4072<br>
> <sup>5</sup>Melbourne Integrative Genomics and School of Mathematics and Statistics, University of Melbourne, Melbourne, Parkville VIC 3052<br>
> <sup>6</sup>Nantes Université, École Centrale Nantes, CNRS, LS2N, UMR 6004, F-44000 Nantes, France.<br>
> <sup>7</sup>Research Federation for the Study of Global Ocean Systems Ecology and Evolution, FR2022/Tara Oceans GOSEE, F-75016 Paris, France.<br>
> <sup>8</sup>Institute for Marine and Antarctic Studies, University of Tasmania, TAS, 7001<br>
> <sup>*</sup>Corresponding authors
>
> **Status:** Preprint/In Review/Published (link to paper here)

## Project Overview

This study investigates the relationship between seawater microbiomes, environmental variables, and reef protection status (No-Take Marine Reserves vs. fished reefs) across the Great Barrier Reef (GBR). We integrated prokaryotic metagenome-assembled genomes (pMAGs), physico-chemical water data, benthic cover, and fish survey data to identify microbial indicators of reef zoning and predict environmental conditions from microbial community composition.

## Data Availability

All primary data used in this analysis are publicly available or available upon request:

*   **Metagenomic Sequences**: Available under EBI BioProject **[PRJEB82623](https://www.ebi.ac.uk/ena/browser/view/PRJEB82623)**.
*   **pMAGs:** Deposited on Zenodo: **[DOI: XXXXXXXX](https://doi.org/XXXXXXX)** (To be activated upon acceptance).
*   **Processed pMAGs and Abundance Tables:** 
*   **Physico-chemical Variables:** Available from the IMOS-AODN portal: [Australian Institute of Marine Science (AIMS). (2022). Great Barrier Reef Genomics Database: Seawater Illumina Reads.](https://doi.org/10.25845/Q4XH-YN10)
*   **Benthic Cover & Fish Data:** Managed by the AIMS Long-Term Monitoring Program (LTMP). Can be accessed via the AIMS data portal (https://apps.aims.gov.au/metadata/view/a17249ab-5316-4396-bb27-29f2d568f727)
*   **Code for Metagenomic Assembly & Binning:** Described in the companion preprint: Robbins et al. (2025). "The planktonic microbiome of the Great Barrier Reef". [https://www.biorxiv.org/content/10.1101/2025.05.13.653689v1](https://www.biorxiv.org/content/10.1101/2025.05.13.653689v1)

## Repository Structure

fishy_microbes/
├── data/
│ ├── processed/ # Processed CLR-transformed abundance tables, environmental data
│ └── raw/ # Links to raw data (see above)
├── figs/ # Generated output figures
├── scripts/
│ ├── 01_indicator_analysis.R # MINT sPLS-DA for microbial indicators
│ ├── 02_environment_integration.R # MINT sPLS for microbe-environment correlations
│ ├── 03_glmm_analysis.R # GLMMs for environmental variables
│ ├── 04_network_analysis.R # Network connectedness and cohesion
│ ├── 05_random_forest.R # Random Forest predictions
│ └── 06_niche_analysis.R # Microbial niche inference (Chaffron et al. 2021 method)
└── README.md


## Analysis Workflow

The code in this repository replicates the following key analyses:

### 1. Microbial Indicator Analysis (`01_indicator_analysis.R`)
- **Multivariate INTegration Sparse PLS-Discriminant Analysis (MINT sPLS-DA)** to identify prokaryotic metagenome-assembled genomes (pMAGs) that consistently discriminate between NTMRs and fished reefs across different GBR sectors, accounting for spatiotemporal confounding effects.

### 2. Correlation with Environmental Variables (`02_environment_integration.R`)
- **MINT Sparse PLS (MINT sPLS)** to integrate the identified microbial indicator abundances with 54 continuous environmental variables (physico-chemical, benthic cover, fish data) and identify key associations.

### 3. Testing Environmental Differences (`03_glmm_analysis.R`)
- **Generalised Linear Mixed Models (GLMMs)** using `glmmTMB` to test if key environmental variables (e.g., herbivore density, hard coral cover) significantly differ between protection zones, with nested random effects (sector, reef, site, transect).

### 4. Microbial Network Analysis (`04_network_analysis.R`)
- Calculation of **network connectedness** (microbe-specific) and **cohesion** (sample-specific) metrics to compare the structure of positive and negative microbial associations between NTMRs and fished reefs.

### 5. Environmental Predictions (`05_random_forest.R`)
- **Random Forest (RF) regression models** to predict continuous environmental variables from microbial abundance data (CLR-transformed). Models were validated using stratified, site-aware repeated train-test splits.

### 6. Microbial Niche Inference (`06_niche_analysis.R`)
- Inference of **microbial niche tolerance ranges** (lower bound Q1, optimum Q2, upper bound Q3) for each pMAG against each environmental variable was done using the robust optimum (RO) method, following the protocol from [Chaffron et al. (2021)](https://doi.org/10.1126/sciadv.abg1921).

## Usage

To replicate the analysis:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mterzin/fishy_microbes.git
    cd fishy_microbes
    ```

2.  **Install Required R Packages:**
    Ensure the following R packages are installed:
    - `tidyverse`
    - `mixOmics`
    - `glmmTMB`
    - `DHARMa`
    - `randomForest`
    - `microbiome`

    A full list of dependencies and versions is available in `sessionInfo.txt`.

3.  **Obtain Data:**
    Download the processed data from Zenodo ([DOI: XXXXXXXX](https://doi.org/XXXXXXX)) and place it in the `data/processed/` directory. *Note: Raw data must be sourced from the links provided in the Data Availability section above.*

4.  **Run Scripts:**
    Execute the R scripts in the `scripts/` directory in numerical order.

## Dependencies

The code was run under R version 4.3.2. See `sessionInfo.txt` for a complete list of package versions.

## Citation

If you use this code or the associated data, please cite our publication:

> *Citation to be added upon publication.*

## Acknowledgements

- Seawater sampling and initial metagenomic processing were conducted by the Australian Institute of Marine Science (AIMS) Long-Term Monitoring Program (LTMP).
- The microbial niche analysis was performed following the protocol from Chaffron et al. (2021); the specific code for this analysis is available from the authors of that study upon request.
- This work was supported by...

## Contact

For questions regarding this code and analysis, please open an issue on GitHub or contact:
- Your Name: [your.email@domain.com]
- Marko Terzin: [marko.terzin@domain.com]
