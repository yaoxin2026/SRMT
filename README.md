# SRMT: Subcell-Refined Marching Tetrahedra

SRMT extracts isosurfaces from a three-dimensional scalar array. Each selected parent cell is divided into eight subcells and 48 tetrahedra. Added nodal values come from trilinear interpolation of the original samples; refinement introduces no additional physical samples. The implementation supports serial execution and multiprocessing with exact-key assembly across spatial partitions.

This repository contains the Python API, a standalone example, comparisons with marching cubes (MC) and marching tetrahedra (MT), and manuscript figure scripts. The API also provides two-dimensional isoline extraction.

Repository: <https://github.com/yaoxin2026/SRMT>

## Contents

| Path | Purpose |
| --- | --- |
| `srmt_example/LYpy_SRMT.py` | Standalone SRMT API. |
| `srmt_example/test_isosurface_two_gaussians_srmt.py` | Runnable two-Gaussian example; its historical filename does not denote a unit-test module. |
| `srmt_benchmark/` | Benchmark driver, a matching standalone API copy, plotting utilities, and Figures 01-09. |
| `srmt_benchmark/data_mc_mt_srmt/` | Supplied benchmark measurements, summaries, reference mesh, and cached figure meshes. |
| `srmt_benchmark/data_mc_mt_srmt.md` | Supplied benchmark console log. |
| `data/README.md` | Required external solar observations and geometry files; these data are **not included**. |
| `fig/` | Default destination for generated figures. |
| `tests/` | Automated API and repository portability checks. |
| `docs/PUBLISHING.md` | Instructions for adding this prepared tree to the existing GitHub repository. |
| `docs/PREPARATION.md` | Changes and validation performed during repository preparation. |

The two `LYpy_SRMT.py` copies are intentionally identical so either directory can be copied and run independently. An automated check detects divergence. Scientific changes must be applied to both copies.

## Installation

