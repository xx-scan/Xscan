# coding:utf-8
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)


def main():
    from lib.conf import load_user_config
    config = load_user_config(project_dir=PROJECT_DIR)
    print(config)


if __name__ == '__main__':
    main()

