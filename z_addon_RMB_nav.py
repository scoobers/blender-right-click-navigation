bl_info = {
			"name": "Right-Click Navigation",
			"author": "Dr. Butts",
			"version": (0, 1),
			"blender": (2, 80, 0),
			"location": "",
			"description": "Navigate editors using the right mouse button",
			"warning": "",
			"tracker_url": "",
			"category": ""
}

import bpy, os, threading, time

# Blender has trouble assigning custom modal hotkeys,
# because it can take a while to load its own keymaps on startup.
# This script comes with a built-in delay, to help solve this:

delaySeconds = 1
# ^ time to wait, in seconds


def start_delay():
	thread = threading.Thread(target=keymapNav)
	thread.start()

def kmi_props_setattr(kmi_props, attr, value):
	try:
		setattr(kmi_props, attr, value)
	except AttributeError:
		print("Warning: property '%s' not found in keymap item '%s'" %
			(attr, kmi_props.__class__.__name__))
	except Exception as e:
		print("Warning: %r" % e)

def keymapNav():
	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon

	# wait for all keymaps to be loaded
	time.sleep(delaySeconds)

	m_select = 'LEFTMOUSE'
	m_nav = 'RIGHTMOUSE'
	m_nav_tweak = 'EVT_TWEAK_R'
	m_context = 'RIGHTMOUSE'
	m_secondary = 'MIDDLEMOUSE'
	m_secondary_tweak = 'EVT_TWEAK_M'
	m_cursor = 'RIGHTMOUSE'

	cM = "wm.call_menu"
	cP = "wm.call_panel"

	def context0(menuName):
		kmi = km.keymap_items.new(menuName, m_context, 'PRESS', alt=True)
		return kmi


	def context1(propName):
		kmi = km.keymap_items.new("wm.call_menu", m_context, 'PRESS', alt=True).properties.name=propName
		return kmi


	def context2(propName, propProp, propValue):
		kmi = km.keymap_items.new("wm.call_panel", m_context, 'PRESS', alt=True)
		kmi_props_setattr(kmi.properties, "name", propName)
		kmi_props_setattr(kmi.properties, propProp, propValue)
		return kmi


	def viewNav3D():
		kmi = km.keymap_items.new('view3d.rotate', m_nav, 'PRESS')
		kmi_props_setattr(kmi.properties, 'use_mouse_init', True) # or try 'Mouse Init'
		kmi = km.keymap_items.new('view3d.move', m_nav, 'PRESS', shift=True)
		kmi = km.keymap_items.new('view3d.zoom', m_nav, 'PRESS', ctrl=True)
		kmi = km.keymap_items.new('view3d.dolly', m_nav, 'PRESS', shift=True, ctrl=True)
		kmi = km.keymap_items.new('view3d.view_center_pick', m_nav, 'PRESS', shift=True, alt=True)

		# tweak stuff
		kmi = km.keymap_items.new('view3d.view_axis', m_nav_tweak, 'NORTH', shift=True, alt=True)
		kmi_props_setattr(kmi.properties, "type", 'TOP')
		kmi_props_setattr(kmi.properties, "relative", True)

		kmi = km.keymap_items.new('view3d.view_axis', m_nav_tweak, 'SOUTH', shift=True, alt=True)
		kmi_props_setattr(kmi.properties, "type", 'BOTTOM')
		kmi_props_setattr(kmi.properties, "relative", True)

		kmi = km.keymap_items.new('view3d.view_axis', m_nav_tweak, 'EAST', shift=True, alt=True)
		kmi_props_setattr(kmi.properties, "type", 'RIGHT')
		kmi_props_setattr(kmi.properties, "relative", True)

		kmi = km.keymap_items.new('view3d.view_axis', m_nav_tweak, 'WEST', shift=True, alt=True)
		kmi_props_setattr(kmi.properties, "type", 'LEFT')
		kmi_props_setattr(kmi.properties, "relative", True)


	def viewNav2D():
		kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS')
		kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS', shift=True)
		kmi = km.keymap_items.new('view2d.zoom', m_nav, 'PRESS', ctrl=True)
		kmi = km.keymap_items.new('image.view_pan', m_nav, 'PRESS')
		kmi = km.keymap_items.new('image.view_pan', m_nav, 'PRESS', shift=True)
		kmi = km.keymap_items.new('image.view_zoom', m_nav, 'PRESS', ctrl=True)


	def viewNav2D_subset():
		kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS', shift=True)
		kmi = km.keymap_items.new('view2d.zoom', m_nav, 'PRESS', ctrl=True)
		kmi = km.keymap_items.new('image.view_pan', m_nav, 'PRESS', shift=True)
		kmi = km.keymap_items.new('image.view_zoom', m_nav, 'PRESS', ctrl=True)


	def brushStencilControl():
	# remap stencil controls for sculpt / image paint modes
		kmi = km.keymap_items.new('brush.stencil_control', m_secondary, 'PRESS')
		kmi_props_setattr(kmi.properties, "mode", 'TRANSLATION')
		kmi = km.keymap_items.new('brush.stencil_control', m_secondary, 'PRESS', shift=True)
		kmi_props_setattr(kmi.properties, "mode", 'SCALE')
		kmi = km.keymap_items.new('brush.stencil_control', m_secondary, 'PRESS', ctrl=True)
		kmi_props_setattr(kmi.properties, "mode", 'ROTATION')



