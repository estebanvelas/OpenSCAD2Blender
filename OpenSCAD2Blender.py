

import bpy
import os
import subprocess
import tempfile

bl_info = {
    "name": "OpenSCAD Generator",
    "blender": (3, 0, 0),
    "category": "Object",
    "version": (1, 0),
    "author": "Esteban Velasquez",
    "description": "Generate objects using OpenSCAD within Blender, and load OpenSCAD files into the Text Editor",
}

class OpenSCADGeneratorPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport sidebar"""
    bl_label = "OpenSCAD Generator"
    bl_idname = "OBJECT_PT_openscad_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "OpenSCAD"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Checkbox to switch to Text Editor after loading
        box = layout.box()
        row = box.row()
        row.label(text="On \"LOAD\" Behaviour Options:")
        row = box.row()
        row.prop(scene, "switch_to_text_editor", text=" TIMELINE Area to Text Editor ")
        # Checkbox to replace object name with file name
        row = box.row()
        row.prop(scene, "use_filename_as_object_name", text="File Name as Object Name")

        # Add a separator for visual grouping
        layout.separator()  # Add separator here

        # File selector for OpenSCAD files
        box = layout.box()
        row = box.row()
        row.label(text="OpenSCAD File:")
        row = box.row()
        row.prop(scene, "openscad_filepath", text="")
        # Button to load the OpenSCAD file into the Text Editor
        row = box.row()
        row.operator("object.load_openscad_file")

        # Add a separator for visual grouping
        layout.separator()  # Add separator here
        # Input field for object name
        box = layout.box()
        row = box.row()
        row.label(text="Object Name:")
        row = box.row()
        row.prop(scene, "openscad_object_name", text="")

        # Checkbox for overwrite option
        row = box.row()
        row.prop(scene, "overwrite_object", text="Overwrite Object if exists")

        # Button to generate the object from the Text Editor
        row = box.row()
        row.operator("object.generate_openscad_object")


class LoadOpenSCADFile(bpy.types.Operator):
    """Load an OpenSCAD file into the Text Editor"""
    bl_idname = "object.load_openscad_file"
    bl_label = "Load OpenSCAD File"

    def execute(self, context):
        filepath = context.scene.openscad_filepath
        switch_to_text_editor = context.scene.switch_to_text_editor
        use_filename_as_object_name = context.scene.use_filename_as_object_name

        if not os.path.exists(filepath):
            self.report({'ERROR'}, "File not found!")
            return {'CANCELLED'}

        try:
            with open(filepath, "r") as file:
                openscad_code = file.read()

            # Create a new text buffer in the Text Editor
            text_name = os.path.basename(filepath)
            text_buffer = bpy.data.texts.new(text_name)
            text_buffer.from_string(openscad_code)

            self.report({'INFO'}, f"Loaded: {filepath}")

            # If the checkbox is checked, replace the object name with the file name (without extension)
            if use_filename_as_object_name:
                file_name = os.path.splitext(text_name)[0]  # Remove file extension
                context.scene.openscad_object_name = file_name

            # Switch to the Text Editor if the checkbox is selected
            prevTextEditorFlag = False
            if switch_to_text_editor:
                timeline_area = None

                # Search for the TIMELINE area
                for window in context.window_manager.windows:
                    for area in window.screen.areas:
                        if area.type == 'TIMELINE':
                            timeline_area = area
                            break
                        elif area.type == 'DOPESHEET_EDITOR':
                            if area.spaces[0].mode == 'TIMELINE':
                                timeline_area = area
                                break
                        elif area.type == 'TEXT_EDITOR':
                            prevTextEditorFlag = True
                            break
                    if timeline_area:
                        break

                if prevTextEditorFlag:
                    self.report({'INFO'}, f"Text Editor Already visible.")
                elif timeline_area:
                    # Change the TIMELINE area to TEXT_EDITOR
                    timeline_area.type = 'TEXT_EDITOR'
                    # Set the newly created Text Editor's buffer
                    timeline_area.spaces.active.text = text_buffer

                    # Temporarily override the context to execute text operators
                    with context.temp_override(area=timeline_area):
                        bpy.ops.text.jump(line=1)
                        bpy.ops.text.move(type='LINE_BEGIN')
                else:
                    self.report({'ERROR'}, "No TIMELINE area found to switch to.")
                    return {'CANCELLED'}

        except Exception as e:
            self.report({'ERROR'}, f"Failed to load file: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}


class GenerateOpenSCADObject(bpy.types.Operator):
    """Generate an object using OpenSCAD code from the Text Editor"""
    bl_idname = "object.generate_openscad_object"
    bl_label = "Generate OpenSCAD Object"

    def execute(self, context):
        # Get the active text editor
        area = None
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'TEXT_EDITOR':
                    break
            if area and area.type == 'TEXT_EDITOR':
                break

        if not area or area.type != 'TEXT_EDITOR':
            self.report({'ERROR'}, "No active Text Editor found!")
            return {'CANCELLED'}

        # Get the active text buffer in the Text Editor
        space_data = area.spaces.active
        if not space_data or not space_data.text:
            self.report({'ERROR'}, "No active text buffer in the Text Editor!")
            return {'CANCELLED'}

        text_buffer = space_data.text
        openscad_code = text_buffer.as_string()

        if not openscad_code:
            self.report({'ERROR'}, "No OpenSCAD code in the active text buffer!")
            return {'CANCELLED'}

        # Get the object name and overwrite setting
        object_name = context.scene.openscad_object_name
        overwrite = context.scene.overwrite_object

        if not object_name:
            self.report({'ERROR'}, "Please provide an object name!")
            return {'CANCELLED'}

        # Check if the object already exists
        existing_object = bpy.data.objects.get(object_name)

        if existing_object:
            if overwrite:
                # Overwrite the object if 'Overwrite if exists' is checked
                bpy.data.objects.remove(existing_object)
            else:
                # If the object exists and overwrite is not selected, append a number
                i = 1
                new_object_name = f"{object_name}_{i}"
                while bpy.data.objects.get(new_object_name):
                    i += 1
                    new_object_name = f"{object_name}_{i}"
                object_name = new_object_name

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        scad_file = os.path.join(temp_dir, "temp.scad")
        stl_file = os.path.join(temp_dir, "temp.stl")

        try:
            # Write the OpenSCAD code to the temporary .scad file
            with open(scad_file, "w") as file:
                file.write(openscad_code)

            # Call OpenSCAD to generate the STL file
            subprocess.run([r"C:\Program Files\OpenSCAD\openscad.exe", "-o", f'{stl_file}', f'{scad_file}'], check=True, shell=True)

            # Ensure the 3D Viewport is active before importing the STL file
            bpy.context.view_layer.update()  # Ensure the context is up to date
            with bpy.context.temp_override(area=area):
                bpy.ops.import_mesh.stl(filepath=f'{stl_file}')

            # Rename the imported object to the user-defined name
            imported_object = bpy.context.view_layer.objects.active
            imported_object.name = object_name

        except subprocess.CalledProcessError as e:
            self.report({'ERROR'}, f"OpenSCAD failed: {e}")
            return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {e}")
            return {'CANCELLED'}
        finally:
            # Clean up temporary files
            if os.path.exists(scad_file):
                self.report({'INFO'}, f"Removing: {scad_file}")
                os.remove(scad_file)
            if os.path.exists(stl_file):
                self.report({'INFO'}, f"Removing: {stl_file}")
                os.remove(stl_file)
            os.rmdir(temp_dir)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OpenSCADGeneratorPanel)
    bpy.utils.register_class(LoadOpenSCADFile)
    bpy.utils.register_class(GenerateOpenSCADObject)
    bpy.types.Scene.openscad_filepath = bpy.props.StringProperty(
        name="OpenSCAD File",
        description="Path to the OpenSCAD file",
        subtype='FILE_PATH'
    )
    bpy.types.Scene.openscad_object_name = bpy.props.StringProperty(
        name="Object Name",
        description="Enter the desired name for the object"
    )
    bpy.types.Scene.overwrite_object = bpy.props.BoolProperty(
        name="Overwrite Object",
        description="Overwrite object with the same name if it exists",
        default=False
    )
    bpy.types.Scene.switch_to_text_editor = bpy.props.BoolProperty(
        name="Switch to Text Editor",
        description="Switch to the Text Editor after loading the file",
        default=False
    )
    bpy.types.Scene.use_filename_as_object_name = bpy.props.BoolProperty(
        name="Use File Name as Object Name",
        description="Replace the object name with the name of the loaded file",
        default=False
    )


def unregister():
    bpy.utils.unregister_class(OpenSCADGeneratorPanel)
    bpy.utils.unregister_class(LoadOpenSCADFile)
    bpy.utils.unregister_class(GenerateOpenSCADObject)
    del bpy.types.Scene.openscad_filepath
    del bpy.types.Scene.openscad_object_name
    del bpy.types.Scene.overwrite_object
    del bpy.types.Scene.switch_to_text_editor
    del bpy.types.Scene.use_filename_as_object_name


if __name__ == "__main__":
    register()