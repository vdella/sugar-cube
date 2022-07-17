from src import resource_dir
from multiprocessing import Pipe


def read_configs_from(filepath) -> tuple:
    with open(resource_dir / filepath) as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]

    process_qtt = lines[lines.index('#processes') + 1: lines.index('#pipes')]
    pipes: dict = __build_pipes_from(lines[lines.index('#pipes') + 1:])

    return process_qtt, pipes


def __build_pipes_from(config_lines: list) -> dict:
    pipes = dict()

    for line in config_lines:
        src, dst = line.split()
        pipes[(int(src), int(dst))] = Pipe()

    return pipes


if __name__ == '__main__':
    print(read_configs_from('config.txt'))
