import argparse
import csv
from pathlib import Path

import cv2

from image_classify_window import ImageClassifyWindow


def read_csv(csv_path):
    if not csv_path.is_file():
        return

    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="input dir")
    parser.add_argument("-i", help="image dir", default="image")
    parser.add_argument("-c", help="class names csv path", default="class_names.csv")
    parser.add_argument("-l", help="label csv path", default="label.csv")
    parser.add_argument("-o", help="output dir", default="result")
    args = parser.parse_args()

    # input_dir
    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        print("not dir: ", input_dir)
        return
    # image dir
    image_dir = input_dir / args.i
    if not image_dir.is_dir():
        print("not dir: ", image_dir)
        return

    # class name
    class_names = read_csv(input_dir / args.c)
    if not class_names:
        print("class name file not found: ", args.c)
        return
    class_names = [v[0] for v in class_names]

    # labels
    labels_str = read_csv(input_dir / args.l) if args.l else None
    labels = []
    for l in labels_str:
        if not l[1]:
            labels.append(None)
            continue
        labels.append(int(l[1]))

    # output dir
    output_dir = Path(args.o) / input_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)
    result_csv_path = output_dir / "label.csv"

    # search images
    extensions = [".jpg", ".jpeg", ".JPG"]
    paths = []
    for ext in extensions:
        paths += list(image_dir.glob(f"*{ext}"))
    print("images: ", len(paths))

    if not paths:
        print("no image in ", image_dir)
        return

    paths.sort()

    # show window
    window = ImageClassifyWindow(paths, class_names, result_csv_path, labels)
    window.show()
    cv2.destroyAllWindows()

    # print to stdout
    print()
    if None in window.labels:
        print("not classified:")
        for p, l in zip(paths, labels):
            if l is None:
                print(f"  {p.name}")

    print()
    print("result export to:", result_csv_path)

    # export result
    window.save_csv()


if __name__ == "__main__":
    main()
