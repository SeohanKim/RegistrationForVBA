import SimpleITK as sitk
import numpy as np

# get boundary planes of liver mask
# axis = [z, y, x]
def get_boundaries(mask):

    z_indices = [z for z in range(mask.shape[0]) if 1 in mask[z, :, :]]
    lower_z = z_indices[0]
    upper_z = z_indices[-1]

    y_indices = [y for y in range(mask.shape[1]) if 1 in mask[:, y, :]]
    lower_y = y_indices[0]
    upper_y = y_indices[-1]

    x_indices = [x for x in range(mask.shape[2]) if 1 in mask[:, :, x]]
    lower_x = x_indices[0]
    upper_x = x_indices[-1]

    return upper_z, lower_z, upper_y, lower_y, upper_x, lower_x

def calculate_liver_dimension(boundaries):

    z = boundaries[0] - boundaries[1]
    y = boundaries[2] - boundaries[3]
    x = boundaries[4] - boundaries[5]

    return z, y, x

def crop_liver_from_ct(ct, mask, margin = 10):
    '''
    crop liver region from abdominal CT image

    ct: abdominal ct array to be cropped
    mask: liver segmentation array
    margin: percentage of liver, default = 10 %
    '''

    ct = ct * mask
    boundaries = get_boundaries(mask)
    liver_dim = calculate_liver_dimension(boundaries)

    target_size = (
        int(liver_dim[0] * margin * 0.02) // 2,
        int(liver_dim[1] * margin * 0.02) // 2,
        int(liver_dim[2] * margin * 0.02) // 2
    )

    cropped_ct = ct[boundaries[1]-target_size[0]:boundaries[0]+target_size[0],
    boundaries[3]-target_size[1]:boundaries[2]+target_size[1],
    boundaries[5]-target_size[2]:boundaries[4]+target_size[2]]

    return cropped_ct


def normalize_ct(ct, HU_min, HU_max):

    windowed_array = np.clip(ct, HU_min, HU_max)

    return windowed_array

def resample_ct_to_reference(moving_ct, fixed_ct):
    """
    Resample moving CT image to match both the voxel dimensions and physical size of fixed CT image

    moving_ct: SimpleITK Image or str - The image to be resampled
    fixed_ct: SimpleITK Image or str - The reference image providing target dimensions
    """

    if isinstance(moving_ct, str):
        moving_ct = sitk.ReadImage(moving_ct, sitk.sitkInt32)
    if isinstance(fixed_ct, str):
        fixed_ct = sitk.ReadImage(fixed_ct, sitk.sitkInt32)

    dimension = moving_ct.GetDimension()

    reference_image = sitk.Image(fixed_ct.GetSize(), moving_ct.GetPixelIDValue())
    reference_image.SetOrigin(fixed_ct.GetOrigin())
    reference_image.SetSpacing(fixed_ct.GetSpacing())
    reference_image.SetDirection(fixed_ct.GetDirection())

    reference_center = np.array(
        reference_image.TransformContinuousIndexToPhysicalPoint(np.array(reference_image.GetSize()) / 2.0))

    transform = sitk.AffineTransform(dimension)
    transform.SetMatrix(moving_ct.GetDirection())
    transform.SetTranslation(np.array(moving_ct.GetOrigin()) - reference_image.GetOrigin())

    centering_transform = sitk.TranslationTransform(dimension)
    img_center = np.array(moving_ct.TransformContinuousIndexToPhysicalPoint(np.array(moving_ct.GetSize()) / 2.0))
    centering_transform.SetOffset(np.array(transform.GetInverse().TransformPoint(img_center) - reference_center))
    composite_transform = sitk.CompositeTransform(transform)
    composite_transform.AddTransform(centering_transform)

    resampled_image = sitk.Resample(moving_ct, reference_image, composite_transform, sitk.sitkLinear, 0.0)

    return resampled_image



