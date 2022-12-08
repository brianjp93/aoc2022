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
    lines = data.strip().split("$ ")
    root = Folder(name="/")
    cwd = root
    for line in lines:
        full = line.splitlines() or [line]
        match full[0].split():
            case ["ls"]:
                for ls_line in full[1:]:
                    a, b = ls_line.split()
                    if a == "dir":
                        cwd.folders.append(Folder(name=b, parent=cwd))
                    else:
                        cwd.files.append(File(name=b, size=int(a)))
            case ["cd", name]:
                cwd = root if name == "/" else cwd.cd(name)
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
