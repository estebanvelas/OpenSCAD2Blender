# OpenSCAD Generator Blender Add-on

![Blender](https://img.shields.io/badge/Blender-3.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT%20with%20Attribution-blue)

The **OpenSCAD Generator** is a Blender add-on that allows you to generate 3D objects using OpenSCAD code directly within Blender. It provides a seamless workflow for loading OpenSCAD files, editing them in Blender's Text Editor, and generating 3D objects. You can also create a blank text file in the Text Editor, write OpenSCAD code, and generate objects without needing an external `.scad` file.

## Features

- **Load OpenSCAD Files**: Load `.scad` files into Blender's Text Editor.
- **Generate 3D Objects**: Convert OpenSCAD code into 3D objects in Blender.
- **Custom Object Naming**: Specify object names and overwrite existing objects.
- **Switch to Text Editor**: Automatically switch the TIMELINE area to the Text Editor after loading a file.
- **File Name as Object Name**: Optionally use the OpenSCAD file name as the object name.
- **Create Blank Text Files**: Write OpenSCAD code directly in Blender's Text Editor and generate objects.

## Installation

1. Download the `OpenSCAD2Blender.py` file from this repository.
2. Open Blender and go to `Edit > Preferences > Add-ons`.
3. Click `Install...` and select the `OpenSCAD2Blender.py` file.
4. Enable the add-on by searching for "OpenSCAD Generator" and checking the box.

## Usage

### Loading an OpenSCAD File
1. Open Blender and press `N` to open the sidebar in the 3D Viewport.
2. Go to the **OpenSCAD** tab in the sidebar.
3. **Load an OpenSCAD File**:
   - Click the `OpenSCAD File` field to select a `.scad` file.
   - Click the `Load OpenSCAD File` button to load the file into the Text Editor.

### Creating a Blank Text File
1. Open Blender's Text Editor (you can switch any area to the Text Editor by changing its type).
2. Create a new text file by clicking `New` in the Text Editor header.
3. Write your OpenSCAD code directly in the Text Editor.

### Generating a 3D Object
1. Enter a name for the object in the `Object Name` field.
2. Check the `Overwrite Object if exists` box if you want to replace an existing object with the same name.
3. Click the `Generate OpenSCAD Object` button to create the 3D object in Blender.

## Configuration

- **Switch to Text Editor**: Enable this option to automatically switch the TIMELINE area to the Text Editor after loading a file.
- **Use File Name as Object Name**: Enable this option to automatically set the object name to the name of the loaded OpenSCAD file (without the `.scad` extension).

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

1. Fork the repository. 
2. Create a new branch for your feature or bugfix. 
3. Commit your changes and push to the branch. 
4. Submit a pull request.

## License

This project is licensed under the **MIT License with Attribution**. You are free to use, modify, and distribute this software for personal and commercial purposes, provided you give proper credit to the original author.

```plaintext
MIT License

Copyright (c) 2025 Esteban Velasquez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

2. If the Software is used in a project, proper credit must be given to the original
   author (Esteban Velasquez) in the project's documentation, credits, or any other
   appropriate form of acknowledgment.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.