Use Python **3.10 or later**. The code uses Python 3.10 type syntax. See [docs/PREPARATION.md](docs/PREPARATION.md) for the environment actually tested.

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\Activate.ps1` in PowerShell. Use `python` in place of `python3` if that is the name of your Python installation.

| Workload | Install command |
| --- | --- |
| API and two-Gaussian example | `python -m pip install -r requirements.txt` |
| Analytic benchmarks and Figures 01-07 | `python -m pip install -r requirements-benchmark.txt` |
| Solar Figures 08-09 | `python -m pip install -r requirements-solar.txt` |

`multiprocessing` is part of Python. LaTeX is optional. This is a collection of directly runnable scripts, not a published PyPI package. Place `LYpy_SRMT.py` beside a script that imports it, as in the supplied example.

The dependency files let pip select compatible versions; they are not lockfiles. The exact environment recorded with the supplied measurements is in [environment.json](srmt_benchmark/data_mc_mt_srmt/environment.json). Its package versions and producer paths describe that historical run, not your local installation.

## Quick start

Run a small example from the repository root:

```bash
python srmt_example/test_isosurface_two_gaussians_srmt.py --resolution 32 --level 0.5 --processes 1 --output-dir outputs/example
```

The example writes an indexed mesh (`.npz`), metadata (`.json`), and a PNG preview. Add `--no-plot` to omit the preview. Select `--mode uniform` for the uniformly translated tetrahedral construction, or `--processes 4` for multiprocessing. The default mode is `default`, with corner-to-center subcell diagonals.

To use the API in your own script:

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

Volume axes are `(x, y, z)` in the supplied examples. `spacing` and `origin` follow array-axis order. `vertices` has shape `(Nv, 3)`, and `faces` has shape `(Nf, 3)` with integer vertex indices. Keep the `if __name__ == "__main__":` guard when using multiprocessing. The general API supports the start methods available on the platform; the publication benchmark specifically uses `fork`.

See the API docstrings for tolerances, orientation, optional facelets, diagnostics, and two-dimensional contours. Edge-incidence diagnostics alone do not certify vertex manifoldness or absence of self-intersections.

## Benchmark calculations

The supplied data contain **1,200 raw repeat records and 240 aggregate configurations**: three fields, eight grid resolutions, MC and MT, and two SRMT modes at four process counts. The benchmark uses level 0.5 and the median of five independent measurements. Geometry diagnostics are calculated on repeat 1 after performance measurement. These supplied results are preserved; repository preparation does not replace them with new timings.

For a small execution check on a platform supporting `fork`:

```bash
python srmt_benchmark/data_mc_mt_srmt.py --cases spheroid --methods MC MT SRMT --resolutions 64 --srmt-modes default --srmt-processes 1 --performance-only --no-plots --stop-on-error --output-dir outputs/benchmark-smoke
```

For a fresh full run:

```bash
python srmt_benchmark/data_mc_mt_srmt.py --full-diagnostics --no-plots --output-dir outputs/benchmark-new
```

The full run includes grids up to `512^3`. Explicit MT creates about 801 million tetrahedra at that resolution, so it requires substantial memory. Use a suitable workstation or select a smaller subset with `--resolutions`. The full publication benchmark requires `fork`; Windows users can run it under a suitable Linux environment such as WSL, while the standalone API and example support native Windows multiprocessing.

Use a separate output directory for new measurements. The default points to the supplied `srmt_benchmark/data_mc_mt_srmt/` tree and can reuse its records or rewrite its summaries. `--overwrite` deliberately reruns compatible cached configurations.

## Figures

After installing `requirements-benchmark.txt`, Figures 01-07 can use the included data without rerunning the full benchmark:

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

Figures 03 and 04 use the supplied cached meshes and may regenerate missing or incompatible meshes. The plot scripts select the default SRMT construction unless their `SRMT_MODE` setting is edited. Outputs go to `fig/` by default at the original 1000 dpi. For a quicker preview, set `SRMT_FIGURE_DPI=150` in the environment. Set `SRMT_USE_TEX=1` only when the external LaTeX rendering dependencies are installed; the default uses Matplotlib's built-in text rendering.

Figures 08 and 09 additionally require the observations and saved NLFFF geometry listed in [data/README.md](data/README.md). Those inputs and the separate geometry-generation workflow are not included. Installing solar dependencies alone is insufficient to reproduce these two figures.

## Paths

| Setting | Default | Use |
| --- | --- | --- |
| `MC_MT_SRMT_OUTPUT_DIR` | `srmt_benchmark/data_mc_mt_srmt/` beside the benchmark script | Benchmark output and figure input; benchmark `--output-dir` overrides it. |
| `SRMT_WORKSPACE_DIR` | Repository root inferred from the script location | Base directory for the default `data/` and `fig/` paths. |
| `SRMT_DATA_DIR` | `<workspace>/data/` | External solar inputs. |
| `SRMT_FIGURE_DIR` | `<workspace>/fig/` | Generated manuscript figures. |
| Example `--output-dir` | A directory beside the example script | Example mesh, metadata, and preview. |
| Figure 07 `--output-dir` | `SRMT_FIGURE_DIR` or default `fig/` | Override for that figure only. |

Defaults are independent of the launch directory. Explicit relative overrides are relative to the current working directory; `~` is expanded. Input data directories are not created merely by importing the plotting utilities. New runs under `outputs/` and generated figures are excluded from Git by default; the supplied benchmark records and meshes remain tracked.

To plot a new benchmark run on Linux or macOS:

```bash
export MC_MT_SRMT_OUTPUT_DIR="$PWD/outputs/benchmark-new"
python srmt_benchmark/Figure05_benchmark_performance.py
```

## Validation and citation

```bash
python -m unittest discover -s tests -v
```

The GitHub Actions workflow runs small API tests and an example on multiple Python/platform combinations, plus an analytic benchmark and plotting check on Linux. It does not rerun the full publication benchmark or solar-data figures.

Please cite the repository and the exact commit or release used in your work; [CITATION.cff](CITATION.cff) supplies software citation metadata. Add the final manuscript citation and DOI when available. The [MIT license](LICENSE) is preserved from the existing GitHub repository. External solar observations retain their providers' terms.
