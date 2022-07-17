# Trident
## About
<table style="margin-left: auto; margin-right: auto;">
    <tr>
        <td>
            <img
                src="https://github.com/BrendanParmer/Trident/blob/master/imgs/jwst.jpeg"
                alt="Original"
                width="850"
                height="850">
        </td>
        <td>
            <img
                src="https://github.com/BrendanParmer/Trident/blob/master/imgs/jwst.gif"
                alt="Trident animation"
                width="850"
                height="850">
        </td>
    </tr>
    <tr>
        <td>
            <p style="text-align: center;">Original</p>
        </td>
        <td>
            <p style="text-align: center;">Trident animation</p>
        </td>
    </tr>
</table>
<p style="text-align: center;">Original image by NASA's James Webb Space Telescope</p>

A Python script that creates low poly images uses Delaunay triangulation, based on this [nice blog post by Samuel Hinton](https://cosmiccoding.com.au/tutorials/lowpoly) on how to achieve this effect. 

Trident uses multiprocessing to speed up this intensive process, lets the user specify parameters from the command line, and automatically handles things like video creation.

## Installation
1. Clone the Git repo

```git clone https://github.com/BrendanParmer/Trident```

2. Install the requirements.

```pip install -r requirements.txt```

## Usage
```python3 trident.py [-h] [--begin BEGIN] [--end END] [--rate RATE] [--worker_count WORKER_COUNT] [--video] [--framerate FRAMERATE] image```

* `-h`: print usage information
* `--begin BEGIN`: (Optional) beginning index. Higher numbers will mean more triangles at the first frame
* `--end END`: (Optional) ending index
* `--rate RATE`: (Optional) Rate of point sampling (higher numbers generate more detailed images, with more triangles)
* `--worker_count WORKER_COUNT`: (Optional) number of worker processes used
* `--video`: (Optional) render a video at the end
* `--framerate`: (Optional) framerate of a video rendered at the end
* `image`: path to the image you would like to make low-poly

## Examples
Use default settings:

```python3 trident.py [path/to/your/image]```

Specify parameters:

```python3 trident.py --begin 5 --end 1000 --rate 5 --worker_count 8 --video --framerate 30 [path/to/your/image]```

Single image

```python trident.py --begin 100 --end 101 [path/to/your/image]```

## Known Bugs
Help contribute by submitting a bug report or feature request! 

This has only been tested on Pop!_OS 22.04, so let me know how this runs on your operating system.

## Future
* Add support for converting videos to a low-poly style