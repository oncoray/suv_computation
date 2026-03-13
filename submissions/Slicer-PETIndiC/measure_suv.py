"""
Measure SUV min, median, and max for all DRO phantoms using 3D Slicer's
PET-IndiC QuantitativeIndicesTool.

Prerequisites:
  - 3D Slicer with PET-IndiC, PETDICOMExtension, and SlicerRT installed
  - All DRO PT and RTSTRUCT DICOM series imported into the Slicer DICOM database
  - PETDICOMExtension must include the vtkImageCast fix (see README)

Usage:
  Paste this script into the Slicer Python console, or run via:
    slicer.util.execPythonScript("measure_suv.py")

Output:
  Prints CSV-formatted results to the Slicer Python console.
  Also saves results to DRO_Slicer_PETIndiC.csv next to this script.
"""

import json
import os
import re

import vtk
import slicer
from DICOMLib import DICOMUtils
from QuantitativeIndicesTool import QuantitativeIndicesToolLogic

# --- Configuration -----------------------------------------------------------

# DRO metadata: (section, dro_id, description, expected_min, expected_med, expected_max)
DRO_LIST = [
    ("default",      "DRO_0_0", 'default DRO with Units = BQML and DC = START',                                "0.20", "1.00", "4.00"),
    ("rescaleslope", "DRO_1_0", 'multiple values Rescale Slope ',                                               "0.20", "1.00", "4.00"),
    ("units",        "DRO_2_0", 'Units = GML (corresponding to SUVbw)',                                         "0.20", "1.00", "4.00"),
    ("units",        "DRO_2_1", 'Units = GML with PatientSex = "M" (male) corresponding to SUVlbmjames128',    "0.20", "1.00", "4.00"),
    ("units",        "DRO_2_2", 'Units = GML with PatientSex = "O" (other) corresponding to SUV IBW',          "0.20", "1.00", "4.00"),
    ("units",        "DRO_2_3", 'Units = CM2ML corresponding to SUVbsa',                                        "0.20", "1.00", "4.00"),
    ("units",        "DRO_2_4", 'Units = CNTS using Philips SUV scale factor',                                  "0.20", "1.00", "4.00"),
    ("units",        "DRO_2_5", 'Units = CNTS using Philips activity scale factor',                             "0.20", "1.00", "4.00"),
    ("dose",         "DRO_3_0", 'dose in MBq',                                                                  "0.20", "1.00", "4.00"),
    ("dose",         "DRO_3_1", 'DC = ADMIN',                                                                   "0.20", "1.00", "4.00"),
    ("dose",         "DRO_3_2", 'DC = START but SeriesTime after AcquisitionTime',                              "0.20", "1.00", "4.00"),
    ("dose",         "DRO_3_3", 'GE private DC datetime',                                                       "0.20", "1.00", "4.00"),
    ("dose",         "DRO_3_4", 'DC = NONE + multiple values ACQ TIME ',                                        "0.20", "1.00", "4.00"),
    ("rptime",       "DRO_4_0", 'only radiopharmaceutical datetime, no RP Date and RP time',                    "0.20", "1.00", "4.00"),
    ("rptime",       "DRO_4_1", 'only radiopharmaceutical time, no RP datetime',                                "0.20", "1.00", "4.00"),
    ("rptime",       "DRO_4_2", 'Sparing midnight',                                                             "0.20", "1.00", "4.00"),
    ("halflife",     "DRO_5_0", 'Radionuclide Ga68',                                                            "0.20", "1.00", "4.00"),
]

# --- DICOM tag constants -----------------------------------------------------

TAG_MODALITY = "0008,0060"              # Modality
TAG_SERIES_DESCRIPTION = "0008,103e"    # Series Description

# --- Build series UID map from DICOM database --------------------------------

def build_dro_series_map():
    """Return dict: {dro_id: {"PT": series_uid, "RTSTRUCT": series_uid}}."""
    db = slicer.dicomDatabase
    dro_map = {}
    for patient in db.patients():
        for study in db.studiesForPatient(patient):
            for series in db.seriesForStudy(study):
                files = db.filesForSeries(series)
                if not files:
                    continue
                modality = db.fileValue(files[0], TAG_MODALITY)
                desc = db.fileValue(files[0], TAG_SERIES_DESCRIPTION)
                m = re.search(r"DRO_(\d+_\d+)", desc)
                if not m:
                    continue
                dro_id = "DRO_" + m.group(1)
                dro_map.setdefault(dro_id, {})[modality] = series
    return dro_map

