import argparse
import csv
import shutil
from pathlib import Path


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
    parser.add_argument("-o", help="output dir")
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
    if labels_str:
        for l in labels_str:
            label = int(l[1]) if l[1] else None
            labels.append((l[0], label))

    else:
        print("label csv not found: ", input_dir / args.l)

    # output dir
    if not args.o:
        output_dir = input_dir / "classes"
    else:
        output_dir = Path(args.o)
    output_dir.mkdir(parents=True, exist_ok=True)

    class_dirs = []
    for class_name in class_names:
        class_dir = output_dir / class_name
        if class_dir.is_dir():
            shutil.rmtree(class_dir)
        class_dir.mkdir()
        class_dirs.append(class_dir)

    no_class_dir = output_dir / "no_class"

    # copy to each dir
    for image_name, label in labels:
        to_dir = class_dirs[label] if label is not None else no_class_dir
        # shutil.copy(image_dir / image_name.replace("_test2.png",".jpg"), to_dir)
        shutil.copy(image_dir / image_name, to_dir)
    print()
    print("result export to:", output_dir)

    # export result


if __name__ == "__main__":
    main()
