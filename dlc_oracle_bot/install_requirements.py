import subprocess
import sys


def install_requirements():
    commands = [
        [
            sys.executable,
            '-m',
            'pip',
            'install',
            '--upgrade',
            'pip',
        ],
        [
            sys.executable,
            '-m',
            'pip',
            'install',
            '--requirement',
            'requirements.txt',
        ]
    ]
    for command in commands:
        subprocess.check_call(command)

    sys.exit(0)