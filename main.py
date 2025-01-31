import SimpleITK as sitk
import ImageProcessing as ip
import matplotlib.pyplot as plt

ct_fin = "path to read moving CT image/.nii or nii.gz"
mask_fin = "path to read liver mask of moving image/.nii or nii.gz"
refer_ct_fin = "path to read cropped liver CT image of reference/.nii or nii.gz"
ct_out_fin = 'path to write preprocessed image/.nii or nii.gz' # blank with '' will not save the preprocessd image

# read moving binary mask (liver segmentation)
mask_img = sitk.ReadImage(mask_fin)
mask_arr = sitk.GetArrayFromImage(mask_img)

# read moving CT
ct_img = sitk.ReadImage(ct_fin)
ct_arr = sitk.GetArrayFromImage(ct_img)

# crop and normalize the CT automatically
cropped_arr = ip.crop_liver_from_ct(ct_arr, mask_arr, margin = 10)
normalized_arr = ip.normalize_ct(cropped_arr,-160,240)

# generate SimpleITK Image
normalized_img = sitk.GetImageFromArray(normalized_arr)
normalized_img.SetOrigin(ct_img.GetOrigin())
normalized_img.SetSpacing(ct_img.GetSpacing())
normalized_img.SetDirection(ct_img.GetDirection())

# read reference CT
refer_ct_img = sitk.ReadImage(refer_ct_fin)
refer_ct_arr = sitk.GetArrayFromImage(refer_ct_img)

# resample preprocessed CT to match with reference CT
resampled_img = ip.resample_ct_to_reference(normalized_img, refer_ct_img)
resampled_arr = sitk.GetArrayFromImage(resampled_img)

# write preprocessed CT
if len(ct_out_fin) > 0:
    sitk.WriteImage(resampled_img,ct_out_fin)

print(f'resampled image: {resampled_img.GetSize()}, {resampled_img.GetOrigin()}, {resampled_img.GetSpacing()}, {resampled_img.GetDirection()}')
print(f'reference image: {refer_ct_img.GetSize()}, {refer_ct_img.GetOrigin()}, {refer_ct_img.GetSpacing()}, {refer_ct_img.GetDirection()}')

# display reference CT and preprocessed CT
fig, ax = plt.subplots(1,2)
ax[0].imshow(refer_ct_arr[40,:,:])
ax[1].imshow(resampled_arr[40,:,:])
plt.tight_layout()
plt.show()