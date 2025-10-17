import numpy as np
import numpy.typing as npt
from typing import Tuple
import cv2


def compute(
    frame_a: npt.NDArray[np.uint8],
    frame_b: npt.NDArray[np.uint8],
    pyr_scale,
    levels,
    winsize,
    iterations,
    poly_n,
    poly_sigma,
    flags,
) -> npt.NDArray[np.float32]:
    w, h = frame_a.shape[:2]
    a = cv2.resize(frame_a, (256 * h // w, 256))
    b = cv2.resize(frame_b, (256 * h // w, 256))
    aa = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    bb = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(
        aa,
        bb,
        None,
        pyr_scale,
        levels,
        winsize,
        iterations,
        poly_n,
        poly_sigma,
        cv2.OPTFLOW_FARNEBACK_GAUSSIAN if flags else 0,
    )
    flow = cv2.resize(flow, (h, w))
    return flow


def interpolate(
    frame_a: npt.NDArray[np.uint8],
    frame_b: npt.NDArray[np.uint8],
    flow: npt.NDArray[np.float32],
    t: float,
    options: int = 0,
) -> npt.NDArray[np.uint8]:

    h, w = frame_a.shape[:2]

    # 1. Create coordinate grid
    y, x = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")

    # 2. Apply scaled flow
    map_x = (x + flow[..., 0] * t).astype(np.float32)
    map_y = (y + flow[..., 1] * t).astype(np.float32)

    # 3. Remap pixels from frame_a towards frame_b
    warped_a = cv2.remap(frame_a, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    if options == 1:
        return warped_a

    # 4. Optionally also warp frame_b backwards for blending
    map_x_back = (x - flow[..., 0] * (1 - t)).astype(np.float32)
    map_y_back = (y - flow[..., 1] * (1 - t)).astype(np.float32)

    warped_b = cv2.remap(
        frame_b, map_x_back, map_y_back, interpolation=cv2.INTER_LINEAR
    )
    if options == 2:
        return warped_b

    # 5. Blend the two warped images
    interpolated = cv2.addWeighted(warped_a, 1 - t, warped_b, t, 0)
    return interpolated


def debug(
    img: npt.NDArray[np.uint8],
    flow: npt.NDArray[np.float32],
    step: int = 16,
    color: Tuple[int, int, int] = (0, 255, 0),
) -> npt.NDArray[np.uint8]:

    # HSV image
    hsv = np.zeros_like(img)
    hsv[..., 1] = 255
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    flow_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Plot arrows into HSV image
    h, w = img.shape[:2]
    for y in range(0, h, step):
        for x in range(0, w, step):
            fx, fy = flow[y, x]
            end_point = (int(x + fx), int(y + fy))
            cv2.arrowedLine(flow_img, (x, y), end_point, color, 1, tipLength=0.3)
    return flow_img
