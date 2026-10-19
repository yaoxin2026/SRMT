# SRMT: Subcell-Refined Marching Tetrahedra

SRMT extracts isosurfaces from scalar nodal values on fixed-resolution structured grids. Each active parent cell is divided into eight subcells and 48 tetrahedra, with additional nodal values obtained by trilinear interpolation. This provides finer surface triangulations without introducing new physical samples. The implementation supports serial execution and multiprocessing, using integer node and edge identifiers to assemble shared surface vertices.

This repository contains the SRMT Python implementation, a standalone example, analytic benchmark results, and scripts for analysis and reproduction of the manuscript figures. The rendered figures are also included. The repository accompanies the manuscript "*Subcell-refined marching tetrahedra for isosurface extraction from fixed-resolution structured grids: application to electron-cyclotron-frequency surfaces in solar coronal magnetic fields*."

## Repository structure

| Path | Contents |
| --- | --- |
| `data/` | Placeholder for solar observations and reconstructed coronal magnetic-field data downloaded from Zenodo. |
| `fig/` | Rendered manuscript figures and the default output directory for figure scripts. |
| `README.md` | Installation and usage instructions. |
| `srmt_benchmark/` | Benchmark results, analysis and figure scripts, and a copy of the SRMT implementation. |
| `srmt_example/` | The SRMT implementation and a standalone example. |

The SRMT implementation is provided in `LYpy_SRMT.py`. The copies in `srmt_benchmark/` and `srmt_example/` are identical; keep them synchronized when modifying the implementation.

The figures in `fig/` can be viewed directly without installing dependencies or downloading the solar data.

## Data sources

1. **Solar observations and reconstructed coronal magnetic fields.** These data are available from [Zenodo, DOI: 10.5281/zenodo.23466388](https://doi.org/10.5281/zenodo.23466388). The archive `data.zip` contains the associated SDO/HMI observations, SDO/AIA 171 Å observations, and reconstructed coronal magnetic-field data.

   **Before reproducing Figures 08 and 09, download `data.zip` and extract its contents into `data/` at the repository root.** Preserve the archive's directory structure and ensure that the resulting paths contain only one `data/` level. This directory is beside `README.md`, `srmt_example/`, and `srmt_benchmark/`.

2. **Analytic benchmark results.** The results in `srmt_benchmark/data_mc_mt_srmt/` are included in the repository and support figure reproduction. See [Benchmark calculations](#benchmark-calculations) for instructions on running the benchmarks.

The standalone example and Figures 01–07 use synthetic fields or the included benchmark results and do not require the Zenodo solar data.

## Installation

The supplied benchmark environment records Python 3.13.5. The scripts use Python 3.10 or later syntax; use a Python version supported by the packages you install.

Clone the repository:

```bash
git clone https://github.com/yaoxin2026/SRMT.git
cd SRMT
```

If you already have a local copy, open the directory containing `README.md`. **Run all subsequent commands from this repository root.**

Use an existing compatible Python environment or create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Install the dependencies for your workflow:

| Workflow | Install command |
| --- | --- |
| API and standalone example | `python -m pip install numpy scipy matplotlib` |
| Analytic benchmarks and Figures 01–07 | `python -m pip install numpy scipy matplotlib h5py scikit-image pyvista vtk psutil` |
| Analytic benchmarks and all manuscript figures, including Figures 08–09 | `python -m pip install numpy scipy matplotlib h5py scikit-image pyvista vtk psutil astropy sunpy` |

`multiprocessing` is included in Python and does not require a separate installation. The scripts run directly from this repository; no package installation of SRMT is required. For the package versions recorded with the supplied benchmark results, see [environment.json](srmt_benchmark/data_mc_mt_srmt/environment.json).

## Run the standalone example

The example uses the SRMT API in `LYpy_SRMT.py`. From the repository root, run:

```bash
cd srmt_example 
python test_isosurface_two_gaussians_srmt.py
```

## Benchmark calculations

The repository includes results for a spheroid, a torus, and a two-Gaussian field: 1,200 individual runs and 240 aggregate configurations, covering eight original-grid resolutions, marching cubes (MC), marching tetrahedra (MT), and two SRMT constructions at four process counts. Each configuration uses five independent repeats; performance summaries report their median, and geometric diagnostics are evaluated on the first repeat.

To run the benchmarks, execute the following command from the repository root:

```bash
cd srmt_benchmark
python data_mc_mt_srmt.py
```

Run the benchmark calculations before analysis and plotting when generating new results. The results supplied with the repository can be used directly for figure reproduction.

## Reproduce the manuscript figures

The following commands regenerate the supplied PNG files. By default, they write to `fig/` and replace images with matching filenames. Prepare the Zenodo data before running the scripts for Figures 08 and 09.

Run these commands from the repository root:

```bash
cd srmt_benchmark
python Figure01_SRMT_illustration_z0.py
python Figure01_SRMT_illustration_z1.py
python Figure02_tetrahedron_intersection.py
python Figure03_benchmark_full.py
python Figure04_benchmark_local.py
python Figure05_benchmark_performance.py
python Figure06_benchmark_accuracy.py
python Figure07_benchmark_geometry.py
python Figure08_fields_geometry_aia.py
python Figure09_fields_geometry_aia.py
```

## Citation and data acknowledgement

When using SRMT, cite the accompanying manuscript when available and identify the repository release or commit used. When using the deposited solar data, also cite the dataset:

**Zenodo DOI: [10.5281/zenodo.23466388](https://doi.org/10.5281/zenodo.23466388).**

The original HMI and AIA observations are available through the [Joint Science Operations Center](https://jsoc.stanford.edu/). The reconstructed coronal magnetic fields are model-derived data. The source code is distributed under the MIT license. Consult the Zenodo record for dataset licensing information and retain the original attribution and applicable notices for the SDO observations.

SDO acknowledgement: “Courtesy of NASA/SDO and the AIA, EVE, and HMI science teams.”
