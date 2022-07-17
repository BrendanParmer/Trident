import argparse
from collections import defaultdict
import matplotlib.pyplot as plt
from multiprocessing import Pool, Lock
from multiprocessing.sharedctypes import Value
import numpy as np
import os
import pygame
import pygame.gfxdraw
from scipy.ndimage import gaussian_filter
from scipy.spatial import Delaunay

def sample(ref, n=1000000):
    np.random.seed(0)
    w, h = x.shape
    xs = np.random.randint(0, w, size=n)
    ys = np.random.randint(0, h, size=n)
    value = ref[xs, ys]
    accept = np.random.random(size=n) < value
    points = np.array([xs[accept], ys[accept]])
    return points.T, value[accept]

def get_color_of_tri(tri, image):
    colors = defaultdict(lambda: [])
    w, h, _ = image.shape
    for i in range(0, w):
        for j in range(0, h):
            # Gets the index of the triangle the point is in
            index = tri.find_simplex((i, j))
            colors[int(index)].append(inp[i, j, :])
    # For each triangle, find the average colour
    for index, array in colors.items():
        colors[index] = np.array(array).mean(axis=0)
    return colors

def draw(tri, colours, screen, upscale):
    s = screen.copy()
    for key, c in colours.items():
        t = tri.points[tri.simplices[key]]
        pygame.gfxdraw.filled_polygon(s, t * upscale, c)
        pygame.gfxdraw.polygon(s, t * upscale, c)
    return s

def init_pool_processes(c: Value):
    global count
    count = c

def process_image(index: int, rate: int, begin: int, end: int) -> None:
    i = index - begin
    n = max(4, rate)*(index + 1)
    tri = Delaunay(points[:n, :])
    colors = get_color_of_tri(tri, inp)
    s = draw(tri, colors, screen, upscale)
    s = pygame.transform.smoothscale(s, (w, h))
    pygame.image.save(s, f"{outdir}/{i:04d}.png")
    with count.get_lock():
        count.value += 1
        percent = count.value/(end - begin) * 100
        print(f"{count.value:04d}/{end - begin} {percent:.2f}", end='\r')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create low poly images and videos from the command line")
    parser.add_argument("image", help="Input image")
    parser.add_argument("--begin", default=0, type=int, help="Starting index")
    parser.add_argument("--end", default=100, type=int, help="Ending index")
    parser.add_argument("--rate", default=10, type=int, help="Rate of point sampling (higher numbers generate more detailed images, with more triangles")
    parser.add_argument("--worker_count", default=4, type=int, help="Number of worker processes used")
    parser.add_argument("--video", action='store_true', help="Render a video at the end")
    parser.add_argument("--framerate", default=24, type=int, help="Framerate of rendered video")
    args = parser.parse_args()

    inp = pygame.surfarray.pixels3d(pygame.image.load(args.image))
    perceptual_weight = np.array([0.2126, 0.7152, 0.0722])
    grayscale = (inp * perceptual_weight).sum(axis=-1)

    x = gaussian_filter(grayscale, 2, mode="reflect")
    x2 = gaussian_filter(grayscale, 30, mode="reflect")

    # Take the difference, deweight negatives, normalize
    diff = (x - x2)
    diff[diff < 0] *= 0.1
    diff = np.sqrt(np.abs(diff) / diff.max())

    samples, v = sample(diff)
    plt.scatter(samples[:, 0], -samples[:, 1], c=v, s=0.2, edgecolors="none", cmap="viridis")

    w, h, _ = inp.shape
    upscale = 2
    screen = pygame.Surface((w * upscale, h * upscale))
    screen.fill(inp.mean(axis=(0, 1)))
    corners = np.array([(0, 0), (0, h - 1), (w - 1, 0), (w - 1, h - 1)])
    points = np.concatenate((corners, samples))

    img_name = (args.image).split(".")[0]
    img_name = img_name.split("/")[-1]
    outdir = f"output/{img_name}"
    os.makedirs(outdir, exist_ok=True)

    c = Value('i', 0)
    with Pool(initializer=init_pool_processes, initargs=(c,), processes=args.worker_count) as pool:
        pool.starmap(process_image, [(i, args.rate, args.begin, args.end) for i in range(args.begin, args.end)])
    print("Finished creating images")

    print(args.video)
    if args.video:
        os.system(f"ffmpeg -framerate {args.framerate} -i {outdir}/%04d.png {outdir}/{img_name}.mp4")
        print("Created video")