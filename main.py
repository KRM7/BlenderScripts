"""Blender 2.91 required"""

import os


def main():

    project_path = os.path.abspath(os.path.dirname(__file__))
    generate_path = os.path.join(project_path, "generate.py")

    cmd = "sudo blender-2.91.2-linux64/blender -b -noaudio -d -E CYCLES --python " + generate_path + " -- " + project_path

    os.system(cmd)


if __name__ == "__main__":
    main()