from OpenGL.GL import *
from glfw.GLFW import *

from shader import *
from keyinput import *
from vao import *
import globalvar

def main():
    globalvar.initialize()

    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) 
    
    window = glfwCreateWindow(800, 800, 'project1_2019097210', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)
    
    glfwSetKeyCallback(window, key_callback)
    glfwSetCursorPosCallback(window, cursor_callback)
    glfwSetMouseButtonCallback(window, mouse_callback)
    glfwSetScrollCallback(window, scroll_callback)

    
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)

    
    MVP_loc = glGetUniformLocation(shader_program, 'MVP')
    
    
    vao_frame = prepare_vao_frame()
    vao_object = prepare_vao_object()
    (vao_ground, vao_ground_size) = prepare_vao_ground(100, 0.1, 0.25)

    

    up_direction = 1
    while not glfwWindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glUseProgram(shader_program)

        #this should be deleted
        glEnable(GL_PROGRAM_POINT_SIZE)
        
        
        ortho_size = (2-globalvar.g_ortho_zoom)
        P = glm.perspective(45, 1, 1, 10) if globalvar.project_state else glm.ortho(-ortho_size,ortho_size,-ortho_size,ortho_size,-ortho_size,ortho_size)
        
        centerpoint = glm.vec3(
                globalvar.g_center.x,
                globalvar.g_center.y,
                globalvar.g_center.z
                )

        eyepoint = glm.vec3(
                globalvar.project_multiplier * np.sin(globalvar.g_cam_ang_y)*np.sin(globalvar.g_cam_ang) + globalvar.g_center.x,
                globalvar.project_multiplier * np.cos(globalvar.g_cam_ang_y) + globalvar.g_center.y,
                globalvar.project_multiplier *np.sin(globalvar.g_cam_ang_y)*np.cos(globalvar.g_cam_ang) + globalvar.g_center.z, 
                )

        # for calculating up direction
        ref_eyepoint = glm.vec3(
                globalvar.project_multiplier * np.sin(globalvar.g_cam_ang_y)*np.sin(globalvar.g_cam_ang),
                globalvar.project_multiplier * np.cos(globalvar.g_cam_ang_y),
                globalvar.project_multiplier * np.sin(globalvar.g_cam_ang_y)*np.cos(globalvar.g_cam_ang), 
                )
        
        is_x_changed = 0 if (globalvar.g_eyepoint_prev.x * ref_eyepoint.x == 0) else -1 if(globalvar.g_eyepoint_prev.x * ref_eyepoint.x < 0) else 1
        is_x_changed += 1
        is_z_changed = 0 if (globalvar.g_eyepoint_prev.z * ref_eyepoint.z == 0) else -1 if(globalvar.g_eyepoint_prev.z * ref_eyepoint.z < 0) else 1
        is_z_changed += 1
        map = [
                [-1, -1, 1],
                [-1, 1, 1],
                [1, 1, 1],
                ]

        up_direction =  up_direction * map[is_x_changed][is_z_changed]
        V = glm.lookAt(eyepoint, centerpoint, glm.vec3(0,up_direction,0))

        globalvar.g_eyepoint_prev = ref_eyepoint


        
        M = glm.identity(glm.mat4)
        A = np.array([
            [1.0, 0.0, 0.0, 0],
            [0.0, 1.0, 0.0, 0],
            [0.0, 0.0, 1.0, globalvar.g_perspective_zoom],
            [0.0, 0.0, 0.0, 1.0],
            ]).transpose()
        A = glm.mat4(*A.flatten())
        V = A*V
        MVP = P*V*M
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
        
        # draw objects

        #  vao_point = prepare_vao_point(globalvar.g_center.x, globalvar.g_center.y, globalvar.g_center.z)
        #  glBindVertexArray(vao_point)
        #  glDrawArrays(GL_LINES, 0, 2)

        glBindVertexArray(vao_ground)
        glDrawArrays(GL_LINES, 0, vao_ground_size)

        glBindVertexArray(vao_object)
        glDrawArrays(GL_TRIANGLES, 0, 12)
        
        glBindVertexArray(vao_frame)
        glDrawArrays(GL_LINES, 0, 6)
        
        glfwSwapBuffers(window)
        
        glfwPollEvents()

    
    glfwTerminate()

if __name__ == "__main__":
    main()
