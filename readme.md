# Liver CT Preprocessing

## Overview
This repository provides a set of Python scripts for preprocessing liver CT images. It includes functions for cropping the liver region based on segmentation masks, normalizing Hounsfield Unit (HU) values, and resampling CT images to match a reference CT.

## Features
- **Liver Mask Boundary Extraction**: Identifies the bounding planes of the liver region from a binary mask.
- **Liver Cropping**: Extracts the liver region from a full abdominal CT scan.
- **Normalization**: Applies windowing to the CT scan to normalize HU values.
- **Resampling**: Matches voxel dimensions and physical size of the moving CT to a reference CT.

## Dependencies
Ensure you have the following Python packages installed:

```bash
pip install SimpleITK numpy matplotlib
```

## Usage

### 1. Preprocess a Reference CT Image to remain only liver region
```python
import SimpleITK as sitk
import ImageProcessing as ip

ct_fin = "path/to/reference_CT.nii.gz"
mask_fin = "path/to/reference_liver_mask.nii.gz"
ct_out_fin = "path/to/output_reference_CT.nii.gz"

# Read CT and mask
mask_img = sitk.ReadImage(mask_fin)
mask_arr = sitk.GetArrayFromImage(mask_img)
ct_img = sitk.ReadImage(ct_fin)
ct_arr = sitk.GetArrayFromImage(ct_img)

# Crop and normalize
cropped_arr = ip.crop_liver_from_ct(ct_arr, mask_arr, margin=10)
normalized_arr = ip.normalize_ct(cropped_arr, -160, 240)

# Convert to SimpleITK image
normalized_img = sitk.GetImageFromArray(normalized_arr)
normalized_img.SetOrigin(ct_img.GetOrigin())
normalized_img.SetSpacing(ct_img.GetSpacing())
normalized_img.SetDirection(ct_img.GetDirection())

# Save output
if ct_out_fin:
    sitk.WriteImage(normalized_img, ct_out_fin)
```

### 2. Preprocess a Moving CT Image
```python
import SimpleITK as sitk
import ImageProcessing as ip

ct_fin = "path/to/moving_CT.nii.gz"
mask_fin = "path/to/moving_liver_mask.nii.gz"
refer_ct_fin = "path/to/reference_CT.nii.gz"
ct_out_fin = "path/to/output_CT.nii.gz"

# Read CT and mask
mask_img = sitk.ReadImage(mask_fin)
mask_arr = sitk.GetArrayFromImage(mask_img)
ct_img = sitk.ReadImage(ct_fin)
ct_arr = sitk.GetArrayFromImage(ct_img)

# Crop and normalize
cropped_arr = ip.crop_liver_from_ct(ct_arr, mask_arr, margin=10)
normalized_arr = ip.normalize_ct(cropped_arr, -160, 240)

# Convert to SimpleITK image
normalized_img = sitk.GetImageFromArray(normalized_arr)
normalized_img.SetOrigin(ct_img.GetOrigin())
normalized_img.SetSpacing(ct_img.GetSpacing())
normalized_img.SetDirection(ct_img.GetDirection())

# Resample to reference CT
refer_ct_img = sitk.ReadImage(refer_ct_fin)
resampled_img = ip.resample_ct_to_reference(normalized_img, refer_ct_img)

# Save output
if ct_out_fin:
    sitk.WriteImage(resampled_img, ct_out_fin)
```

## Registration using 3D Slicer
To perform registration of the processed CT images in **3D Slicer**, navigate to:

**Modules -> Plastimatch -> Registration -> B-spline Deformable Registration**

Set the following parameters:

### **Stage 1**
- Image subsampling rate: `4, 4, 2`
- Max iterations: `50`
- Transformation: `Affine`

### **Stage 2**
- Image subsampling rate: `4, 4, 2`
- Max iterations: `50`
- Grid size: `100`
- Regularization: `0.005`
- Landmark Penalty: `0.005`

### **Stage 3**
- Image subsampling rate: `2, 2, 1`
- Max iterations: `50`
- Grid size: `50`
- Regularization: `0.005`
- Landmark Penalty: `0.005`

### **Stage 4**
- Image subsampling rate: `1, 1, 1`
- Max iterations: `50`
- Grid size: `10`
- Regularization: `0.005`
- Landmark Penalty: `0.005`

## License
This project is open-source. Feel free to use and modify it as needed.

