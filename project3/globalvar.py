import glm
import numpy as np

from draw import *
from keyinput import *

def initialize():

    global project_state
    project_state = True

    global project_multiplier
    project_multiplier = 3

    global g_cam_ang
    g_cam_ang = 0.
    global g_cam_ang_y
    g_cam_ang_y = 45.

    global g_up_direction
    g_up_direction = 1

    global g_center
    g_center = glm.vec3(0,0,0)
    global g_view_pos
    g_view_pos = glm.vec3(0,0,0)
    global g_ref_eyepoint_prev
    g_ref_eyepoint_prev = glm.vec3(0,0,0)

    global g_perspective_zoom
    g_perspective_zoom = -1

    global g_ortho_zoom
    g_ortho_zoom = 0

    global g_prev_cursor
    g_prev_cursor = (0, 0)
    
    global g_mouse_state
    g_mouse_state = (0, 0)
    
    # applied to Node
    global g_wireframe_mode
    g_wireframe_mode = False
    global g_wireframe_shader
    g_wireframe_shader = None
    global g_wireframe_mvp_loc
    g_wireframe_mvp_loc = None

    global g_bvh_offset_multiplier
    g_bvh_offset_multiplier = 1

    # applied to CNode
    # global g_line_rendering_mode
    # g_line_rendering_mode = True

    global g_box_rendering_mode
    g_box_rendering_mode = False


    global g_viewer_mode
    g_viewer_mode = True

    global g_time
    g_time = 0

    global main_obj
    main_obj = Node(None, None, 0, 0, None, True)
    
    global main_bvh
    main_bvh = CNode(None, "main_bvh", "main_bvh")
    global main_bvh_frames
    main_bvh_frames = 1
    global main_bvh_frame_time
    main_bvh_frame_time = 0

    global main_bvh_curframe
    main_bvh_curframe = -1
    global main_bvh_paused
    main_bvh_paused = True

