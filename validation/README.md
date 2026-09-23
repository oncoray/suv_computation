This folder contains real-world data for SUV computation validation, that were released under CC BY 3.0 (see [license.txt](license.txt)) through The Cancer Imaging Archive (see attribution file within each patient directory).

Instructions:
- Each patient directory contains a DICOM PET series (PT) and a NIfTI binary mask (mask).
- Each binary mask contains a single spherical ROI, typically located in the liver; in one case, the ROI is located in a muscle.
- Normalize the intensities to body-weight-adjusted standardized uptake value (SUVbw).
- Do not apply any other preprocessing steps (such as resampling or interpolation).
- For each patient, report the maximum and mean value within the ROI (SUVmax and SUVmean) with a precision of at least three decimal places.
- Submit the results, including patient names or patient directory names and the software name and version, as a CSV table by email. You may use the template [validation_results_softwarename_version.csv](validation_results_softwarename_version.csv).