from OpenGL.GL import *
from glfw.GLFW import *

from shader import *
from keyinput import *
from vao import *
from draw import *
from objparser import *
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
    
    window = glfwCreateWindow(1200, 800, 'project2_2019097210', None, None)
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
    
    # obj_frame = Node(None, prepare_vao_frame(), 6, 0, shader_default, False)
    (vao_ground, vao_ground_size) = prepare_vao_ground(10, 0.1, 0.35)
    obj_ground = Node(None, vao_ground, vao_ground_size, 0, shader_default, False)

    obj_base = Node(None, None, 0, 0, shader_default, True)

    #scene
    earth_vaos = obj_multi_parser(os.path.join(".","obj","earth.obj"), 'o')
    tucano_vaos = obj_multi_parser(os.path.join(".","obj","tucano.obj"), 'g')
    drone_vaos = obj_multi_parser(os.path.join(".","obj","drone.obj"), 'o')
    balloon_vaos = obj_multi_parser(os.path.join(".","obj","balloon.obj"), 'o') 

    (obj_earth) = load_earth(obj_base, earth_vaos, glm.scale((0.2, 0.2, 0.2)))

    (obj_tucano1,obj_tucano1_prop,obj_tucano1_flapL,obj_tucano1_flapR, obj_tucano1_eleronL, obj_tucano1_eleronR) = load_tucano(obj_earth, tucano_vaos, glm.scale((0.3,0.3,0.3)))
    obj_tucano1.set_color_properties([10, 10, 10], [1,1,1], [0.7,0.7,1], 10, True)
    obj_tucano1_prop.set_color_properties([10,10,10], [1,1,1], [0.5, 0.5, 1], 10, True)
    obj_tucano1_flapL.set_color_properties([10,10,10], [1,1,1], [0.5, 0.5, 1], 10, True)
    obj_tucano1_flapR.set_color_properties([10,10,10], [1,1,1], [0.5, 0.5, 1], 10, True)
    obj_tucano1_eleronL.set_color_properties([10,10,10], [1,1,1], [0.4, 0.4, 1], 10, True)
    obj_tucano1_eleronR.set_color_properties([10,10,10], [1,1,1], [0.4, 0.4, 1], 10, True)

    (obj_drone1) = load_drone(obj_tucano1, drone_vaos, glm.translate((4,0,-5))*glm.scale((10,10,10)))
    (obj_drone2) = load_drone(obj_tucano1, drone_vaos, glm.translate((-4,0,-5))*glm.scale((10,10,10)))
    obj_drone1.set_color_properties([10, 10, 10], [1,1,1], [0.4, 0.4, 1], 10, True)
    obj_drone2.set_color_properties([10, 10, 10], [1,1,1], [0.4, 0.4, 0.9], 10, True)

    (obj_tucano2,obj_tucano2_prop,obj_tucano2_flapL,obj_tucano2_flapR, obj_tucano2_eleronL, obj_tucano2_eleronR) = load_tucano(obj_earth, tucano_vaos, glm.scale((0.3,0.3,-0.3)))
    obj_tucano2.set_color_properties([10, 10, 10], [1,1,1], [1,0.7,0.7], 10, True)
    obj_tucano2_prop.set_color_properties([10,10,10], [1,1,1], [1, 0.5, 0.5], 10, True)
    obj_tucano2_flapL.set_color_properties([10,10,10], [1,1,1], [1, 0.5, 0.5], 10, True)
    obj_tucano2_flapR.set_color_properties([10,10,10], [1,1,1], [1, 0.5, 0.5], 10, True)
    obj_tucano2_eleronL.set_color_properties([10,10,10], [1,1,1], [1, 0.4, 0.4], 10, True)
    obj_tucano2_eleronR.set_color_properties([10,10,10], [1,1,1], [1, 0.4, 0.4], 10, True)

    (obj_balloon) = load_balloon(obj_tucano2, balloon_vaos, glm.translate((0,2,-5))*glm.rotate(np.radians(90), (1,0,0))*glm.scale((10,-10,10)))

    (obj_drone3) = load_drone(obj_tucano2, drone_vaos, glm.translate((0,3,0))*glm.scale((10,10,10)))
    obj_drone3.set_color_properties([10, 10, 10], [1,1,1], [1, 0.4, 0.6], 50, True)
    

    timer = 0
    while not glfwWindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        if globalvar.g_wireframe_mode:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        
        VP = create_pv()

        obj_ground.draw(GL_LINES, VP)

        globalvar.g_time = glfwGetTime()
        if globalvar.g_viewer_mode:
            globalvar.main_obj.update_global_transform()
            globalvar.main_obj.recursive_draw(GL_TRIANGLES, VP);
        else:
            obj_base.update_global_transform()
            

            #scene2
            timer_multiplier = 1/((np.sin(globalvar.g_time)*10 + 11))
            timer += (0.02)*timer_multiplier
            obj_earth.set_local_transform(glm.rotate(globalvar.g_time*0.3, (0,1,0)))

            obj_tucano1.set_local_transform(glm.rotate(-(timer), (0, 1, 0))*glm.translate((8, 0, 0))*glm.rotate(np.sin(globalvar.g_time),(0,0,1)))
            obj_drone1.set_org_local_transform(glm.rotate(np.sin(globalvar.g_time*3), ((0,0,1))))
            obj_drone2.set_org_local_transform(glm.rotate(-np.sin(globalvar.g_time*3), ((0,0,1))))
            obj_tucano2.set_local_transform(glm.rotate(np.radians(60), (0,1,0))*glm.rotate(-(globalvar.g_time*0.5), (1,0,0))*glm.translate((0, 6, 0)))
            obj_balloon.set_org_local_transform(glm.rotate(np.sin(globalvar.g_time*10)*0.1, (1,0,0))*glm.rotate(globalvar.g_time*5, (0,1,0)))
            obj_drone3.set_org_local_transform(glm.translate((0,0,np.sin(globalvar.g_time)*0.3))*glm.rotate(np.sin(globalvar.g_time*1.3)*0.3, (1,0,0)))

            obj_earth.recursive_draw(GL_TRIANGLES, VP)
            obj_tucano1.recursive_draw(GL_TRIANGLES, VP)
            obj_tucano2.recursive_draw(GL_TRIANGLES, VP)
            obj_drone1.recursive_draw(GL_TRIANGLES, VP)
            obj_drone2.recursive_draw(GL_TRIANGLES, VP)
            obj_balloon.recursive_draw(GL_TRIANGLES, VP)
            obj_drone3.recursive_draw(GL_TRIANGLES, VP)
            
        
        glfwSwapBuffers(window)
        
        glfwPollEvents()

    
    glfwTerminate()

if __name__ == "__main__":
    main()
