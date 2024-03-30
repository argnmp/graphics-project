import glm
import numpy as np
def initialize():

    global project_state
    project_state = True

    global project_multiplier
    project_multiplier = 3

    global g_cam_ang
    g_cam_ang = 0.
    global g_cam_ang_y
    g_cam_ang_y = 45.

    global g_center
    g_center = glm.vec3(0,0,0)
    global g_eyepoint_prev
    g_eyepoint_prev = glm.vec3(0,0,0)

    global g_perspective_zoom
    g_perspective_zoom = 0

    global g_ortho_zoom
    g_ortho_zoom = 0

    global g_prev_cursor
    g_prev_cursor = (0, 0)
    
    global g_mouse_state
    g_mouse_state = (0, 0)
    
