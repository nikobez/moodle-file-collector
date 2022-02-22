import configparser
import hashlib
import os

def config_read(path: str):
    config = configparser.ConfigParser()
    config.read(path)
    wdir = config.get("Settings", "work_dir")
    return wdir

def do_check(path: str):
    return

if __name__ == "__main__":
    work_dir = config_read('config.ini')
    do_check(work_dir)