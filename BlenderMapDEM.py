# Import required packages

# Fetch DEM of user specified extent
def fetchDEM(upper_lat, lower_lat, left_lon, right_lon, output_dir, filename = 'DEM.tif'):
    # Create a bounding box for the DEM extent coordinates
    bbox = {'lonLower':left_lon,'latLower':lower_lat,'lonHigher':right_lon,'latHigher':upper_lat}
    
    # Search database for DEM

# Fetch satellite imagery of user specified extent
def fetchImagery(upper_lat,lower_lat,left_lon,right_lon, output_dir, filename = 'imagery.tif'):

# Simplify DEM to a lower resolution
def simplifyDEM(dem):

# Plots 2D DEM visualization 
def plotDEM(dem)

# Generate 3D elevation map using Blender
def renderDEM(output_dir, exaggeration = 0.3, resolution_scale = 100, samples = 20):
     
    # Set variables to hold resolution of DEM image
    width = 2000
    height = 2800
    
    #width, height = bpy.data.images['myImage'].size
    
        ### --- Render Settings --- ###
    
    # Set render engine to "Cycles" and select "Experimental" feature set
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
    
    # Set render output resolution to the same as DEM image
    bpy.data.scenes["Scene"].render.resolution_x = width
    bpy.data.scenes["Scene"].render.resolution_y = height
    
    # Specify render quality
    bpy.data.scenes["Scene"].render.resolution_percentage = resolution_scale
    bpy.data.scenes["Scene"].cycles.samples = samples
    
        ### --- Plane Settings --- ###
    
    # Select and delete the default cube
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete() 

    # Add plane to scene
    bpy.ops.mesh.primitive_plane_add()
    
    plane = bpy.data.objects['Plane']

    # Scale plane to aspect ratio of image
    plane.scale[0] = width/1000
    plane.scale[1] = height/1000

    # Add subdivision surface modifier to plane
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].subdivision_type = 'SIMPLE'
    bpy.context.object.cycles.use_adaptive_subdivision = True
    
        ### --- Camera Settings --- ###
    
    camera = bpy.data.objects["Camera"]
    
    # Set camera location to origin
    camera.location[0] = 0
    camera.location[1] = 0
    camera.location[2] = 3
    
    # Set camera rotation to point down
    camera.rotation_euler[0] = 0
    camera.rotation_euler[1] = 0
    camera.rotation_euler[2] = 0
    
    # Set camera to orthographic
    bpy.data.cameras["Camera"].type = 'ORTHO'
    
    # Set orthographic scale to be twice the largest dimension of our plane (so plane fills view)
    if width/1000 > height/1000:
        orthographic_scale = 2*(width/1000)
    elif height/1000 > width/1000:
        orthographic_scale = 2*(height/1000)
    
    bpy.data.cameras["Camera"].ortho_scale = orthographic_scale
    
        ### --- Light Settings --- ###
    
    light = bpy.data.objects["Light"]
    
    # Select light and change its type to "Sun"
    bpy.data.lights["Light"].type = 'SUN'
    
    # Change strength and hardness of light
    bpy.data.lights["Light"].energy = 5
    bpy.data.lights["Light"].angle = 1.5708
    
    # Change direction of the light
    light.rotation_euler[0] = 0
    light.rotation_euler[1] = 0.785398
    light.rotation_euler[2] = 2.35619
    
        ### --- Shader Settings --- ###

    mat = bpy.data.materials["Material"]
    
    # Add new material to plane
    bpy.data.objects['Plane'].active_material = mat
    bpy.context.object.active_material.cycles.displacement_method = 'DISPLACEMENT'
    
    # Set material color and change "Roughness" to 1 and "Specular" to 0 (makes material matte)
    mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.6, 0.6, 0.6, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs['Roughness'].default_value = 1
    mat.node_tree.nodes["Principled BSDF"].inputs['Specular'].default_value = 0
    
    # Add image texture node and set its extrapolation mode to "Extend"
    #"C:\\Users\\sebas\\OneDrive\\Desktop\\Test Blender Map\\Blender Demo DEM.tif"
    mat.node_tree.nodes.new('ShaderNodeTexImage')
    mat.node_tree.nodes["Image Texture"].extension = 'EXTEND'

    # Add displacement node and specify the elevation exaggeration of heightmap
    mat.node_tree.nodes.new('ShaderNodeDisplacement')
    mat.node_tree.nodes["Displacement"].inputs['Scale'].default_value = exaggeration
    
    # Add color ramp node
    mat.node_tree.nodes.new('ShaderNodeValToRGB')
    
    ### --- Render Image --- ###
    
    # Set the output file path and format
    bpy.context.scene.render.filepath = output_dir
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    
    # Render the image
    bpy.ops.render.render(write_still=True)
