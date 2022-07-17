from src import resource_dir
from multiprocessing import Pipe


def read_configs_from(filepath) -> tuple:
    with open(resource_dir / filepath) as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]

    process_qtt = lines[lines.index('#processes') + 1: lines.index('#pipes')]
    pipes: set = __build_pipes_from(lines[lines.index('#pipes') + 1:])

    return process_qtt, pipes


def __build_pipes_from(config_lines: list) -> set:
    pipes = set()

    for line in config_lines:
        src, connection_type, dst = line.split()
        pipes.add(('duplex', (src, dst))) if connection_type == '<->' else pipes.add(('simplex', (src, dst)))

    return pipes


if __name__ == '__main__':
    read_configs_from('config.txt')
