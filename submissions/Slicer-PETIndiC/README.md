# SUV Measurement Results: 3D Slicer PET-IndiC

## Overview

SUV min, median, and max were measured for all 17 DRO phantoms using [3D Slicer](https://www.slicer.org)'s [PET-IndiC](https://github.com/QIICR/PET-IndiC) extension (QuantitativeIndicesTool) with [PETDICOMExtension](https://github.com/QIICR/Slicer-PETDICOMExtension) for SUVbw volume loading and [SlicerRT](http://slicerrt.github.io/) for RTSTRUCT segmentation import.

## How this report was generated

This report was generated interactively using [Claude Code](https://claude.com/claude-code) (Claude Opus 4.6) connected to a running 3D Slicer instance via the [slicer-skill](https://github.com/pieper/slicer-skill) MCP (Model Context Protocol) server. Claude Code executed Python commands inside Slicer to load DICOM data, run the quantitative analysis, and collect results. During this process, a bug in the PETDICOMExtension was identified and fixed (see below).

The resulting `measure_suv.py` script captures the complete analysis pipeline and can be run independently in Slicer to reproduce the results.

## Process

1. All DRO PT and RTSTRUCT DICOM series were imported into the Slicer DICOM database.
2. For each DRO:
   - The PT series was loaded via the `DICOMPETSUVPlugin`, which uses `SUVFactorCalculator` CLI to generate Real World Value Mapping (RWVM) objects and applies the SUVbw conversion factor.
   - The RTSTRUCT was loaded via SlicerRT's DICOM plugin, producing a segmentation node.
   - `QuantitativeIndicesToolLogic.runOnSegment()` was called with `minimum`, `maximum`, and `median` enabled. This internally exports the segment to a label map and runs the `QuantitativeIndicesCLI` C++ module.
   - Results were extracted from the CLI node's output parameter group.
3. Results were collected into `DRO_Slicer_PETIndiC.csv`.

See `measure_suv.py` for the complete script.

## Tool versions

| Component | Version | Details |
|-----------|---------|---------|
| 3D Slicer | 5.11.0-2026-03-09 | Revision `d3726f0`, macOS amd64 |
| Python | 3.12.10 | Slicer built-in |
| VTK | 9.5.2 | |
| Qt | 5.15.18 | |
| PET-IndiC | `31e5cf0` | [QIICR/PET-IndiC](https://github.com/QIICR/PET-IndiC) |
| PETDICOMExtension | `4fa3cdf` | [QIICR/Slicer-PETDICOMExtension](https://github.com/QIICR/Slicer-PETDICOMExtension), includes vtkImageCast fix (see below) |
| SlicerRT | installed via Extension Manager | [SlicerRT](http://slicerrt.github.io/) |
| DRO repository | `afec925` | [oncoray/suv_computation](https://github.com/oncoray/suv_computation) at time of report generation |

## Bug fix: integer truncation in SUV conversion

During testing, a bug was identified in `DICOMRWVMPlugin.loadPetSeries()` where `vtkImageMathematics.MultiplyByK` preserves the input scalar type. Since PET DICOM pixel data is typically stored as `int16`, multiplying by a small RWVM slope (e.g., 0.000278) truncated fractional SUV values to zero (e.g., 0.2 SUV became 0).

The fix adds `vtkImageCast` to convert the volume to `float` before applying the multiplication. This fix has been submitted upstream: [QIICR/Slicer-PETDICOMExtension#27](https://github.com/QIICR/Slicer-PETDICOMExtension/pull/27).

## Results summary

5 out of 17 DROs produce correct SUVbw values matching expectations (min=0.20, median=1.00, max=4.00):

| DRO | Status | Notes |
|-----|--------|-------|
| DRO_0_0 | PASS | default (BQML, DC=START) |
| DRO_1_0 | PASS | multiple Rescale Slope values |
| DRO_3_3 | PASS | GE private DC datetime |
| DRO_4_1 | PASS | RP time only |
| DRO_5_0 | PASS | Ga68 radionuclide |

The remaining 12 DROs produce incorrect values, indicating that the PETDICOMExtension SUV factor calculation does not yet handle all DICOM encoding variations tested by the DROs (GML/CM2ML/CNTS units, Philips private tags, dose in MBq, various decay correction modes, and radiopharmaceutical time edge cases).

## Files

- `DRO_Slicer_PETIndiC.csv` — measurement results
- `measure_suv.py` — Python script to reproduce the analysis in Slicer
- `README.md` — this file

## Contact

Andrey Fedorov ([@fedorov](https://github.com/fedorov)), Brigham and Women's Hospital, Boston, USA
