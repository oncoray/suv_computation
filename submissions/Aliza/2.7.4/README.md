# SUV Measurement Results: [Aliza Medical Imaging & DICOM Viewer 2.7.4](https://www.aliza-dicom-viewer.com)

## Overview
Aliza uses the exact implementation of the [SUV_vendorneutral_pseudocode_20180626_DAC](https://qibawiki.rsna.org/images/8/86/SUV_vendorneutral_pseudocode_20180626_DAC.pdf) from https://qibawiki.rsna.org/index.php/Standardized_Uptake_Value_(SUV). The file is also available in this directory.
`oncoray/suv_computation` revision is [e48a3af](https://github.com/oncoray/suv_computation/commit/e48a3afe875f8bd5fc796d5b4efbe85fb8a1a859)

## Process
Used [Aliza Medical Imaging & DICOM Viewer](https://www.aliza-dicom-viewer.com/download/download_aliza). Please note that PET SUV calculation is not available in the open-source version `Aliza MS`. Drag-and-drop the directory `DRO`, double click at a PET image (or corresponding RT file) in the "DICOM Scanner" tab to load it, use "Filter" -> "PET" -> "Standardized Uptake Value" and click "Apply" button. To view values under cursor hold middle mouse button or activate "Show value under cursor" in the 2D view panel (cursor icon). Validate SUVmin, SUVmed and SUVmax. SUVmax is also visible as image maximum value in the image properties.


## Results summary
10 out of 17 DROs produce correct SUVbw values. Rounding to two decimal places is permitted; see the file `DRO_Aliza.csv` for exact results.

| DRO | Status | Notes | Application Message |
|-----|--------|-------|---------------------|
| DRO_0_0 | PASS | default |  |
| DRO_1_0 | PASS | rescaleslope |  |
| DRO_2_0 | PASS | Units = GML (corresponding to SUVbw) | SUV calculation is not required, units are GML (g/ml), scale factor 1. |
| DRO_2_1 | FAIL | Units = GML with PatientSex = “M” (male) corresponding to SUVlbmjames128 | SUV calculation is not required, units are GML (g/ml), scale factor 1. |
| DRO_2_2 | PASS | Units = GML with PatientSex = “O” (other) corresponding to SUV IBW | SUV calculation is not required, units are GML (g/ml), scale factor 1. |
| DRO_2_3 | FAIL | Units = CM2ML corresponding to SUVbsa | Can not process units "CM2ML". |
| DRO_2_4 | FAIL | Units = CNTS using Philips SUV scale factor | Can not process, units are CNTS, but required Philips private tags were not found. |
| DRO_2_5 | FAIL | Units = CNTS using Philips activity scale factor | Can not process, units are CNTS, but required Philips private tags were not found. |
| DRO_3_0 | FAIL | dose in MBq |  |
| DRO_3_1 | FAIL | DC = ADMIN | Can not process - "Decay Correction" ADMIN is not compatible, required is "START". |
| DRO_3_2 | PASS | DC = START but SeriesTime after AcquisitionTime | "Series Time" is after "Acquisition Time", tried to workaround using "Frame Reference Time" and "Frame Duration". |
| DRO_3_3 | PASS | GE private DC datetime |  |
| DRO_3_4 | FAIL | DC = NONE + multiple values ACQ TIME | Can not process - "Corrected Image" is not compatible. |
| DRO_4_0 | PASS | only radiopharmaceutical datetime, no RP Date and RP time |  |
| DRO_4_1 | PASS | only radiopharmaceutical time, no RP datetime |  |
| DRO_4_2 | FAIL | Sparing midnight | Can not process - "Radiopharmaceutical Start Date Time" is after scan time. |
| DRO_5_0 | PASS | Radionuclide Ga68 |  |


## Files

- `DRO_Aliza.csv` — measurement results
- `README.md` — this file

## Contact
	
s.  [Aliza Medical Imaging & DICOM Viewer](https://www.aliza-dicom-viewer.com/info)
