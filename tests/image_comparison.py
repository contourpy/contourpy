import numpy as np
import os
from PIL import Image
from shutil import copyfile


def compare_images(test_buffer, baseline_filename, test_filename_suffix=None, max_threshold=None,
                   mean_threshold=None):
    if max_threshold is None:
        max_threshold = 100
    if mean_threshold is None:
        mean_threshold = 0.02

    if test_filename_suffix:
        basename, extension = os.path.splitext(baseline_filename)
        test_filename = f"{basename}_{test_filename_suffix}{extension}"
    else:
        test_filename = baseline_filename

    max_diff = None
    mean_diff = None

    try:
        test_image = np.asarray(Image.open(test_buffer).convert("RGBA"))
        test_image = test_image.astype(np.int16)

        full_baseline_filename = os.path.join("tests", "baseline_images", baseline_filename)
        assert os.path.isfile(full_baseline_filename)

        baseline_image = np.asarray(Image.open(full_baseline_filename).convert("RGBA"))
        baseline_image = baseline_image.astype(np.int16)

        diff = np.abs(test_image - baseline_image)
        max_diff = diff[:, :, :3].max()
        mean_diff = diff[:, :, :3].mean()

        assert max_diff < max_threshold and mean_diff < mean_threshold
    except AssertionError:
        # Write test image.
        result_directory = "result_images"
        if not os.path.exists(result_directory):
            os.makedirs(result_directory)

        full_test_filename = os.path.join(result_directory, test_filename)
        with open(full_test_filename, "wb") as f:
            f.write(test_buffer.getbuffer())

        if max_diff is not None and mean_diff is not None:
            basename, extension = os.path.splitext(test_filename)

            # Copy expected file.
            expected_filename = f"{basename}-expected{extension}"
            expected_filename = os.path.join(result_directory, expected_filename)
            copyfile(full_baseline_filename, expected_filename)

            print(f"diffs: max {max_diff}, mean {mean_diff:.4f} "
                  f"(thresholds max {max_threshold}, mean {mean_threshold})")

            # Write difference image.
            difference_filename = f"{basename}-diff{extension}"
            difference_filename = os.path.join(result_directory, difference_filename)

            diff *= 10
            diff = np.clip(diff, 0, 255).astype(np.uint8)
            diff[:, :, 3] = 255
            Image.fromarray(diff).save(difference_filename, format="png")

        raise
