import flow
import cv2
from timer import Timer
from ui import UI
from cli import cli


image_a_path, image_b_path = cli()
image_a = cv2.imread(image_a_path)
image_b = cv2.imread(image_b_path)
image_base = cv2.imread(image_a_path)
image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2RGB)
image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2RGB)
image_base = cv2.cvtColor(image_base, cv2.COLOR_BGR2RGB)

if image_a is None or image_b is None:
    print(f"Error: Could not read one or both images: {image_a_path}, {image_b_path}")
if image_a.shape != image_b.shape:
    print(
        f"Error: Images must be the same size. Got {image_a.shape} and {image_b.shape}"
    )

timer = Timer()
ui = UI(window_name="Optical_flow")

# feat: video recorder
# height, width = image_a.shape[:2]
# fourcc = cv2.VideoWriter_fourcc(*"avc1")
# out = cv2.VideoWriter("./public/optical_flow.mp4", fourcc, 24, (width, height))
# out.write(cv2.cvtColor(image_a, cv2.COLOR_BGR2RGB))

while True:

    ui.update()
    pyr_scale = ui.pyr_scale
    levels = ui.levels
    winsize = ui.winsize
    iterations = ui.iterations
    poly_n = ui.poly_n
    poly_sigma = ui.poly_sigma
    gaussian = ui.gaussian
    slow_motion = ui.slow_motion
    feedback = ui.feedback
    # 0: default optical flow
    # 1: only warp image A
    # 2: only warp image B
    optical_mode = ui.optical_mode

    timer.update()
    inc_frame = timer.normalized(slow_motion)  # 0 to 1

    flow_field = flow.compute(
        image_a,
        image_b,
        pyr_scale,
        levels,
        winsize,
        iterations,
        poly_n,
        poly_sigma,
        gaussian,
    )
    frame_flow = flow.interpolate(image_a, image_b, flow_field, inc_frame, optical_mode)
    frame_flow = cv2.cvtColor(frame_flow, cv2.COLOR_RGB2BGR)
    frame_debug = flow.debug(image_a, flow_field, 8)

    last_frame = 1 - (timer.delta_time * slow_motion)  # 1 - delta
    if feedback == 1:
        image_a = frame_flow
        if inc_frame > last_frame:
            image_a = image_base
    else:
        image_a = image_base

    ui.show(frame_debug, frame_flow)

    # feat: video recorder
    # out.write(frame_flow)
    # if inc_frame > last_frame:
    #     break

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

ui.cleanup()
