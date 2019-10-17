import csv
import time
from dataclasses import dataclass
from typing import List, Optional

import cv2
import numpy as np
import regex as re


@dataclass
class ImageItem:
    name: str
    img: np.ndarray
    label: Optional[int]


class ImageClassifyWindow:
    NO_CLASS_STR = "no class"
    WINDOW_WIDTH = 500

    def __init__(self, items: List[ImageItem], class_names, result_csv_path, name="ImageClassifyWindow"):
        self.name: str = name
        self.img_num: int = len(items)
        self.items = items
        for item in self.items:
            h, w, _ = item.img.shape
            item.img = cv2.resize(item.img, (self.WINDOW_WIDTH, h * self.WINDOW_WIDTH // w))
        self.class_names: List[str] = class_names
        self.class_num: int = len(class_names)
        self.result_csv_path = result_csv_path
        self._current_index = 0

    @property
    def _current_item(self) -> ImageItem:
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
        # 漢字等の文字があるとdisplayStatusBarがうまくいかないので置換
        name = self._current_item.name
        p = re.compile(r'[\p{Script=Han}〜]+')
        name = re.sub(p, "_", name)

        class_ = self._get_class_name(self._current_item.label)
        text = f"{self._current_index + 1}/{self.img_num} | {name} | {class_}"
        cv2.displayStatusBar(self.name, text)

    def _change_image(self, move_idx):
        idx = self._current_index + move_idx
        if idx <= 0:
            self._current_index = 0
        elif idx >= self.img_num - 1:
            self._current_index = self.img_num - 1
        else:
            self._current_index = idx

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
        print("  [f]: jump to 10 after image")
        print("  [b]: jump to 10 before image")
        print("  [g]: jump to first image")
        print("  [e]: jump to last image")
        print("  [p]: print all labels")
        print("  [s]: save csv")
        print("  [q]: save and quit")
        print("  [esc]: quit (no save)")
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
                self.save_csv()
                print("result export to:", self.result_csv_path)
                break
            elif chr_k == "\x1b":
                cv2.destroyWindow(self.name)
                break
            elif chr_k in [str(i) for i in range(self.class_num)]:
                self._current_item.label = int(chr_k)
                cv2.imshow(self.name, self._current_item.img)
                self._print_item(self._current_item)
                time.sleep(0.5)
                self._change_image(1)

            elif chr_k == "j":
                self._change_image(1)
            elif chr_k == "k":
                self._change_image(-1)
            elif chr_k == "f":
                self._change_image(10)
            elif chr_k == "b":
                self._change_image(-10)
            elif chr_k == "g":
                self._change_image(-self.img_num)
            elif chr_k == "e":
                self._change_image(self.img_num)
            elif chr_k == "p":
                self._print_all_items()
            elif chr_k == "x":
                self._current_item.label = None
                self._change_image(0)
            elif chr_k == "s":
                self.save_csv()
                print("save csv to :", self.result_csv_path)
        return self.labels