############################################
# Screen
############################################
	km = kc.keymaps.new('Screen', space_type='EMPTY', region_type='WINDOW', modal=False)



############################################
# Screen Editing
############################################
	km = kc.keymaps.new('Screen Editing', space_type='EMPTY', region_type='WINDOW', modal=False)

#context menu
	context0("screen.area_options")


############################################
# Region Context Menu
############################################
	km = kc.keymaps.new('Region Context Menu', space_type='EMPTY', region_type='WINDOW', modal=False)

#context menu
	context0("screen.region_context_menu")


############################################
# Window
############################################
	km = kc.keymaps.new('Window', space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav3D()


###################################
# Object Non-modal
###################################
	km = kc.keymaps.new('Object Non-modal', space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav3D()



############################################
# Image
############################################
	km = kc.keymaps.new('Image', space_type='IMAGE_EDITOR', region_type='WINDOW', modal=False)

	viewNav2D()

#secondary stuff
	kmi = km.keymap_items.new('image.sample', m_secondary, 'PRESS')
	kmi = km.keymap_items.new('image.curves_point_set', m_secondary, 'PRESS', ctrl=True)
	kmi_props_setattr(kmi.properties, "point", 'BLACK_POINT')
	kmi = km.keymap_items.new('image.curves_point_set', m_secondary, 'PRESS', shift=True)
	kmi_props_setattr(kmi.properties, "point", 'WHITE_POINT')



############################################
# Image Paint
############################################
	km = kc.keymaps.new('Image Paint', space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav2D()

	context2("VIEW3D_PT_paint_texture_context_menu", "keep_open", True)

#secondary stuff
	brushStencilControl()

	kmi = km.keymap_items.new('paint.grab_clone', m_secondary, 'PRESS')



############################################
# Vertex Paint
############################################
	km = kc.keymaps.new('Vertex Paint', space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav3D()

	context2("VIEW3D_PT_paint_vertex_context_menu", "keep_open", True)

#secondary stuff
	brushStencilControl()



############################################
# Weight Paint
############################################
	km = kc.keymaps.new('Weight Paint', space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav3D()

	context2("VIEW3D_PT_paint_weight_context_menu", "keep_open", True)

#secondary stuff
	kmi = km.keymap_items.new('paint.weight_sample', m_secondary, 'PRESS', ctrl=True)
	kmi = km.keymap_items.new('paint.weight_sample_group', m_secondary, 'PRESS', shift=True)




############################################
# Sequencer
############################################
	km = kc.keymaps.new('Sequencer', space_type='SEQUENCE_EDITOR', region_type='WINDOW', modal=False)

	#viewNav2D()
	kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS')

	context1("SEQUENCER_MT_context_menu")


############################################
# SequencerPreview
############################################
	km = kc.keymaps.new('SequencerPreview', space_type='SEQUENCE_EDITOR', region_type='WINDOW', modal=False)

	viewNav2D()

#secondary stuff
	context0("sequencer.sample")


############################################
# Clip Editor
############################################
	km = kc.keymaps.new('Clip Editor', space_type='CLIP_EDITOR', region_type='WINDOW', modal=False)

	#viewNav2D()

	context1("CLIP_MT_tracking_context_menu")
	kmi = km.keymap_items.new('clip.view_pan', m_nav, 'PRESS')
	kmi = km.keymap_items.new('clip.view_zoom', m_nav, 'PRESS', ctrl=True)

#cursor set
	kmi = km.keymap_items.new('clip.cursor_set', m_nav, 'PRESS', shift=True)

#secondary stuff
	kmi = km.keymap_items.new('clip.slide_plane_marker', m_secondary, 'PRESS')


############################################
# Clip Graph Editor
############################################
	km = kc.keymaps.new('Clip Graph Editor', space_type='CLIP_EDITOR', region_type='WINDOW', modal=False)

	#viewNav2D_subset()

	kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS')
	kmi = km.keymap_items.new('view2d.zoom', m_nav, 'PRESS', ctrl=True)


#secondary stuff
	#kmi = km.keymap_items.new('clip.change_frame', m_nav, 'PRESS', shift=True)


############################################
# Clip Dopesheet Editor
############################################
	km = kc.keymaps.new('Clip Dopesheet Editor', space_type='CLIP_EDITOR', region_type='WINDOW', modal=False)




############################################
# Node Editor
############################################
	km = kc.keymaps.new('Node Editor', space_type='NODE_EDITOR', region_type='WINDOW', modal=False)

	#viewNav2D()

	kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS')
	#kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS', shift=True)
	#kmi = km.keymap_items.new('view2d.zoom', m_nav, 'PRESS', ctrl=True)

	context1("NODE_MT_context_menu")


############################################
# NLA Channels
############################################
	km = kc.keymaps.new('NLA Channels', space_type='NLA_EDITOR', region_type='WINDOW', modal=False)

	viewNav2D_subset()

	context1("NLA_MT_channel_context_menu")


############################################
# NLA Editor
############################################
	km = kc.keymaps.new('NLA Editor', space_type='NLA_EDITOR', region_type='WINDOW', modal=False)

	#viewNav2D()
	kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS')

	context1("NLA_MT_context_menu")



############################################
# View2D
############################################
	km = kc.keymaps.new('View2D', space_type='EMPTY', region_type='WINDOW', modal=False)

	#IMPORTANT - don't use Shift+RMB shortcuts here, because they override the "go to frame" op
	#viewNav2D_subset()

	#kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS')
	kmi = km.keymap_items.new('view2d.zoom', m_nav, 'PRESS', ctrl=True)



############################################
# View2D Buttons List
############################################
# properties panel rollout content areas, etc
	km = kc.keymaps.new('View2D Buttons List', space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav2D_subset()



############################################
# Animation
############################################
	km = kc.keymaps.new('Animation', space_type='EMPTY', region_type='WINDOW', modal=False)



############################################
# Animation Channels
############################################
	km = kc.keymaps.new(name='Animation Channels')

	viewNav2D_subset()

	context1("DOPESHEET_MT_channel_context_menu")


############################################
# Dopesheet
############################################
	km = kc.keymaps.new('Dopesheet', space_type='DOPESHEET_EDITOR', region_type='WINDOW', modal=False)

	context1("DOPESHEET_MT_channel_context_menu")

# manually reassign pan, since Shift+RMB is reserved for moving to selected frame
	kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS')


############################################
# Graph Editor
############################################
	km = kc.keymaps.new('Graph Editor', space_type='GRAPH_EDITOR', region_type='WINDOW', modal=False)

	#viewNav2D()
	kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS')

	context1("GRAPH_MT_context_menu")



############################################
# File Browser
############################################
	km = kc.keymaps.new('File Browser', space_type='FILE_BROWSER', region_type='WINDOW', modal=False)

	#viewNav2D()
	kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS')



############################################
# Property Editor
############################################
	km = kc.keymaps.new('Property Editor', space_type='PROPERTIES', region_type='WINDOW', modal=False)

	context0("buttons.context_menu")


############################################
# Console
############################################
	km = kc.keymaps.new('File Browser', space_type='CONSOLE', region_type='WINDOW', modal=False)



############################################
# Info
############################################
	km = kc.keymaps.new('Info', space_type='INFO', region_type='WINDOW', modal=False)

	viewNav2D()



############################################
# UV Editor
############################################
	km = kc.keymaps.new('UV Editor', space_type='EMPTY', region_type='WINDOW', modal=False)

	#viewNav2D()
	kmi = km.keymap_items.new('image.view_pan', m_nav, 'PRESS')
	kmi = km.keymap_items.new('image.view_pan', m_nav, 'PRESS', shift=True)
	kmi = km.keymap_items.new('image.view_zoom', m_nav, 'PRESS', ctrl=True)

	#kmi = km.keymap_items.new('uv.select_lasso', m_nav_tweak, 'ANY', ctrl=True)
	#kmi_props_setattr(kmi.properties, 'extend', True)
	#kmi = km.keymap_items.new('uv.select_lasso', m_nav_tweak, 'ANY', ctrl=True, shift=True)
	#kmi_props_setattr(kmi.properties, 'deselect', True)

	context1("IMAGE_MT_uvs_context_menu")

# cursor
	kmi = km.keymap_items.new('uv.cursor_set', m_cursor, 'PRESS', ctrl=True, alt=True, shift=True)


############################################
# 3D View
############################################
	km = kc.keymaps.new('3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)

	viewNav3D()
	brushStencilControl() # apparently these hotkeys need to go in either 3D View or Mesh

# cursor
	kmi = km.keymap_items.new('view3d.cursor3d', m_cursor, 'PRESS', ctrl=True, alt=True, shift=True)


############################################
# Object Mode
############################################
	km = kc.keymaps.new(name='Object Mode')

	viewNav3D()

# context menu
	context1("VIEW3D_MT_object_context_menu")



############################################
# Sculpt
############################################
	km = kc.keymaps.new(name='Sculpt')

	viewNav3D()

	context2("VIEW3D_PT_sculpt_context_menu", "keep_open", True)

#secondary stuff
	brushStencilControl()



############################################
# Mesh
############################################
	km = kc.keymaps.new(name='Mesh')

	viewNav3D()
	brushStencilControl() # apparently these hotkeys need to go in either 3D View or Mesh

# context menu
	context1("VIEW3D_MT_edit_mesh_context_menu")

#secondary stuff
	kmi = km.keymap_items.new('mesh.dupli_extrude_cursor', m_secondary, 'PRESS', ctrl=True)
	kmi_props_setattr(kmi.properties, "rotate_source", True)
	kmi = km.keymap_items.new('mesh.dupli_extrude_cursor', m_secondary, 'PRESS', ctrl=True, shift=True)
	kmi_props_setattr(kmi.properties, "rotate_source", False)




############################################
# Armature
############################################
	km = kc.keymaps.new(name='Armature')

	context1("VIEW3D_MT_armature_context_menu")

#secondary stuff
	kmi = km.keymap_items.new('armature.click_extrude', m_secondary, 'PRESS', ctrl=True)


############################################
# Metaball
############################################
	km = kc.keymaps.new(name='Metaball')

	context1("VIEW3D_MT_edit_metaball_context_menu")


############################################
# Lattice
############################################
	km = kc.keymaps.new(name='Lattice')

	context1("VIEW3D_MT_edit_lattice_context_menu")


############################################
# Particle
############################################
	km = kc.keymaps.new(name='Particle')

	context1("VIEW3D_MT_particle_context_menu")


############################################
# Font (3D font object)
############################################
	km = kc.keymaps.new(name='Font')

	context1("VIEW3D_MT_edit_text_context_menu")



############################################
# Grease Pencil
############################################
	km = kc.keymaps.new('Grease Pencil', space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav3D()

# erase annotation
#	kmi = km.keymap_items.new('gpencil.annotate', m_select, 'PRESS', key_modifier='E', ctrl=True, shift=True, alt=True)
#	kmi_props_setattr(kmi.properties, "mode", 'ERASER')
#	kmi_props_setattr(kmi.properties, "wait_for_input", False)


############################################
# Grease Pencil Stroke Edit Mode
############################################
	km = kc.keymaps.new("Grease Pencil Stroke Edit Mode", space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav3D()

	context1("VIEW3D_MT_gpencil_edit_context_menu")


############################################
# Grease Pencil Stroke Paint Mode
############################################
	km = kc.keymaps.new("Grease Pencil Stroke Paint Mode", space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav3D()

	context2("VIEW3D_PT_gpencil_draw_context_menu", "keep_open", True)



############################################
# Pose
############################################
	km = kc.keymaps.new("Pose", space_type='EMPTY', region_type='WINDOW', modal=False)

	context1("VIEW3D_MT_pose_context_menu")





############################################
# Mask Editing
############################################
	km = kc.keymaps.new('Mask Editing', space_type='EMPTY', region_type='WINDOW', modal=False)

#these don't work; inherits nav behavior from another mode
#	#viewNav2D()


#cursor - doesn't work
#	kmi = km.keymap_items.new('uv.cursor_set', m_cursor, 'PRESS', ctrl=True, alt=True, shift=True)


############################################
# Paint Curve
############################################
	km = kc.keymaps.new("Paint Curve", space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav2D()

#secondary stuff
	kmi = km.keymap_items.new('paintcurve.add_point_slide', m_secondary, 'PRESS', ctrl=True)
	kmi = km.keymap_items.new('paintcurve.slide', m_secondary, 'PRESS')
	kmi = km.keymap_items.new('paintcurve.slide', m_secondary, 'PRESS', shift=True)
	kmi_props_setattr(kmi.properties, "align", True)

#cursor
	kmi = km.keymap_items.new('paintcurve.cursor', m_cursor, 'PRESS', ctrl=True, shift=True, alt=True)




############################################
# Curve
############################################
	km = kc.keymaps.new('Curve', space_type='EMPTY', region_type='WINDOW', modal=False)

	viewNav3D()

	context1("VIEW3D_MT_edit_curve_context_menu")

#secondary stuff
	kmi = km.keymap_items.new('curve.vertex_add', m_secondary, 'PRESS', ctrl=True)




############################################
# Text Editor panel
############################################
	km = kc.keymaps.new('Text', space_type='TEXT_EDITOR', region_type='WINDOW', modal=False)

	#viewNav2D_subset()

	context1("TEXT_MT_toolbox")

	kmi = km.keymap_items.new('text.scroll_bar', m_nav, 'PRESS')
	kmi = km.keymap_items.new('text.scroll', m_nav, 'PRESS')



############################################
# Outliner
############################################
	km = kc.keymaps.new('Outliner', space_type='OUTLINER', region_type='WINDOW', modal=False)

#context menu
	context0("outliner.operation")

	kmi = km.keymap_items.new('view2d.pan', m_nav, 'PRESS', shift=True)






# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# MODALS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


############################################
# Generic Gizmos Tweak Modal Map
############################################
	km = kc.keymaps.new('Generic Gizmos Tweak Modal Map', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'PRESS', any=True)


############################################
# Generic Gizmos Select Tweak Modal Map
############################################
	km = kc.keymaps.new('Generic Gizmos Select Tweak Modal Map', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('NONE', m_secondary, 'PRESS', any=True)


############################################
# Knife Tool Modal Map
############################################
	km = kc.keymaps.new('Knife Tool Modal Map', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('PANNING', m_nav, 'ANY', any=True)
	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'PRESS', any=True)


############################################
# Custom Normals Modal Map
############################################
	km = kc.keymaps.new('Custom Normals Modal Map', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'CLICK')
	kmi = km.keymap_items.new_modal('SET_USE_3DCURSOR', m_secondary, 'CLICK', ctrl=True)
	kmi = km.keymap_items.new_modal('SET_USE_SELECTED', m_select, 'CLICK', ctrl=True)


############################################
# Bevel Modal Map
############################################
	km = kc.keymaps.new('Bevel Modal Map', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'PRESS', any=True)



############################################
# Eyedropper Modal Map
############################################
	km = kc.keymaps.new('Eyedropper Modal Map', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'PRESS', any=True)


############################################
# Transform Modal Map
############################################
	km = kc.keymaps.new('Transform Modal Map', space_type='EMPTY', region_type='WINDOW', modal=True)

#don't enable this: it breaks MMB-triggered axis constraints on transform / duplicate
#	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'PRESS', any=True)


############################################
# View3D Fly Modal
############################################
	km = kc.keymaps.new('View3D Fly Modal', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'ANY', any=True)
	kmi = km.keymap_items.new_modal('PAN_ENABLE', m_nav, 'PRESS', any=True)
	kmi = km.keymap_items.new_modal('PAN_DISABLE', m_nav, 'RELEASE', any=True)


############################################
# View3D Walk Modal
############################################
	km = kc.keymaps.new('View3D Walk Modal', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'ANY', any=True)
	kmi = km.keymap_items.new_modal('TELEPORT', m_nav, 'ANY', any=True)


############################################
# View3D Rotate Modal
############################################
	km = kc.keymaps.new('View3D Rotate Modal', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CONFIRM', m_nav, 'RELEASE', any=True)


############################################
# View3D Move Modal
############################################
	km = kc.keymaps.new('View3D Move Modal', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CONFIRM', m_nav, 'RELEASE', any=True)


############################################
# View3D Zoom Modal
############################################
	km = kc.keymaps.new('View3D Zoom Modal', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CONFIRM', m_nav, 'RELEASE', any=True)


############################################
# View3D Dolly Modal
############################################
	km = kc.keymaps.new('View3D Dolly Modal', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CONFIRM', m_nav, 'RELEASE', any=True)


############################################
# View3D Gesture Circle
############################################
	km = kc.keymaps.new('View3D Gesture Circle', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'ANY', any=True)
	kmi = km.keymap_items.new_modal('DESELECT', m_nav, 'PRESS')
	kmi = km.keymap_items.new_modal('NOP', m_nav, 'RELEASE', any=True)


############################################
# Gesture Box
############################################
	km = kc.keymaps.new('Gesture Box', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'PRESS', any=True)
	kmi = km.keymap_items.new_modal('SELECT', m_nav, 'RELEASE', any=True)
	kmi = km.keymap_items.new_modal('BEGIN', m_nav, 'PRESS')
	kmi = km.keymap_items.new_modal('DESELECT', m_nav, 'RELEASE')



############################################
# Gesture Zoom Border
############################################
	km = kc.keymaps.new('Gesture Zoom Border', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'ANY', any=True)
	kmi = km.keymap_items.new_modal('BEGIN', m_nav, 'PRESS')
	kmi = km.keymap_items.new_modal('OUT', m_nav, 'RELEASE')


############################################
# Gesture Straight Line
############################################
	km = kc.keymaps.new('Gesture Straight Line', space_type='EMPTY', region_type='WINDOW', modal=True)

	kmi = km.keymap_items.new_modal('CANCEL', m_secondary, 'ANY', any=True)



def register():
	start_delay()

def unregister():
	start_delay()

if __name__ == "__main__":
	register()
