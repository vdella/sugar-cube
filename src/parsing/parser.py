from src import resource_dir
from multiprocessing import Pipe


def read_configs_from(filepath) -> tuple:
    """Reads configs from :param filepath: and :returns a tuple with (process_quantity, pipe_map, operations)."""
    with open(resource_dir / filepath) as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]  # Trims the \n at the end of the lines.

    process_qtt = __processes_qtt_from(lines[lines.index('#processes') + 1: lines.index('#pipes')])
    pipes: dict = __build_pipes_from(lines[lines.index('#pipes') + 1:])

    return process_qtt, pipes


def __processes_qtt_from(config_lines):
    """Digests info from :param config_lines in order to retrieve the process quantity."""
    qtt_as_list = config_lines
    qtt_as_str = qtt_as_list.pop()  # Gets the single element of the list.
    return int(qtt_as_str)


def __build_pipes_from(config_lines: list) -> dict:
    """:returns a pipe dictionary indexed by the processes ID's.
    Connections inside the dict follow a (src_end_point, dst_end_point) pattern."""
    pipes = dict()

    for line in config_lines:
        src, dst = line.split()
        pipes[(int(src), int(dst))] = Pipe()

    return pipes


if __name__ == '__main__':
    print(read_configs_from('config.txt'))
