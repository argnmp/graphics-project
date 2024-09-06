from glfw.GLFW import *
import numpy as np
import glm

import globalvar

def key_callback(window, key, scancode, action, mods):
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    else:
        if action==GLFW_PRESS or action==GLFW_REPEAT:
            if key==GLFW_KEY_V:
                globalvar.project_state = not globalvar.project_state
                if globalvar.project_state:
                    globalvar.project_multiplier = 3
                    globalvar.g_ortho_zoom = 0
                else:
                    globalvar.project_multiplier = 0.1
                    globalvar.g_perspective_zoom = 0


def cursor_callback(window, xpos, ypos):
    x_delta = xpos - globalvar.g_prev_cursor[0]
    y_delta = ypos - globalvar.g_prev_cursor[1]
    if(globalvar.g_mouse_state == (GLFW_MOUSE_BUTTON_LEFT, GLFW_PRESS)):
        if(x_delta < 0):
            globalvar.g_cam_ang += np.radians(-x_delta*0.3)
        elif(x_delta > 0):
            globalvar.g_cam_ang += np.radians(-x_delta*0.3)
        if(y_delta < 0):
            globalvar.g_cam_ang_y += np.radians(-y_delta*0.3)
        elif(y_delta > 0):
            globalvar.g_cam_ang_y += np.radians(-y_delta*0.3)

    elif(globalvar.g_mouse_state == (GLFW_MOUSE_BUTTON_RIGHT, GLFW_PRESS)):
        if(x_delta < 0):
            globalvar.g_center.x += -x_delta/300 * np.sin(globalvar.g_cam_ang + np.pi/2)
            globalvar.g_center.z += -x_delta/300 * np.cos(globalvar.g_cam_ang + np.pi/2)
        elif(x_delta > 0):
            globalvar.g_center.x -= x_delta/300 * np.sin(globalvar.g_cam_ang + np.pi/2)
            globalvar.g_center.z -= x_delta/300 * np.cos(globalvar.g_cam_ang + np.pi/2)

        if(y_delta < 0):
            globalvar.g_center.y += y_delta/300
        elif(y_delta > 0):
            globalvar.g_center.y -= -y_delta/300
        
    globalvar.g_prev_cursor = (xpos, ypos)

def mouse_callback(window, button, action, mods):
    globalvar.g_mouse_state = (button, action)

def scroll_callback(window, xoffset, yoffset):
    if(globalvar.project_state):
        globalvar.g_perspective_zoom += yoffset/10
    else:
        globalvar.g_ortho_zoom += yoffset/100
    
    

            
