import typing
from dataclasses import dataclass, field
from typing import List, Union

Directory = typing.NewType("Directory", None)


@dataclass
class Node:
    name: str
    parent: Directory = field(init=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


@dataclass
class File(Node):
    size: int = 0


@dataclass
class Directory(Node):
    content: List[Union[File, Directory]] = field(default_factory=list)

    @property
    def size(self):
        return sum(node.size for node in self.content)

    def add(self, node):
        self.content.append(node)
        node.parent = self

    def get(self, name):
        return next(node for node in self.content if node.name == name)

    @property
    def directories(self):
        return [d for d in self.content if isinstance(d, Directory)]

    @property
    def all_directories(self):
        result = list(self.directories)
        for d in self.directories:
            result.extend(d.all_directories)
        return result

    @property
    def files(self):
        return [f for f in self.content if isinstance(f, File)]


def decode_output(terminal_output):
    root_dir = Directory('/')
    current_dir = root_dir
    ls_mode = False
    for line in terminal_output:
        words = line.split()
        if words[0] == '$':
            ls_mode = False
            if words[1] == 'cd':
                if words[2] == '/':
                    current_dir = root_dir
                elif words[2] == '..':
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir.get(words[2])
            elif words[1] == 'ls':
                ls_mode = True
        elif ls_mode and words[0] == 'dir':
            current_dir.add(Directory(words[1]))
        elif ls_mode:
            current_dir.add(File(words[1], int(words[0])))
    return root_dir


def sum_up_dirs_smaller_than(max_size, from_directory):
    return sum(d.size for d in from_directory.all_directories if d.size < max_size)


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        terminal_output = f.readlines()

    root_dir = decode_output(terminal_output)

    result1 = sum_up_dirs_smaller_than(100000, root_dir)
    print(f"Part 1: total size of directories smaller than 100000 is {result1}")
    if testing and expected1 is not None:
        assert result1 == expected1

    result2 = 0
    print(f"Part 2: {result2}")
    if testing and expected2 is not None:
        assert result2 == expected2


if __name__ == '__main__':
    main('test.txt', True, 95437, None)
    main('input.txt')
