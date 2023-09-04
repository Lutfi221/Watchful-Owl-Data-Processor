from .test_utils import compare_entry
from .consolidator import Consolidator
from ..types import Entry, EntryData, Window, WindowData

PATHS: list[str] = [
    "/program/0.exe",
    "/program/1.exe",
    "/program/2.exe",
    "/program/3.exe",
]
TITLES: list[str] = ["Zero", "One", "Two", "Three"]


def window_data_mock(i: int, active=False) -> WindowData:
    w: WindowData = {"path": PATHS[i], "title": TITLES[i]}
    if active:
        w["isActive"] = True
    return w


def test_1():
    def generate_entries() -> list[EntryData]:
        return [
            {
                "timestamp": 0,
                "windows": [
                    window_data_mock(0),
                    window_data_mock(1, True),
                    window_data_mock(2),
                ],
            },
            {
                "timestamp": 1,
                "windows": [
                    window_data_mock(1, True),
                    window_data_mock(2),
                ],
            },
            {"timestamp": 2, "durationSinceLastUserInput": 60},
        ]

    consolidator = Consolidator()

    for entry in generate_entries():
        consolidator.insert_entry(entry)

    col = consolidator.generate_col()

    entries_original = generate_entries()
    entries_view = col.get_entries_view(0, 2)

    assert len(entries_original) == len(entries_view)

    for i in range(0, len(entries_original)):
        e = entries_original[i]
        windows: list[WindowData] = []
        if "windows" in e:
            windows = [
                Window(w["path"], w["title"], w.get("isActive", False))
                for w in e["windows"]
            ]

        assert compare_entry(
            entries_view[i],
            Entry(e["timestamp"], windows, e.get("durationSinceLastUserInput", None)),
        )
