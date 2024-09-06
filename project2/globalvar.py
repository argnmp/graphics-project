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
    g_perspective_zoom = 0

    global g_ortho_zoom
    g_ortho_zoom = 0

    global g_prev_cursor
    g_prev_cursor = (0, 0)
    
    global g_mouse_state
    g_mouse_state = (0, 0)
    
    global g_wireframe_mode
    g_wireframe_mode = False
    global g_wireframe_shader
    g_wireframe_shader = None
    global g_wireframe_mvp_loc
    g_wireframe_mvp_loc = None

    global g_viewer_mode
    g_viewer_mode = True

    global g_time
    g_time = 0

    global main_obj
    main_obj = Node(None, None, 0, 0, None, True)

    # global light_pos_set
    # light_pos_set = np.array([[-10, 10, -10], [10, 10, -10], [-10, 10, 10],[10, 10, 10],[-10, -10, -10],[10, -10, -10],[-10, -10, 10],[10, -10, 10]]);
    # glUniform3fv(self.temp,24, globalvar.light_pos_set)

    
