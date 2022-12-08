from functools import cached_property
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

file = Path(__file__).parent.parent / "data" / "day7.txt"
raw = file.read_text().strip()


@dataclass
class File:
    name: str
    size: int


@dataclass
class Folder:
    name: str
    folders: list['Folder'] = field(default_factory=list)
    files: list[File] = field(default_factory=list)
    parent: Optional['Folder'] = None

    def __hash__(self):
        return id(self)

    def cd(self, name: str):
        if name == "..":
            return self.parent or self
        for folder in self.folders:
            if folder.name == name:
                return folder
        folder = Folder(name=name, parent=self)
        self.folders.append(folder)
        return folder

    @cached_property
    def size(self) -> int:
        return sum(x.size for x in self.files + self.folders)

    def traverse_folders(self):
        for folder in self.folders:
            yield from folder.traverse_folders()
        yield self


def parse_output(data: str):
    lines = data.strip().splitlines()
    root = Folder(name="/")
    cwd = root
    for line in lines:
        match line.split():
            case ["$", "cd", name]:
                cwd = root if name == "/" else cwd.cd(name)
            case ['dir', b]:
                cwd.folders.append(Folder(name=b, parent=cwd))
            case [size, name] if size.isdigit():
                cwd.files.append(File(name=name, size=int(size)))
    return root


if __name__ == "__main__":
    root = parse_output(raw)
    print(sum(x.size for x in root.traverse_folders() if x.size <= 100000))

    MIN_DELETE = root.size - (70000000 - 30000000)
    item = min(
        (x for x in root.traverse_folders() if x.size >= MIN_DELETE),
        key=lambda x: x.size,
    )
    print(item.size)
