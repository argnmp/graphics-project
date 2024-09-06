from OpenGL.GL import *
from glfw.GLFW import *
import glm
import ctypes
import numpy as np

def prepare_vao_frame():
    vertices = glm.array(glm.float32,
         0.0, 0.0, 0.0,  1.0, 0.0, 0.0, 
         1.0, 0.0, 0.0,  1.0, 0.0, 0.0, 

         0.0, 0.0, 0.0,  0.0, 1.0, 0.0, 
         0.0, 1.0, 0.0,  0.0, 1.0, 0.0, 

         0.0, 0.0, 0.0,  0.0, 0.0, 1.0, 
         0.0, 0.0, 1.0,  0.0, 0.0, 1.0, 
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
    return VAO

def prepare_vao_ground(bound, unit, color):
    bound = abs(bound)
    unit = abs(unit)
    
    count = 0
    lines = []

    for i in np.arange(-bound, bound + unit, unit):
        lines.extend([-bound, 0.0,  i, color, color, color])    
        lines.extend([bound, 0.0, i, color, color, color])
        lines.extend([i, 0.0, -bound, color, color, color])
        lines.extend([i, 0.0, +bound, color, color, color])
        count += 4

    vertices = np.array(lines, dtype='float32')
    
    VAO = glGenVertexArrays(1)  
    glBindVertexArray(VAO)      

    
    VBO = glGenBuffers(1)   
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  

    
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ctypes.data_as(ctypes.c_void_p), GL_STATIC_DRAW) 

    
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)
    
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return (VAO, count) 
    

# no additional attributes
def vao_builder(vertices, faces):
    vertices = glm.array(glm.float32, *vertices.flatten())
    faces = glm.array(glm.uint32, *faces.flatten())

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces.ptr, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6*glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6*glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO
    
