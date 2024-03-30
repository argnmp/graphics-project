from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np

import globalvar

from shader import *

class Node:
    def __init__(self, parent, vao, vertices_count, faces_count, shader_program, wireframe_permit):
        self.parent = parent
        self.children = []
        if parent is not None:
            parent.children.append(self)

        self.origin_transform = glm.mat4()
        self.static_transform = glm.mat4()
        self.local_transform = glm.mat4()
        self.global_transform = glm.mat4()
        self.vao = vao
        self.faces_count = faces_count
        self.vertices_count = vertices_count
        self.wireframe_permit = wireframe_permit
        self.color_properties = ([10, 10, 10], [1,1,1], [0.8, 0.8, 0.8], 32, False)
        self.refresh_func = None
        
        if vao != None:
            self.shader_program = shader_program
            self.mvp_loc = glGetUniformLocation(shader_program, 'MVP')
            self.m_loc = glGetUniformLocation(shader_program, 'M')
            self.view_pos_loc = glGetUniformLocation(shader_program, 'view_pos')
            self.set_color_properties([10,10,10], [1,1,1], [0,0,1], 32., False)
            light_pos_loc = glGetUniformLocation(self.shader_program, 'light_pos')
            light_color_loc = glGetUniformLocation(self.shader_program, 'light_color')
            material_color_loc = glGetUniformLocation(self.shader_program, 'material_color')
            material_shiness_loc = glGetUniformLocation(self.shader_program, 'material_shiness')
            light_rendering_mode_loc = glGetUniformLocation(self.shader_program, 'light_rendering_mode')
            self.color_properties_loc = (light_pos_loc, light_color_loc, material_color_loc, material_shiness_loc, light_rendering_mode_loc)
    
    def set_refresh_function(self, func):
        self.refresh_func = func

    def set_origin_transform(self, origin_transform):
        self.origin_transform = origin_transform  

    def set_static_transform(self, static_transform):
        self.static_transform = static_transform  

    def set_local_transform(self, local_transform):
        self.local_transform = local_transform
    def set_org_local_transform(self, local_transform):
        self.local_transform = glm.inverse(self.origin_transform)*local_transform*self.origin_transform

    def update_global_transform(self):
        if self.parent is not None:
            self.global_transform = self.parent.get_global_transform() * self.local_transform * self.static_transform
        else:
            self.global_transform = self.local_transform * self.static_transform

        for child in self.children:
            child.update_global_transform()

    def get_global_transform(self):
        return self.global_transform
    def get_local_transform(self):
        return self.local_transform

    def set_color_properties(self, light_pos, light_color, material_color, material_shiness, light_rendering_mode):
        self.color_properties = (light_pos, light_color, material_color, material_shiness, light_rendering_mode)
        for child in self.children:
            child.set_color_properties(light_pos, light_color, material_color, material_shiness, light_rendering_mode)

    def draw(self, draw_type, VP):
        if self.refresh_func != None:
            self.refresh_func()

        if self.vao == None:
            return

        M = self.global_transform #* self.static_transform
        MVP = VP * M 
        
        if self.wireframe_permit and globalvar.g_wireframe_mode:
            glUseProgram(globalvar.g_wireframe_shader) 
            glUniformMatrix4fv(globalvar.g_wireframe_mvp_loc, 1, GL_FALSE, glm.value_ptr(MVP))
        else:
            glUseProgram(self.shader_program) 
            glUniformMatrix4fv(self.mvp_loc, 1, GL_FALSE, glm.value_ptr(MVP))
            glUniformMatrix4fv(self.m_loc, 1, GL_FALSE, glm.value_ptr(M))
            glUniform3f(self.view_pos_loc, globalvar.g_view_pos.x, globalvar.g_view_pos.y, globalvar.g_view_pos.z)
            

            glUniform1i(self.color_properties_loc[4], 1 if self.color_properties[4] else 0)
            glUniform3f(self.color_properties_loc[0], self.color_properties[0][0], self.color_properties[0][1],self.color_properties[0][2])
            glUniform3f(self.color_properties_loc[1], self.color_properties[1][0],self.color_properties[1][1],self.color_properties[1][2])
            glUniform3f(self.color_properties_loc[2], self.color_properties[2][0],self.color_properties[2][1],self.color_properties[2][2])
            glUniform1f(self.color_properties_loc[3], self.color_properties[3])

        if self.faces_count == 0:
            glBindVertexArray(self.vao)
            glDrawArrays(draw_type, 0, self.vertices_count)
        else:
            glBindVertexArray(self.vao)
            glDrawElements(draw_type, self.faces_count * 3, GL_UNSIGNED_INT, None)

    def recursive_draw(self, draw_type, VP):
        self.draw(draw_type, VP)
        for child in self.children:
            child.draw(draw_type, VP)
        


def create_pv():
        ortho_size = (2-globalvar.g_ortho_zoom)
        P = glm.perspective(45, 1.5, 0.01, 50) if globalvar.project_state else glm.ortho(-(ortho_size*1.5),ortho_size*1.5,-ortho_size,ortho_size,-ortho_size,ortho_size)
        
        centerpoint = glm.vec3(
                globalvar.g_center.x,
                globalvar.g_center.y,
                globalvar.g_center.z
                )

        multiplier = 5
        view_pos = glm.vec3(
                multiplier * np.sin(globalvar.g_cam_ang_y)*np.sin(globalvar.g_cam_ang),
                multiplier * np.cos(globalvar.g_cam_ang_y) + globalvar.g_center.y,
                multiplier *np.sin(globalvar.g_cam_ang_y)*np.cos(globalvar.g_cam_ang), 
                )
        globalvar.g_view_pos = view_pos

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
        
        is_x_changed = 0 if (globalvar.g_ref_eyepoint_prev.x * ref_eyepoint.x == 0) else -1 if(globalvar.g_ref_eyepoint_prev.x * ref_eyepoint.x < 0) else 1
        is_x_changed += 1
        is_z_changed = 0 if (globalvar.g_ref_eyepoint_prev.z * ref_eyepoint.z == 0) else -1 if(globalvar.g_ref_eyepoint_prev.z * ref_eyepoint.z < 0) else 1
        is_z_changed += 1
        map = [
                [-1, -1, 1],
                [-1, 1, 1],
                [1, 1, 1],
                ]

        globalvar.g_up_direction =  globalvar.g_up_direction * map[is_x_changed][is_z_changed]
        V = glm.lookAt(eyepoint, centerpoint, glm.vec3(0,globalvar.g_up_direction,0))

        globalvar.g_ref_eyepoint_prev = ref_eyepoint
        
        A = np.array([
            [1.0, 0.0, 0.0, 0],
            [0.0, 1.0, 0.0, 0],
            [0.0, 0.0, 1.0, globalvar.g_perspective_zoom],
            [0.0, 0.0, 0.0, 1.0],
            ]).transpose()
        A = glm.mat4(*A.flatten())
        V = A*V

        return P*V

