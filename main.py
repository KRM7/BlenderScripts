import os


def main():

    project_path = os.path.abspath(os.path.dirname(__file__))
    generate_path = os.path.join(project_path, "generate.py")

    cmd = "blender --background --verbose 0 --log-level 0 --python " + generate_path + " -- " + project_path

    os.system(cmd)


if __name__ == "__main__":
    main()