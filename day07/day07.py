import typing
from dataclasses import dataclass, field

Directory = typing.NewType("Directory", None)


@dataclass
class Node:
    name: str
    parent: Directory = field(init=False)

    @property
    def size(self) -> int:
        return 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


@dataclass
class File(Node):
    _size: int = 0

    @property
    def size(self) -> int:
        return self._size


@dataclass
class Directory(Node):
    content: list[Node] = field(default_factory=list)

    @property
    def size(self) -> int:
        return sum(node.size for node in self.content)

    def add(self, node: Node):
        self.content.append(node)
        node.parent = self

    def get(self, name: str) -> Node:
        return next(node for node in self.content if node.name == name)

    @property
    def directories(self) -> list['Directory']:
        return [node for node in self.content if isinstance(node, Directory)]

    @property
    def all_directories(self) -> list['Directory']:
        result = list(self.directories)
        for d in self.directories:
            result.extend(d.all_directories)
        return result


def decode_output(terminal_output) -> Directory:
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
        elif ls_mode:
            if words[0] == 'dir':
                current_dir.add(Directory(words[1]))
            else:
                current_dir.add(File(words[1], int(words[0])))
    return root_dir


def solve_problem(filename, expected1=None, expected2=None):
    print(f'--------- {filename}')

    with open(filename) as f:
        terminal_output = f.readlines()

    root_dir = decode_output(terminal_output)

    result1 = sum(d.size for d in root_dir.all_directories if d.size <= 100_000)
    print(f"Part 1: total size of directories smaller than 100k is {result1}")
    if expected1 is not None:
        assert result1 == expected1

    min_size_to_delete = root_dir.size - 40_000_000
    candidate_dirs = (d for d in root_dir.all_directories if d.size >= min_size_to_delete)
    min_directory = min(candidate_dirs, key=lambda d: d.size)
    result2 = min_directory.size
    print(f"Part 2: need to delete directory '{min_directory}' with size {result2}")
    if expected2 is not None:
        assert result2 == expected2


def main():
    solve_problem('test.txt', 95_437, 24_933_642)
    solve_problem('input.txt', 1648397, 1815525)


if __name__ == '__main__':
    main()
