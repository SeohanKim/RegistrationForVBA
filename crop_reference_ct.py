import SimpleITK as sitk
import ImageProcessing as ip
import matplotlib.pyplot as plt

ct_fin = "path to read reference CT image/.nii or nii.gz"
mask_fin = "path to read liver mask of reference image/.nii or nii.gz"
ct_out_fin = '' # path/to/write/preprocessed/image/.nii or nii.gz

# read binary mask (liver segmentation)
mask_img = sitk.ReadImage(mask_fin)
mask_arr = sitk.GetArrayFromImage(mask_img)

# read moving CT
ct_img = sitk.ReadImage(ct_fin)
ct_arr = sitk.GetArrayFromImage(ct_img)

# crop and window the CT automatically
cropped_arr = ip.crop_liver_from_ct(ct_arr, mask_arr, margin = 10)
normalized_arr = ip.normalize_ct(cropped_arr,-160,240)

# generate SimpleITK Image
normalized_img = sitk.GetImageFromArray(normalized_arr)
normalized_img.SetOrigin(ct_img.GetOrigin())
normalized_img.SetSpacing(ct_img.GetSpacing())
normalized_img.SetDirection(ct_img.GetDirection())

if ct_out_fin:
    sitk.WriteImage(normalized_img,ct_out_fin)

# display reference CT and preprocessed CT
plt.imshow(normalized_arr[40,:,:])
plt.tight_layout()
plt.show()