# --- Process a single DRO ----------------------------------------------------

def process_dro(dro_id, pt_uid, rs_uid, logic):
    """Load PT and RTSTRUCT, run QuantitativeIndicesTool, return (min, med, max)."""
    slicer.mrmlScene.Clear(0)
    slicer.app.processEvents()

    # Load PT series via PET SUV plugin (produces SUVbw volume)
    pt_loaded = DICOMUtils.loadSeriesByUID([pt_uid])

    # Find the SUVbw volume by name
    suvbw_node = None
    for node_id in pt_loaded:
        node = slicer.mrmlScene.GetNodeByID(node_id)
        if node and "SUVbw" in node.GetName():
            suvbw_node = node
            break

    if not suvbw_node:
        # Fallback: first scalar volume
        vols = slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode")
        suvbw_node = vols[0] if vols else None

    if not suvbw_node:
        raise RuntimeError(f"{dro_id}: no SUVbw volume loaded")

    # Load RTSTRUCT (produces segmentation via SlicerRT)
    DICOMUtils.loadSeriesByUID([rs_uid])
    seg_nodes = slicer.util.getNodesByClass("vtkMRMLSegmentationNode")
    if not seg_nodes:
        raise RuntimeError(f"{dro_id}: no segmentation loaded")

    seg_node = seg_nodes[0]
    segment_id = seg_node.GetSegmentation().GetNthSegmentID(0)

    # Run QuantitativeIndicesTool CLI
    cli_node = logic.runOnSegment(
        suvbw_node, seg_node, segment_id,
        minimum=True, maximum=True, median=True,
    )

    # Extract results from CLI output (parameter group 3)
    results = {}
    for i in range(cli_node.GetNumberOfParametersInGroup(3)):
        name = cli_node.GetParameterName(3, i)
        value = cli_node.GetParameterDefault(3, i)
        if value != "--":
            results[name] = value

    slicer.mrmlScene.RemoveNode(cli_node)

    return results.get("Min_s", ""), results.get("Median_s", ""), results.get("Max_s", "")

# --- Main --------------------------------------------------------------------

def main():
    dro_map = build_dro_series_map()
    logic = QuantitativeIndicesToolLogic()

    # CSV header
    header = '"Section","ID","Description","SUVmin_expected","SUVmed_expected","SUVmax_expected","SUVmin_measured","SUVmed_measured","SUVmax_measured"'
    rows = [header]

    for section, dro_id, description, exp_min, exp_med, exp_max in DRO_LIST:
        pt_uid = dro_map.get(dro_id, {}).get("PT")
        rs_uid = dro_map.get(dro_id, {}).get("RTSTRUCT")

        if not pt_uid or not rs_uid:
            print(f"WARNING: {dro_id} missing PT or RTSTRUCT series, skipping")
            rows.append(f'"{section}","{dro_id}","{description}","{exp_min}","{exp_med}","{exp_max}",,,')
            continue

        try:
            meas_min, meas_med, meas_max = process_dro(dro_id, pt_uid, rs_uid, logic)
            print(f"{dro_id}: min={meas_min}, median={meas_med}, max={meas_max}")
        except Exception as e:
            print(f"ERROR processing {dro_id}: {e}")
            meas_min = meas_med = meas_max = ""

        # Escape inner quotes in description for CSV
        desc_escaped = description.replace('"', '""')
        rows.append(
            f'"{section}","{dro_id}","{desc_escaped}","{exp_min}","{exp_med}","{exp_max}","{meas_min}","{meas_med}","{meas_max}"'
        )

    csv_text = "\n".join(rows) + "\n"
    print("\n--- Results CSV ---")
    print(csv_text)

    # Save next to this script
    out_path = os.path.join(os.path.dirname(__file__) if "__file__" in dir() else slicer.app.temporaryPath,
                            "DRO_Slicer_PETIndiC.csv")
    with open(out_path, "w") as f:
        f.write(csv_text)
    print(f"Saved to: {out_path}")

main()
