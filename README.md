<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h1 align="center">Blender DEM Visualization Toolkit</h3>

---
 
## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
    - [Requirements](#requirements)
    - [Installation](#installation)
- [Functions in this Module](#functions)
    - [fetchDEM()](#fetch)
    - [renderDEM()](#render)
    - [simplifyDEM()](#simplify)
- [Blender Usage](#usage)
    - [Render from python script using terminal](#terminal)
    - [Render from python script using GUI](#gui)
    - [Usage tips](#tips)
- [Acknowledgements](#acknowledgements)

<br/>

## 🧐 About <a name = "about"></a>
This is a python module of functions for creating 3D hillshade maps using Blender. It enables users with minimal Blender knowledge to fetch, clean, and visualize DEM data in the form of beautifully rendered hillshade maps.


This module is ultimately centered around its `renderDEM()` function which interfaces with Blender in order to generate a 3D rendered hillshade map using an input DEM image file.

### What is DEM Data?
A digital elevation model (DEM) is a 3D representation of a terrain's surface, created using remote sensing technologies to model the elevation of the ground. A DEM image is simply a visual representation of a digital elevation model (DEM), created by rendering the elevation data in a way that is easy to understand and interpret. Typically, within a DEM image each pixel carries its elevation data as values closer to white are higher and values closer to black are lower. These images can be fed into Blender to visualize this information in 3D space, creating high quality "hillshade" maps for use in cartography.

<br/>

## 🏁 Getting Started <a name = "getting_started"></a>
This module requires an installation of **Blender**, a free and open-source 3D modelling software, in order to utilize the `renderDEM()` function. At the time of writing, this module is working as of Blender 3.4 (latest version) and can be downloaded [here](https://www.blender.org/download/)


This module also requires an [OpenTopography API key](https://portal.opentopography.org/lidarAuthorizationInfo?s=api), obtained for free by creating an account with OpenTopography, in order to to utilize the `fetchDEM()` function. This must be done in order for the function to access the global DEM datasets hosted by OpenTopography through their API.

### 🔧 Requirements <a name = "requirements"></a>
- [Blender](https://www.blender.org/download/)
- [OpenTopography API key](https://portal.opentopography.org/lidarAuthorizationInfo?s=api)
- Python packages:
    - requests
    - PIL


`pip install requests PIL`

### ⛏️ Installation <a name = "installation"></a>
- To install this module, begin by first downloading Blender, the required python packages, as well as obtain an OpenTopography API key.

<br/>

## 📦 Functions in this Module <a name = "functions"></a>
Below you will find documentation surrounding the functions featured in this module, their parameters, and usage examples.

### fetchDEM() <a name = "fetch"></a>
```Python
fetchDEM(north_bound, south_bound, east_bound, west_bound, API_Key, output_dir, dataset = 'SRTMGL1')
```

Uses the OpenTopography API in order to fetch a .GeoTIFF raster image containing DEM data for your specified extent that can then be opened using GIS programs.


It is important to note that each dataset has limitations on the amount of area it can retrieve, and that fetching DEM data of a very large extent may result in long query times. Requests are limited to 500,000,000 km2 for GEDI L3, 125,000,000 km2 for SRTM15+ V2.1, 4,050,000 km2 for SRTM GL3, COP90 and 450,000 km2 for all other data.

**NOTE:** This function requires an OpenTopography API key in order to fetch maps from their database, obtained through [creating an account](https://portal.opentopography.org/newUser) on the OpenTopography website,


Parameters:
- `north_bound: float`
    - Latitude coordinate of the northern bound of your chosen DEM extent.
    - This value must be greater than `south_bound` in order to create a valid bounding box. Acceptable values range **between 90 and -90.**
    - **Requires float.**
- `south_bound: float`
    - Latitude coordinate of the southern bound of your chosen DEM extent.
    - This value must be less than `north_bound` in order to create a valid bounding box. Acceptable values range **between 90 and -90.**
    - **Requires float.**
- `east_bound: float`
    - Longitude coordinate of the eastern bound of your chosen DEM extent.
    - This value must be greater than `west_bound` in order to create a valid bounding box. Acceptable values range **between 180 and -180.**
    - **Requires float.**
- `west_bound: float`
    - Longitude coordinate of the western bound of your chosen DEM extent.
    - This value must be less than `east_bound` in order to create a valid bounding box. Acceptable values range **between 180 and -180.**
    - **Requires float.**
- `API_Key: str`
    - OpenTopography API key, required for the function to fetch global DEM data made available by OpenTopography. Obtained free [here](https://portal.opentopography.org/lidarAuthorizationInfo?s=api).
    - **Requires string.** 
- `output_dir: str`
    - Directory path of the fetched DEM (including .tif file extension).
    - Example: `'absolute/path/to/output.tif'`.
    - **Requires string.**
- `dataset: str`
    - Specifies the global raster DEM dataset hosted on OpenTopography to fetch data from.
    - Different datasets have different coverage, quality, cell resolution, or fetchable area limitations. In general, `'SRTMGL3'` (90m cell resolution) and `'SRTMGL1'` (30m cell resolution) are very high quality and widely used.
    - Available DEM datasets:
        - `'SRTMGL3'` (SRTM GL3 90m)
        - `'SRTMGL1'` (SRTM GL1 30m)
        - `'SRTMGL1_E'` (SRTM GL1 Ellipsoidal 30m)
        - `'AW3D30'` (ALOS World 3D 30m)
        - `'AW3D30_E'` (ALOS World 3D Ellipsoidal, 30m)
        - `'SRTM15Plus'` (Global Bathymetry SRTM15+ V2.1)
        - `'NASADEM'` (NASADEM Global DEM)
        - `'COP30'` (Copernicus Global DSM 30m)
        - `'COP90'` (Copernicus Global DSM 90m)
        - `'EU_DTM'` (DTM 30m)
        - `'GEDI_L3'` (DTM 1000m)
    - **Requires string and defaults to 'SRTMGL1'** 

Usage example:
```Python
# The following code fetches DEM data from OpenTopography using the SRTM GL1 30m dataset and a hypothetical API key

Key = '8da2375367b589517231f8fee1ae6b7c'

fetchDEM(north_bound = 50, south_bound = 49, east_bound = 81, west_bound = 80, API_Key = Key, output_dir = 'path/to/output/DEM.tif', dataset = 'SRTMGL1')
```

<br/>

### renderDEM() <a name = "render"></a>
```Python
renderDEM(dem_dir, output_dir, exaggeration = 0.5, resolution_scale = 50, samples = 5)
```

Uses Blender to generate a 3D rendered hillshade map image using an input DEM image file.


Parameters:
- `dem_dir: str`
    - Absolute directory of the input DEM image including its file extension. All standard image file types are acceptable as input and readable by Blender, **including .tif/.tiff files**.
    - Example: `'absolute/path/to/DEM.tif'`.
    - **Requires string.**
- `output_dir: str`
    - Absolute directory path of the outputted rendered image (including .png file extension).
    - Example: `'absolute/path/to/output.png'`.
    - **Requires string.**
- `exaggeration: float`
    - Level of topographic exaggeration to be applied to 3D plane based on input DEM. Higher values will result in "spiky" terrain and darker crevices between landforms.
    - **Requires float and defaults to 0.5.**
- `resolution_scale: int`
    - Scale of the rendered image resolution in relation to the input DEM resolution in the form of percentage. An input DEM with resolution 2000x2000 and a `resolution_scale = 100` will result in a rendered image with resolution 2000x2000, whereas `resolution_scale = 50` will result in a final render of 1000x1000.
    - It is recommended to keep this value around or below 50 while performing test renders to improve speed before raising it to 100 for the final render at full resolution. Has a great affect on render speed and resource load on computer.
    - **Requires integer and defaults to 50.**
- `samples: int`
    - Amount of samples to be used in the final render. Samples can be understood as how many "passes" Blender takes over the image during the rendering process, refining the image more and more each sample/pass, making it more clear and less noisy. Has an **extremely large** affect on render speed and resource load on computer.
    - Depending on the strength of your computer it is recommended to keep this value very low (from 1-10) while performing test renders before your final render where you can then raise it to anywhere from 20-500 for crisp image quality.
    - **Requires integer and defaults to 5.**


Usage example:
```Python
# The following code uses Blender to render a 3D hillshade map

# Notice the very conservative resolution_scale and samples values,
# do not underestimate the length of time it takes to render image with these values set too high

renderDEM(dem_dir = 'path/to/dem.tif', output_dir = 'path/to/outputRender.png', exaggeration = 0.5, resolution_scale = 25, samples = 2)
```


For more information on using Blender to execute this function, see the [Blender Usage](#usage) section.

<br/>

### simplifyDEM() <a name = "simplify"></a>
```Python
simplifyDEM(dem_dir, output_dir, reduction_factor = 2)
```

Uses the PIL package to read in an input DEM image (of likely a high resolution) and output a down-sampled image with lower file size and resolution using a resample method appropriate for DEM maps. May be helpful depending on your DEM data source for easing resource requirements when rendering images in Blender.


**NOTE:** this function currently does not work with .GeoTIFF files which contain geospatial metadata, this method is intended to be used to prepare a file before it is imported into Blender to ease computational requirements on computers.


Parameters:
- `dem_dir: str`
    - Directory of the input DEM image including its file extension. All standard image file types are acceptable as input **including .tif/.tiff files**.
    - Example: `'absolute/path/to/DEM.tif'`.
    - **Requires string.**
- `output_dir: str`
    - Directory path of the outputted down-sampled image (including chosen file extension, .tif or .png is recommended).
    - Example: `'absolute/path/to/output.png'`.
    - **Requires string.**
- `reduction_factor: int`
    - Refers to the integer by which to divide the input DEM resolution by. A `reduction_factor = 4` will result in a down-sampled image with a quarter of the original resolution, whereas a `reduction_factor = 10` will result in a down-sampled image with a tenth of the original resolution.
    - Be gentle with the amount you reduce the resolution by, depending on the size of your input image, reducing the resolution by more than half could have negative impacts on its clarity in the final rendered image.
    - **Requires integer and defaults to 2 (reducing resolution by half).**


Usage example:
```Python
# The following code reduces the resolution of the input DEM to be a quarter of its original

simplifyDEM(dem_dir = 'path/to/dem.tif', output_dir = 'path/to/outputRender.png', reduction_factor = 4)
```

<br/>

## 🗺️ Blender Usage <a name = "usage"></a>
**IMPORTANT:** The following methods will render a map based on your python script using Blender's own python installation and interpreter. This means it does not have any packages installed other than its own default bpy package (and some others). There are likely ways around this that install outside packages into Blender however it is beyond the scope of this project. For this reason it is important that the script you feed into Blender to render your 3D map **ONLY contains your function call of renderDEM()** and your chosen argument parameters like this...


Example script.py:
```Python
# Script to render a 3D hillshade map in Blender
import BlenderMapDEM

renderDEM(dem_dir = 'C:/Users/sebas/OneDrive/Desktop/DEM.png', output_dir = 'C:/Users/sebas/OneDrive/Desktop/render.png', exaggeration = 0.5, resolution_scale = 100, samples = 50)

# End of script
```

<br/>

### 🖥️ Render Map from Python Script Using Terminal <a name = "terminal"></a>
- Steps to render map using terminal:
    - If Blender is not added to your PATH, in your terminal navigate to your Blender installation directory that contains your Blender.exe file. On Windows this defaults to: `C:\Program Files\Blender Foundation\Blender 3.4` as of Blender 3.4.
    - If Blender is added to your PATH, you should be able to run Blender from anywhere in your terminal. You can be sure it is added to your PATH if running "Blender" in your terminal from any directory opens a Blender instance. (see LINK for adding Blender to PATH).
    - To run a python script which contains the renderDEM() function, input `./Blender.exe --background --python path/to/script.py` into your terminal (working on Git Bash, syntax for executing applications from the terminal may differ slightly between terminal clients).
    - This will render a DEM image to the absolute directory specified in your renderDEM() function WITHOUT opening Blender's GUI.
    - For more information on starting Blender from the command line see [here](https://docs.Blender.org/manual/en/dev/advanced/command_line/launch/index.html).

<br/>

### 🖥️ Render Map from Python Script Using GUI <a name = "gui"></a>
- While rendering from the terminal is quicker and more resource efficient, it may be simpler if you are not that familiar with the command line to render using Blender's GUI.


- **NOTE:** the renderDEM() function is intended to work on a **new** Blender project file that features the default cube, camera, and light. If you already have Blender open and have made any changes to your project, go to `File>New>General` to create a new project.


- Steps to render map using GUI:
    - When Blender starts, create a new project default by clicking the "General" template. Then, navigate to the "Scripting" workspace located at the far right along the top bar.
    ![alt text](https://docs.Blender.org/manual/en/latest/_images/interface_window-system_workspaces_screen.png "Blender workspace")
    - You should see a new workspace featuring a text editor and Blender's own python console. Along the top bar of the text editor click "Open Text" (folder icon).
    - Navigate to your python script (which imports module and calls the `renderDEM()` function) and open it.
    - Click the "Run Script" (play button icon) and the script should produce a rendered image according to the parameters specified in the renderDEM() function.
    - If you wish to make changes and run the script again, you must open a new project and repeat the previous steps. This is because the script is built around a new default project that is present each time the script is run from the terminal. (This is why it is recommended to render using the terminal (see above).

<br/>

### 💡 Usage Tips <a name = "tips"></a>
It is recommended to start with **very** conservative quality settings (`renderDEM()` arguments of `resolution_scale` and `samples`) so that you are able to quickly perform many test renders while you fine-tune the stylistic arguments before your final high-quality render. This is because different input maps may have better readability with certain scale exaggerations, colors, shadows, etc. and rendering a high-quality map every time to tweak these parameters would require an unnecessary amount of time and resources.


Use [latlong.net](https://www.latlong.net/) to help you find the north, south, east, and west bounds of your chosen area to use with the `fetchDEM()` function.

<br/>

## 🙌 Acknowledgements <a name = "acknowledgements"></a>
- This documentation was created with reference from the following template created by [@kylelobo](https://github.com/kylelobo), accessible [here](https://github.com/kylelobo/The-Documentation-Compendium/blob/master/en/README_TEMPLATES/Standard.md)