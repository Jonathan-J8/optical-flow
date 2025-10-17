import argparse


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image_a",
        help="path to the first image to apply optical flow from",
    )
    parser.add_argument(
        "--image_b",
        help="path to the second image to apply optical flow to",
    )

    parser.add_argument(
        "--exemple1",
    )
    parser.add_argument(
        "--exemple2",
    )
    parser.add_argument(
        "--exemple3",
    )
    args = parser.parse_args()

    if args.exemple1:
        return "./public/face0.png", "./public/face1.png"
    if args.exemple2:
        return "./public/test0.png", "./public/test1.png"
    if args.exemple3:
        return "./public/ai0.png", "./public/ai1.png"
    if args.image_a and args.image_b:
        return args.image_a, args.image_b
    return "./public/face0.png", "./public/face1.png"
