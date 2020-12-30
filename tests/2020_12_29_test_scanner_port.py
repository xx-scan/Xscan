# coding:utf-8
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)


def main():
    from lib.conf import load_user_config
    config = load_user_config(project_dir=PROJECT_DIR)
    print(config)


def test_celery():
    from tasks.xscan.tasks import push_cmd
    from core.portscan.port_scanner import portscan

    masscan_shell, masscan_result_path = portscan(scan_ip='127.0.0.1')

    results = push_cmd.delay(masscan_shell)
    print(results)


if __name__ == '__main__':
    # main()
    test_celery()

