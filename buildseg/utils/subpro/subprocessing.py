import os.path as osp
import sys
import subprocess


def check_package_version():
    sys.executable = "python"
    package_path = osp.join(osp.dirname(osp.realpath(__file__)), "env_packs.py")
    # print(package_path)
    args = [sys.executable, package_path]
    child_proccess = subprocess.Popen(args, 
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      shell=True,
                                      creationflags=subprocess.CREATE_NEW_CONSOLE)
    child_process_output = child_proccess.communicate()
    packs_ver = child_process_output[0].decode("utf8").strip()
    return eval(packs_ver)


# TODO: some paddle's infer code
def sub_paddle():
    pass


if __name__ == "__main__":
    packages_version = check_package_version()
    print(type(packages_version))
    print(packages_version["paddle"])