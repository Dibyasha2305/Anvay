import os
import shutil


def package_project(project_dir):
    output_dir = "generated"

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    zip_base = os.path.join(
        output_dir,
        "anvay-integrated-project"
    )

    zip_path = shutil.make_archive(
        zip_base,
        "zip",
        project_dir
    )

    return zip_path