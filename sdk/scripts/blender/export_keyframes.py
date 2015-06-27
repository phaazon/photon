#############################################################################
##
## Copyright   : (C) 2015 Dimitri Sabadie
## License     : BSD3
##
## Maintainer  : Dimitri Sabadie <dimitri.sabadie@gmail.com>
##
############################################################################

bl_info = {
    "name"     : "Export keyframes to Quaazar JSON (.qkfr)"
  , "author"   : "Dimitri Sabadie"
  , "category" : "Import-Export"
  , "location" : "File > Import-Export"
}

import bpy
import mathutils
from bpy_extras.io_utils import ExportHelper
from bpy.props import BoolProperty
from math import pi
import json

# Dump digits after the 6th one in order to make output less heavy.
def round_(x):
  return round(x,6)

class QuaazarKeyframesExporter(bpy.types.Operator, ExportHelper):
  """Quaazar Keyframes Exporter Script"""
  bl_idname      = "object.quaazar_keyframes_exporter"
  bl_label       = "Quaazar Keyframes Exporter"
  bl_description = "Export all keyframes from the scene"
  bl_options     = {'REGISTER'}

  filename_ext   = ".qkfr"

  sparse = BoolProperty (
      name        = "Sparse output"
    , description = "Should the output file be sparse?"
    , default     = False
    , )

  def execute(self, context):
    actions = bpy.data.actions
    for action in actions:
      co = (0,0,0) # origin is the default
      orient = (0,0,0,-1) # -Z axis is the default
      scale = (1,1,1) # identity scale
      print ("exporting action " + action.name)

      # Check whether we only have LocRotScale group
      if not action.groups['LocRotScale'] or len(action.groups) != 1:
        self.report({'ERROR'}, action.name + " should only have LocRotScale")
        return {}

      # Check that we have 10 channels
      #   · location x
      #   · location y
      #   · location z
      #   · orientation x
      #   · orientation y
      #   · orientation z
      #   · orientation w
      #   · scale x
      #   · scale y
      #   · scale z
      channels = action.groups['LocRotScale'].channels
      if len(channels) != 10:
        self.report({'ERROR'}, action.name + " doesn’t have enough channels")
        return {}

      # Get the curves and the keyframe points.
      locXCurve = channels[0]
      locYCurve = channels[1]
      locZCurve = channels[2]
      rotWCurve = channels[3]
      rotXCurve = channels[4]
      rotYCurve = channels[5]
      rotZCurve = channels[6]
      scaXCurve = channels[7]
      scaYCurve = channels[8]
      scaZCurve = channels[9]
      locXKeys = locXCurve.keyframe_points
      locYKeys = locYCurve.keyframe_points
      locZKeys = locZCurve.keyframe_points
      rotWKeys = rotWCurve.keyframe_points
      rotXKeys = rotXCurve.keyframe_points
      rotYKeys = rotYCurve.keyframe_points
      rotZKeys = rotZCurve.keyframe_points
      scaXKeys = scaXCurve.keyframe_points
      scaYKeys = scaYCurve.keyframe_points
      scaZKeys = scaZCurve.keyframe_points

      # Shrink the location curves into a single curves


    return {'FINISHED'}

def register():
  bpy.utils.register_class(QuaazarKeyframesExporter)

def unregister():
  bpy.utils.unregister_class(QuaazarKeyframesExporter)

if __name__ == "__main__":
  register()
