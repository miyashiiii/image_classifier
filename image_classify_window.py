import csv
import time
from dataclasses import dataclass
from typing import List, Optional

import cv2
import numpy as np


class ImageClassifyWindow:
    NO_CLASS_STR = "no class"

    @dataclass
    class _Item:
        name: str
        img: np.ndarray
        label: Optional[int]

    def __init__(self, img_paths, class_names, result_csv_path, labels=None, name="ImageClassifyWindow"):
        self.name: str = name
        self.items: List[_Item] = []
        self.img_num: int = len(img_paths)
        labels = labels if labels is not None else [None] * self.img_num
        self.class_names: List[str] = class_names
        self.class_num: int = len(class_names)
        for p, l in zip(img_paths, labels):
            self.items.append(self._Item(p.name, cv2.imread(str(p)), l))
        self.result_csv_path = result_csv_path
        self._current_index = 0

    @property
    def _current_item(self) -> _Item:
        return self.items[self._current_index]

    @property
    def labels(self):
        return [item.label for item in self.items]

    def _get_class_name(self, idx):
        if idx is None:
            return self.NO_CLASS_STR
        return self.class_names[idx]

    def _increment_index(self):
        if self._current_index == self.img_num - 1:
            # print("no next image")
            return
        self._current_index += 1

    def _decrement_index(self):
        if self._current_index == 0:
            # print("no previous image")
            return
        self._current_index -= 1

    def _update_status_bar(self):
        class_ = self._get_class_name(self._current_item.label)
        text = f"{self._current_index + 1}/{self.img_num} | {self._current_item.name} | {class_}"
        cv2.displayStatusBar(self.name, text)

    def _update_window(self, is_next):
        if is_next:
            self._increment_index()
        else:
            self._decrement_index()
        cv2.imshow(self.name, self._current_item.img)
        self._update_status_bar()

    def _print_usage(self):
        print()
        print("Usage" + "-" * 30)
        print(f"  [{0}] - [{self.class_num - 1}]: classify")
        for i, class_name in enumerate(self.class_names):
            print(f"    [{i}]: {class_name}")
        print("  [x]: delete label")
        print("  [j]: next image")
        print("  [k]: previous image")
        print("  [p]: print all labels")
        print("  [s]: save csv")
        print("  [q]: quit")
        print("-" * 30)
        print()

    def _initialize_window(self):
        cv2.namedWindow(self.name)
        cv2.imshow(self.name, self.items[0].img)
        self._update_status_bar()
        self._print_usage()

    def _print_item(self, item):

        print(f"name: {item.name}, label:{self._get_class_name(item.label)}")

    def _print_all_items(self):
        print()
        print("labels" + "-" * 30)
        for item in self.items:
            self._print_item(item)
        print("-" * 30)
        print()

    def save_csv(self):
        names = [item.name for item in self.items]
        with open(self.result_csv_path, "w", encoding="utf_8_sig") as f:
            writer = csv.writer(f)
            writer.writerows(zip(names, self.labels))

    def show(self) -> List[Optional[int]]:
        self._initialize_window()

        while True:
            k = cv2.waitKey() & 0xFF
            chr_k = chr(k)
            if chr_k == "q":
                cv2.destroyWindow(self.name)
                break
            elif chr_k in [str(i) for i in range(self.class_num)]:
                self._current_item.label = int(chr_k)
                cv2.imshow(self.name, self._current_item.img)
                self._print_item(self._current_item)
                time.sleep(0.5)
                self._update_window(is_next=True)

            elif chr_k == "j":
                self._update_window(is_next=True)
            elif chr_k == "k":
                self._update_window(is_next=False)
            elif chr_k == "p":
                self._print_all_items()
            elif chr_k == "x":
                self._current_item.label = None
                self._update_window(is_next=False)
            elif chr_k == "s":
                self.save_csv()
                print("save csv to :", self.result_csv_path)
        return self.labels
