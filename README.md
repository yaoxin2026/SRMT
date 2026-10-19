# SRMT: Subcell-Refined Marching Tetrahedra

SRMT extracts isosurfaces from scalar nodal values on fixed-resolution structured grids. Each active parent cell is divided into eight subcells and 48 tetrahedra, with additional nodal values obtained by trilinear interpolation. This provides finer surface triangulations without introducing new physical samples. The implementation supports serial execution and multiprocessing, using integer node and edge identifiers to assemble shared surface vertices.

This repository contains the SRMT Python implementation, a standalone example, analytic benchmark results, and scripts for analysis and reproduction of the manuscript figures. The rendered figures are also included. The repository accompanies the manuscript *Subcell-refined marching tetrahedra for isosurface extraction from fixed-resolution structured grids: application to electron-cyclotron-frequency surfaces in solar coronal magnetic fields*.



- **SDO observations and reconstructed coronal magnetic-field data:** [Zenodo, DOI: 10.5281/zenodo.23466388](https://doi.org/10.5281/zenodo.23466388)

**Before reproducing the coronal figures (Figures 08 and 09), download `data.zip` from Zenodo and extract the data into `data/` at the repository root.** This is the directory beside `README.md`, `srmt_example/`, and `srmt_benchmark/`. The standalone example and analytic figures (Figures 01–07) use synthetic fields or the included benchmark results and do not require the Zenodo solar data.

The rendered figures are already included in `fig/` and can be viewed directly without installing dependencies or downloading the solar data.

## Repository contents

| Path | Contents |
| --- | --- |
| `README.md` | Installation, data preparation, usage, and figure-reproduction instructions. |
| `.gitignore` | Excludes downloaded solar data, Python caches, local environments, and newly generated outputs from version control. |
| `srmt_example/LYpy_SRMT.py` | Standalone SRMT API, including three-dimensional isosurface and two-dimensional isoline extraction. |
| `srmt_example/test_isosurface_two_gaussians_srmt.py` | Runnable two-Gaussian isosurface example. |
| `srmt_benchmark/LYpy_SRMT.py` | Matching API copy used by the benchmark scripts. |
| `srmt_benchmark/data_mc_mt_srmt.py` | Analytic benchmark driver for marching cubes (MC), marching tetrahedra (MT), and SRMT. |
| `srmt_benchmark/data_mc_mt_srmt/` | Included benchmark measurements, summaries, reference mesh, and cached meshes for figure reproduction. |
| `srmt_benchmark/data_mc_mt_srmt.md` | Recorded benchmark console output. |
| `srmt_benchmark/Import_CWD.py` | Shared plotting, path, and data-loading utilities. |
| `srmt_benchmark/Figure*.py` | Manuscript figure scripts. |
| `data/` | Destination for the solar data downloaded from Zenodo; only the empty `.gitkeep` placeholder is tracked in Git. |
| `fig/` | Ten supplied PNG files for Figures 01–09, including two Figure 01 illustrations; also the default output directory for regenerated figures. |

The solar data under the root-level `data/` directory are distributed through Zenodo. The analytic benchmark results under `srmt_benchmark/data_mc_mt_srmt/` are included in the repository and support figure reproduction. The `.gitkeep` placeholder preserves the otherwise empty `data/` directory when the repository is cloned.

The two copies of `LYpy_SRMT.py` are identical. Keep them synchronized when modifying the implementation. Python creates `__pycache__/` directories automatically; these caches are excluded from version control.

### Included figures and source scripts

| Figure | Script in `srmt_benchmark/` | Image in `fig/` |
| --- | --- | --- |
| 01 (z0) | [Figure01_SRMT_illustration_z0.py](srmt_benchmark/Figure01_SRMT_illustration_z0.py) | [PNG](fig/Figure01_SRMT_illustration_z0.png) |
| 01 (z1) | [Figure01_SRMT_illustration_z1.py](srmt_benchmark/Figure01_SRMT_illustration_z1.py) | [PNG](fig/Figure01_SRMT_illustration_z1.png) |
| 02 | [Figure02_tetrahedron_intersection.py](srmt_benchmark/Figure02_tetrahedron_intersection.py) | [PNG](fig/Figure02_tetrahedron_intersection.png) |
| 03 | [Figure03_benchmark_full.py](srmt_benchmark/Figure03_benchmark_full.py) | [PNG](fig/Figure03_benchmark_full.png) |
| 04 | [Figure04_benchmark_local.py](srmt_benchmark/Figure04_benchmark_local.py) | [PNG](fig/Figure04_benchmark_local.png) |
| 05 | [Figure05_benchmark_performance.py](srmt_benchmark/Figure05_benchmark_performance.py) | [PNG](fig/Figure05_benchmark_performance.png) |
| 06 | [Figure06_benchmark_accuracy.py](srmt_benchmark/Figure06_benchmark_accuracy.py) | [PNG](fig/Figure06_benchmark_accuracy.png) |
| 07 | [Figure07_benchmark_geometry.py](srmt_benchmark/Figure07_benchmark_geometry.py) | [PNG](fig/Figure07_benchmark_geometry.png) |
| 08 | [Figure08_fields_geometry_aia.py](srmt_benchmark/Figure08_fields_geometry_aia.py) | [PNG](fig/Figure08_fields_geometry_aia.png) |
| 09 | [Figure09_fields_geometry_aia.py](srmt_benchmark/Figure09_fields_geometry_aia.py) | [PNG](fig/Figure09_fields_geometry_aia.png) |

## Installation

The supplied benchmark environment records Python 3.13.5. The scripts use Python 3.10 or later syntax; use a Python version supported by the packages you install.

Clone the repository:

```bash
git clone https://github.com/yaoxin2026/SRMT.git
cd SRMT
```

If you already have a local copy, open its root directory, which contains `README.md`. Run the commands below from that directory. You can use an existing compatible Python environment or create a new one:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

On Windows, use `python` if `python3` is unavailable and activate the environment with `.venv\Scripts\Activate.ps1` in PowerShell.

Install dependencies for the required workflow:

| Workflow | Install command |
| --- | --- |
| API and standalone example | `python -m pip install numpy scipy matplotlib` |
| Analytic benchmarks and Figures 01–07 | `python -m pip install numpy scipy matplotlib h5py scikit-image pyvista vtk psutil` |
| All manuscript figures, including Figures 08–09 | `python -m pip install numpy scipy matplotlib h5py scikit-image pyvista vtk psutil astropy sunpy` |

`multiprocessing` is included in Python and does not require a separate installation. The scripts run directly from this repository; no package installation of SRMT is required. These commands install packages compatible with your Python environment. For the versions recorded with the supplied benchmark results, see [environment.json](srmt_benchmark/data_mc_mt_srmt/environment.json).

## Download and arrange the solar data

Download `data.zip` from **[https://doi.org/10.5281/zenodo.23466388](https://doi.org/10.5281/zenodo.23466388)**. The archive contains the associated SDO/HMI and SDO/AIA 171 Å observations and reconstructed coronal magnetic-field data.

Extract the archive while preserving its filenames and directory structure. Place the extracted data under `<repository-root>/data/`, creating the directory if necessary, so the scripts can find `data/sdo_aia/`, `data/sdo_hmi/`, and the saved geometry in `data/nlfff_visualization/`. Here, `data/` means the directory inside the repository, not an absolute `/data` directory on your system.

If the archive already contains a top-level `data/` directory, place that directory beside `README.md`. If it contains the data subdirectories directly, extract them into the repository's `data/` directory. The resulting paths should contain a single `data/` level, for example `data/sdo_aia/20260418/`.

The `.gitkeep` file may remain in place after extraction. The repository's `.gitignore` excludes the downloaded solar data from subsequent Git commits.

### Observation files

The default figure scripts expect these files relative to the repository root:

```text
data/sdo_aia/20260418/aia.lev1_euv_12s.2026-04-18T051210Z.171.image_lev1.fits
data/sdo_hmi/20260418/hmi.sharp_cea_720s.14594.20260418_051200_TAI.Br.fits
data/sdo_aia/20260629/aia.lev1_euv_12s.2026-06-29T012410Z.171.image_lev1.fits
data/sdo_hmi/20260629/hmi.sharp_cea_720s.14829.20260629_012400_TAI.Br.fits
```

Figure 08 uses HARP 14594, and Figure 09 uses HARP 14829. Preserve the timestamps and time-standard labels in the original filenames.

### Saved coronal geometry

Figures 08 and 09 load previously computed field lines and SRMT isosurface meshes from the following case directories:

```text
data/nlfff_visualization/nlfff_vis_20260418_051200/
data/nlfff_visualization/nlfff_vis_20260629_012400/
```

Each case requires these geometry files:

| Geometry | Preferred filename | Automatically selected CEA fallback |
| --- | --- | --- |
| Field lines | `data_fieldlines_helioprojective.h5` | `data_fieldlines_cea.h5` |
| SRMT isosurfaces | `data_isosurfaces_helioprojective_srmt.h5` | `data_isosurfaces_cea_srmt.h5` |

The default `NLFFF_SAVE_MODE` is `"h5"`. For matching NPZ files, set `NLFFF_SAVE_MODE = "npz"` near the beginning of the corresponding figure script. The scripts require SRMT meshes produced with `mode="default"` and their saved diagnostic metadata. They accept CEA or helioprojective geometry and convert CEA footprints for display when necessary.

These figure scripts load saved geometry; they do not reconstruct the magnetic field or generate field lines and isosurfaces from a raw magnetic-field volume. If a geometry file is missing, obtain the corresponding saved product or generate it with the separate NLFFF processing workflow before plotting. The error message identifies the required paths. To use existing geometry elsewhere, adjust `NLFFF_VISUALIZATION_DIR`, `FIELDLINE_FILE`, or `ISOSURFACE_FILE` in the relevant script.

## Run the standalone example

Run commands from the repository root unless otherwise stated:

```bash
python srmt_example/test_isosurface_two_gaussians_srmt.py --resolution 32 --level 0.5 --processes 1 --output-dir outputs/example
```

The example writes an indexed surface mesh (`.npz`), metadata (`.json`), and a PNG preview. Use `--no-plot` to omit the preview, `--processes 4` to use four worker processes, or `--mode uniform` to select the uniform tetrahedral construction. The default mode is `default`, with corner-to-center subcell diagonals.

To use the API in another script, place `LYpy_SRMT.py` beside that script:

```python
import numpy
from LYpy_SRMT import subcell_refined_marching_tetrahedra

if __name__ == "__main__":
    x = numpy.linspace(-1.0, 1.0, 25)
    field = x[:, None, None]**2 + x[None, :, None]**2 + x[None, None, :]**2
    spacing = (float(x[1] - x[0]),) * 3
    vertices, faces, normals, values, diagnostics = subcell_refined_marching_tetrahedra(field, level=0.64, spacing=spacing, origin=(-1.0, -1.0, -1.0), n_jobs=1, return_diagnostics=True)
    print(vertices.shape, faces.shape, diagnostics["n_active_parent_cells"])
```

The examples use array axes `(x, y, z)`. The `spacing` and `origin` arguments follow array-axis order. Keep the `if __name__ == "__main__":` guard when using multiprocessing. See the API docstrings for the available arguments and diagnostics.

## Benchmark calculations

The repository includes results for a spheroid, a torus, and a two-Gaussian field: 1,200 raw repeats and 240 aggregate configurations, covering eight original-grid resolutions, MC, MT, and two SRMT constructions at four process counts. Each configuration uses five independent repeats; performance summaries report their median, and geometric diagnostics are evaluated on the first repeat.

**Run `data_mc_mt_srmt.py` before analysis and plotting when generating new benchmark results.** The included results can be used directly to reproduce the analytic figures, so rerunning the full benchmark is optional when using those results.

For a small benchmark run:

```bash
python srmt_benchmark/data_mc_mt_srmt.py --cases spheroid --methods MC MT SRMT --resolutions 64 --srmt-modes default --srmt-processes 1 --performance-only --no-plots --stop-on-error --output-dir outputs/benchmark-small
```

For the full benchmark with geometric diagnostics:

```bash
python srmt_benchmark/data_mc_mt_srmt.py --full-diagnostics --no-plots --output-dir outputs/benchmark-new
```

The full benchmark includes original grids up to `512^3` and can require substantial time and memory. At that resolution, full-volume MT constructs approximately 801 million tetrahedra. Select smaller cases with `--cases` and `--resolutions` when appropriate. A performance-only run does not provide the geometric diagnostics needed for Figures 06 and 07.

The benchmark driver fixes the multiprocessing start method to `fork`, so use an environment that supports it, such as Linux. The standalone API and example support the start methods available on the platform.

Keep new measurements in a separate output directory. Without `--output-dir`, the driver uses `srmt_benchmark/data_mc_mt_srmt/` or the directory selected by `MC_MT_SRMT_OUTPUT_DIR`; it can reuse existing records and rewrite summaries. Add `--overwrite` only when intentionally rerunning cached configurations.

## Reproduce the manuscript figures

The commands below regenerate the supplied PNG files. By default, they write to `fig/` and replace images with matching filenames. To save a separate set, first set the output directory from the repository root:

```bash
export SRMT_FIGURE_DIR="$PWD/fig_reproduced"
```

The scripts create this directory automatically. Use `unset SRMT_FIGURE_DIR` to restore the default `fig/` destination.

### Analytic figures: Figures 01–07

With the dependencies installed, run:

```bash
python srmt_benchmark/Figure01_SRMT_illustration_z0.py
python srmt_benchmark/Figure01_SRMT_illustration_z1.py
python srmt_benchmark/Figure02_tetrahedron_intersection.py
python srmt_benchmark/Figure03_benchmark_full.py
python srmt_benchmark/Figure04_benchmark_local.py
python srmt_benchmark/Figure05_benchmark_performance.py
python srmt_benchmark/Figure06_benchmark_accuracy.py
python srmt_benchmark/Figure07_benchmark_geometry.py
```

Figures 01 and 02 illustrate the method. Figures 03 and 04 use cached benchmark meshes and can regenerate missing or incompatible meshes. Figures 05–07 read the benchmark summaries. The default SRMT construction is selected by `SRMT_MODE = "default"` in the relevant scripts.

To plot results from a new full benchmark run, set the input directory before running Figures 03–07. For example, in a POSIX shell from the repository root:

```bash
export MC_MT_SRMT_OUTPUT_DIR="$PWD/outputs/benchmark-new"
python srmt_benchmark/Figure05_benchmark_performance.py
python srmt_benchmark/Figure06_benchmark_accuracy.py
python srmt_benchmark/Figure07_benchmark_geometry.py
```

Use `unset MC_MT_SRMT_OUTPUT_DIR` to return to the default input directory.

### Coronal figures: Figures 08 and 09

After downloading the [Zenodo data](https://doi.org/10.5281/zenodo.23466388) and arranging the observations and saved geometry under `data/` as described above, run:

```bash
python srmt_benchmark/Figure08_fields_geometry_aia.py
python srmt_benchmark/Figure09_fields_geometry_aia.py
```

These scripts combine AIA 171 Å images, HMI radial magnetic-field maps, reconstructed field lines, and SRMT magnetic-field-strength isosurfaces.

### Figure output

The default figure resolution is 1000 dpi. For a lower-resolution preview in a POSIX shell:

```bash
export SRMT_FIGURE_DPI=150
python srmt_benchmark/Figure01_SRMT_illustration_z0.py
```

Use `unset SRMT_FIGURE_DPI` to restore the default. The scripts use Matplotlib's built-in text rendering unless `SRMT_USE_TEX=1` is set; enable that option only when the external LaTeX rendering dependencies are installed.

## Data and output paths

| Setting | Default | Purpose |
| --- | --- | --- |
| `SRMT_WORKSPACE_DIR` | Repository root inferred from the script location | Base directory for the default `data/` and `fig/` paths. |
| `SRMT_DATA_DIR` | `<workspace>/data/` | Solar observations and coronal geometry downloaded from Zenodo. |
| `SRMT_FIGURE_DIR` | `<workspace>/fig/` | Destination for regenerated manuscript figures. |
| `MC_MT_SRMT_OUTPUT_DIR` | `srmt_benchmark/data_mc_mt_srmt/` | Benchmark output and input for the analytic figure scripts. |

The default paths are independent of the current working directory. Explicit relative overrides are resolved from the directory in which the command is run.

To keep the downloaded data elsewhere, set `SRMT_DATA_DIR` to the directory containing `sdo_aia/`, `sdo_hmi/`, and `nlfff_visualization/`. For example:

```bash
export SRMT_DATA_DIR="/path/to/data"
python srmt_benchmark/Figure08_fields_geometry_aia.py
```

In PowerShell, the corresponding syntax is `$env:SRMT_DATA_DIR = "C:\path\to\data"`.

## Citation and data acknowledgement

When using SRMT, cite the accompanying manuscript when available and identify the repository release or commit used. When using the deposited solar data, also cite the dataset:

**Zenodo DOI: [10.5281/zenodo.23466388](https://doi.org/10.5281/zenodo.23466388).**

The original HMI and AIA observations are available through the [Joint Science Operations Center](https://jsoc.stanford.edu/). The reconstructed coronal magnetic fields are model-derived data. The source code is distributed under the MIT license. Consult the Zenodo record for dataset licensing information and retain the original attribution and applicable notices for the SDO observations.

SDO acknowledgement: “Courtesy of NASA/SDO and the AIA, EVE, and HMI science teams.”
