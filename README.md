# Standardizing SUV Computation (IBSI-SUV)

Our goal is to standardize how DICOM PET images are converted to standardized uptake values (SUVs) – an essential step in PET image analysis. 
For that, we are developing a set of [digital reference objects (DROs)](https://github.com/oncoray/suv_computation/blob/main/DRO) together with a [manual](https://oncoray.github.io/suv_computation/suv.html) including usage instructions.

## Changelog

#### [v2.0.0] - 2026-04-10
DROs
- Several DROs now include multiple versions for different values of Patient Sex or Manufacturer (where relevant).
- A new DRO (3_5_x) has been added.
- The file structure has been revised: each DRO now represents a single patient.
- Multiple DICOM attributes have been modified to improve compatibility and realism, which may affect previous results.
- Manufacturer is specified where required for SUV conversion.

Manual
- Recommendations have been refined and updated, particularly for scan start determination when Decay Correction = START.
- An SUV computation flowchart has been added to facilitate implementation.

#### [v1.1.1] - 2026-03-16
A new version of the RTStruct files was released with improved compatibility. The region of interest is called `DRO_mask`.
Additionally, the contour now covers the whole volume of the reference object.

#### [v1.1.0] - 2026-02-04
RTStruct files (DICOM radiotherapy structure sets) were added for each DRO as an alternative for NIfTI masks. 
Furthermore, the file structure was changed. From now on, each DRO is one series of the same study.

#### [v1.0.0] - 2026-01-28
We are happy to introduce the first version of our manual for standardized uptake value (SUV) computation as well as the digital reference objects (DROs) for SUV conversion verification. The final versions will be released in subsequent updates.

## Getting the Data

You can clone the whole repository via HTTPS:
```bash
git clone https://github.com/oncoray/suv_computation.git
```
or via ssh: 
```bash
git clone git@github.com:oncoray/suv_computation.git
```
The DRO DICOM directory includes a mask subdirectory with a NIfTI mask for feature extraction. More details on their use can be found in the [manual](https://oncoray.github.io/suv_computation/suv.html).

## Feedback and Support

Please report issues or provide feedback by contacting:
- [Michael Vácha](mailto:m.vacha@hzdr.de)
- [Alex Zwanenburg](mailto:alexander.zwanenburg@nct-dresden.de)

We welcome feedback on:
- Extracted SUV values
- Technical issues with reading files or SUV computation
- Suggestions for future versions

## License

The manual and the digital reference objects (DROs) are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**© 2026 Michael Vácha & Alex Zwanenburg & The image biomarker standardisation initiative (IBSI)**

