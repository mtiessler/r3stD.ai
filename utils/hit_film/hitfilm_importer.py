
import math
import mathutils
import xml.etree.ElementTree as ET
from io_utils import axis_conversion

PixelsPerMM = 2.8352

def zoomToLens(lensZoomInPixels, compWidthInPixels):
    lensZoomInMM = lensZoomInPixels / PixelsPerMM
    compWidthInMM = compWidthInPixels / PixelsPerMM
    lens = (36.0 * lensZoomInMM) / compWidthInMM # 36mm is the default sensor size in Blender
    return lens

def calculateFOV(lensZoomInPixels, compHeightInPixels):
    lensZoomInMM = lensZoomInPixels / PixelsPerMM
    compHeightInMM = compHeightInPixels / PixelsPerMM

    fov = math.atan((compHeightInMM * 0.5) / lensZoomInMM) * 2.0
    print(math.degrees(fov))
    return fov

def import_hitfilm_composite(filepath):

    tree = ET.parse(filepath)
    root = tree.getroot()

    ### Global Scene Settings

    avSettingsNode = root.find(".//*AudioVideoSettings")
    width = int(avSettingsNode.find("Width").text)
    height = int(avSettingsNode.find("Height").text)
    frameRate = int(avSettingsNode.find("FrameRate").text)

    cameraNode = root.find(".//*CameraLayer")
    if cameraNode is None:
        print("Unable to find CameraLayer in Composite")
        return {'CANCELLED'}
    
    ### Import the Camera and Animation

    timeKeys = []
    camPositions = []
    camRotations = []
    camZoomVals = []

    cameraPosAnim = cameraNode.findall(".//*position/Animation")
    if len(cameraPosAnim) > 0:
        posKeys = list(cameraPosAnim[0])
        for key in posKeys:
            timeKeys.append(key.get('Time'))
            position = key.find('.//*FXPoint3_32f')
            camPositions.append( (float(position.get('X')), float(position.get('Y')), float(position.get('Z'))) )

    cameraRotationAnim = cameraNode.findall(".//*orientation/Animation")
    if len(cameraRotationAnim) > 0:
        rotationKeys = list(cameraRotationAnim[0])
        assert len(timeKeys) == len(rotationKeys) # Must match the timings already recorded for Position Data
        for key in rotationKeys:
            euler = key.find('.//*Orientation3D')
            camRotations.append( (float(euler.get('X')), float(euler.get('Y')), float(euler.get('Z'))) )

    cameraZoomAnim = cameraNode.findall(".//*zoom/Animation")
    if len(cameraZoomAnim) > 0:
        zoomKeys = list(cameraZoomAnim[0])
        assert len(timeKeys) == len(zoomKeys) # Must match the timings already recorded for Position Data
        for key in zoomKeys:
            zoom = key.find('Value/float').text
            camZoomVals.append(float(zoom))

    # Rescale to Blender coordinates 
    blenderScale = (1.0 / 1000.0) * PixelsPerMM # number of pixels per mm

    # Transform required for HF to Blender coordinate system
    mToZUp = axis_conversion(from_forward='Z', from_up='Y', to_forward='-Y', to_up='Z').to_4x4()

    # mToZUp = axis_conversion(from_forward='Z', from_up='Y', to_forward='-Y', to_up='Z').to_4x4()

    rot_mats = []

    for i in range(len(timeKeys)):
        
        # Zoom to Lens
        lens = zoomToLens(camZoomVals[i], width)
        
        # Rotation
        orientation = mathutils.Vector(camRotations[i]) 
        # Remember, orientations were inverted on export for HF, so invert again here for Blender.
        eul = mathutils.Euler(tuple([-math.radians(elem) for elem in orientation])) # Degrees to Radians xyz
        ##eul = mathutils.Euler((eul.z, eul.y, eul.x)) # XYZ to ZYX

      
        # Location
        location = mathutils.Vector(camPositions[i])
        location = tuple([blenderScale * elem for elem in location]) # Rescale to Blender units

        mat_rot = eul.to_matrix() # Rotation Matrix (3x3)
        mat_loc = mathutils.Matrix().Translation(location) # Translation Matrix (4x4)
        mat = mat_loc @ mat_rot.to_4x4() # World Transform

        matrix_world = mToZUp @ mat
        rot_mats.append(matrix_world)
    
    return camZoomVals[0], width, height, rot_mats

if __name__ == '__main__':
    import_hitfilm_composite(r"C:\Users\lopez\Desktop\hkupc-20220429T230959Z-001\hkupc\2022_04_30_0104561040.hfcs")