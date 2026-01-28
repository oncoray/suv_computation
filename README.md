# Standardizing SUV Computation

## Project Aims

Our goal is to standardize how DICOM PET images are converted to SUVs – an essential step in PET image analysis. 

## Current Status

We are happy to introduce the first version of our manual for standardized uptake value (SUV) computation as well as the digital reference objects (DROs) for SUV conversion verification. 

You can clone the whole repository via https:

```bash
git clone https://github.com/oncoray/suv_computation.git
```
or via ssh: 

```bash
git clone git@github.com:oncoray/suv_computation.git
```

You may as well inspect the files separately:

- [Manual - online version](https://oncoray.github.io/suv_computation/suv.html)

- [Manual - .docx version](https://github.com/oncoray/suv_computation/blob/main/docs/suv.docx)

- [DRO dicom directory](https://github.com/oncoray/suv_computation/blob/main/DRO)

The DRO dicom directory includes a mask subdirectory with a nifti mask for feature extraction. More details on their use can be found in the manual.

The manual and the digital reference objects (DROs) are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The final versions will be released in subsequent updates.

© 2026 Michael Vácha

