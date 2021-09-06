import os


def main():

    project_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(project_path, "generate.py")

    cmd = "blender --background --python " + path + " -- " + project_path

    os.system(cmd)


if __name__ == "__main__":
    main()