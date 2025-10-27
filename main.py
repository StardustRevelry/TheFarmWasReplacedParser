import os
import sys
import yaml
import shutil

from parser import parse_all_files, save_nodes

if __name__ == '__main__':
    # read save path from config.yaml
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        save_path = config['SAVE_PATH']
        stack_depth = config['MAX_STACK_DEPTH']

    # set stack depth
    sys.setrecursionlimit(stack_depth)

    # init dirs
    current_dir = os.path.dirname(os.path.realpath(__file__))
    scripts_dir = os.path.join(current_dir, 'scripts')
    build_dir = os.path.join(current_dir, 'build')

    # parse scripts
    shutil.rmtree(build_dir, ignore_errors=True)
    nodes = parse_all_files(scripts_dir)
    save_nodes(nodes, build_dir)

    # copy build files to save path
    shutil.copy2(os.path.join(save_path, "save.json"), build_dir)
    shutil.rmtree(save_path, ignore_errors=True)
    shutil.copytree(build_dir, save_path)


