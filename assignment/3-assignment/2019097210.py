from OpenGL.GL import *
from glfw.GLFW import *
import glm

g_vertex_shader_src = '''
#version 330 core

// input vertex position. its attribute index is 0.
layout (location = 0) in vec3 vin_pos; 
layout (location = 1) in vec3 vin_color; 

out vec3 vout_color;

uniform float x_pos;

void main()
{
    gl_Position = vec4(vin_pos.x + x_pos, vin_pos.y, vin_pos.z, 1.0);
    vout_color = vec3(vin_color);
}
'''

g_fragment_shader_src = '''
#version 330 core

in vec3 vout_color;
out vec4 FragColor;
uniform float v_alpha_value;

void main()
{
    FragColor = vec4(vout_color.x + v_alpha_value, vout_color.y + v_alpha_value, vout_color.z + v_alpha_value, 0);
}
'''

def load_shaders(vertex_shader_source, fragment_shader_source):
    # build and compile our shader program
    # ------------------------------------
    
    # vertex shader 
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)    # create an empty shader object
    glShaderSource(vertex_shader, vertex_shader_source) # provide shader source code
    glCompileShader(vertex_shader)                      # compile the shader object
    
    # check for shader compile errors
    success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
    if (not success):
        infoLog = glGetShaderInfoLog(vertex_shader)
        print("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" + infoLog.decode())
        
    # fragment shader
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)    # create an empty shader object
    glShaderSource(fragment_shader, fragment_shader_source) # provide shader source code
    glCompileShader(fragment_shader)                        # compile the shader object
    
    # check for shader compile errors
    success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
    if (not success):
        infoLog = glGetShaderInfoLog(fragment_shader)
        print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" + infoLog.decode())

    # link shaders
    shader_program = glCreateProgram()               # create an empty program object
    glAttachShader(shader_program, vertex_shader)    # attach the shader objects to the program object
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)                    # link the program object

    # check for linking errors
    success = glGetProgramiv(shader_program, GL_LINK_STATUS)
    if (not success):
        infoLog = glGetProgramInfoLog(shader_program)
        print("ERROR::SHADER::PROGRAM::LINKING_FAILED\n" + infoLog.decode())
        
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program    # return the shader program


def key_callback(window, key, scancode, action, mods):
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);

def main():
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = glfwCreateWindow(800, 800, '2019097210', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    glfwSetKeyCallback(window, key_callback);

    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)
    x_pos_loc = glGetUniformLocation(shader_program, 'x_pos') # find uniform's location
    v_alpha_value_loc = glGetUniformLocation(shader_program, 'v_alpha_value') # find uniform's location
    

    vertices = glm.array(glm.float32,
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
         0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
         0.0,  0.5, 0.0,  0.0, 0.0, 1.0,
    )

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)

    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    while not glfwWindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program)
        t = glfwGetTime()
        alpha = glm.cos(t)*.5 - .5
        glUniform1f(v_alpha_value_loc, alpha)
        x_value = glm.sin(t) * .5
        glUniform1f(x_pos_loc, x_value)
        
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfwSwapBuffers(window)

        glfwPollEvents()

    glfwTerminate()

if __name__ == "__main__":
    main()
