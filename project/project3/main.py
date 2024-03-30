from OpenGL.GL import *
from glfw.GLFW import *

from shader import *
from keyinput import *
from vao import *
from draw import *
from objparser import *
from bvhparser import *
from sample import *
import globalvar

def main():
    globalvar.initialize()

    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) 
    
    window = glfwCreateWindow(1200, 800, 'project3_2019097210', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)
    
    # initializae data
    globalvar.g_prev_cursor = glfwGetCursorPos(window)
    wireframe_shader = load_shaders(g_vertex_shader_src, g_fragment_wireframe_shader_src)
    globalvar.g_wireframe_shader = wireframe_shader
    globalvar.g_wireframe_mvp_loc = glGetUniformLocation(wireframe_shader, 'MVP')

    # input callbacks
    glfwSetKeyCallback(window, key_callback)
    glfwSetCursorPosCallback(window, cursor_callback)
    glfwSetMouseButtonCallback(window, mouse_callback)
    glfwSetScrollCallback(window, scroll_callback)
    glfwSetDropCallback(window, drop_callback)

    shader_default = load_shaders(g_vertex_shader_src, g_fragment_shader_src)
    
    (vao_ground, vao_ground_size) = prepare_vao_ground(10, 0.1, 0.35)
    obj_ground = Node(None, vao_ground, vao_ground_size, 0, shader_default, False)

    # scene rendering
    # obj_base = Node(None, None, 0, 0, shader_default, True)
    # scene1 = Scene(obj_base);

    # (root, frames, frame_time) = bvh_parser('/Users/tyler/workspace/cse4020/project/project3/bvh/sample-walk.bvh');
    
    base_time = 0
    while not glfwWindowShouldClose(window):
        t = glfwGetTime()
        
        if not globalvar.main_bvh_paused:
            if(t - base_time >= globalvar.main_bvh_frame_time):
                base_time = t
                globalvar.main_bvh_curframe = (globalvar.main_bvh_curframe+1) % globalvar.main_bvh_frames

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        if globalvar.g_wireframe_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        
        VP = create_pv()

        obj_ground.draw(GL_LINES, VP)

        # globalvar.g_time = glfwGetTime()
        # if globalvar.g_viewer_mode:
        #     globalvar.main_obj.update_global_transform()
        #     globalvar.main_obj.recursive_draw(GL_TRIANGLES, VP);
        # else:
        #     obj_base.update_global_transform()
        #     scene1.render(VP)
            
        globalvar.main_bvh.update_global_transform(globalvar.main_bvh_curframe)

        globalvar.main_bvh.recursive_draw(GL_LINES, VP)
        
        glfwSwapBuffers(window)
        
        glfwPollEvents()

    
    glfwTerminate()

if __name__ == "__main__":
    main()
