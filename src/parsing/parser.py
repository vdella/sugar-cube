from src import resource_dir
from multiprocessing import Pipe


def read_configs_from(filepath) -> tuple:
    with open(resource_dir / filepath) as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]

    process_qtt = __processes_qtt_from(lines[lines.index('#processes') + 1: lines.index('#pipes')])
    pipes: dict = __build_pipes_from(lines[lines.index('#pipes') + 1: lines.index('#operations')])
    operations = lines[lines.index('#operations') + 1:]
    operations = __digest_operations_from(operations, process_qtt)

    return process_qtt, pipes, operations


def __processes_qtt_from(config_lines):
    qtt_as_list = config_lines
    qtt_as_str = qtt_as_list.pop()
    return int(qtt_as_str)


def __build_pipes_from(config_lines: list) -> dict:
    pipes = dict()

    for line in config_lines:
        src, dst = line.split()
        pipes[(int(src), int(dst))] = Pipe()

    return pipes


def __digest_operations_from(config_lines: list, process_qtt: int) -> dict:
    operations = {i: [] for i in range(process_qtt)}

    now = -1
    for line in config_lines:
        if '>' in line:
            now += 1
        else:
            operations[now].append(line)

    return operations


if __name__ == '__main__':
    print(read_configs_from('config.txt'))
