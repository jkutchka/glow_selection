#!/usr/bin/env python
# A script created that makes a glow effect of the selection area
# Borrowed parts from python_selection_to_layer_cropped found at https://github.com/fre-sch

from gimpfu import *


def python_glow_selection(image, drawable, option_var, FrameCount_var ):
    if pdb.gimp_selection_is_empty(image):
        raise Exception('No selection in image')
    pdb.gimp_image_undo_group_start(image)
    prev_layer = image.active_layer

    pdb.gimp_edit_cut(image.active_layer)
    fsel = pdb.gimp_edit_paste(drawable, False)
    pdb.gimp_floating_sel_to_layer(fsel)
    image.active_layer.name = "Frame0"
    pdb.plug_in_autocrop_layer(image, image.active_layer)
    
    base_layer = 0
    for i in image.layers:
       if i.name == 'Frame0':
          base_layer = i
          break
    
    pdb.gimp_drawable_set_visible(base_layer, False)
    
    blank_array = [ 0.0, 0.0, 1.0, 0.0 ]
     
    # Remove the color contributions from the other channels
    
    if (option_var+1) == HISTOGRAM_RED:
        pdb.gimp_drawable_curves_spline(base_layer, HISTOGRAM_GREEN, 4, blank_array)
        pdb.gimp_drawable_curves_spline(base_layer, HISTOGRAM_BLUE, 4, blank_array) 

    if (option_var+1) == HISTOGRAM_GREEN:
        pdb.gimp_drawable_curves_spline(base_layer, HISTOGRAM_RED, 4, blank_array)
        pdb.gimp_drawable_curves_spline(base_layer, HISTOGRAM_BLUE, 4, blank_array) 

    if (option_var+1) == HISTOGRAM_BLUE:
        pdb.gimp_drawable_curves_spline(base_layer, HISTOGRAM_GREEN, 4, blank_array)
        pdb.gimp_drawable_curves_spline(base_layer, HISTOGRAM_RED, 4, blank_array) 

    #   Need to re_arrange new frames' order.
        
    step_size = 1.00 / FrameCount_var 
    
    #Beta
    
    for i in range(0,int(FrameCount_var),1):
       new_frame = base_layer.copy()
       new_frame.name = "Frame" + str(i+1)
       image.add_layer(new_frame, 0)
       points_array = [ 0.0, (i*step_size), 1.0, 1.0]
       pdb.gimp_drawable_curves_spline(new_frame, option_var+1, 4, points_array) 
    
    #Alpha
    
    for i in range(0,int(FrameCount_var),1):
       new_frame = base_layer.copy()
       new_frame.name = "-Frame" + str(i+1)
       image.add_layer(new_frame, 0)
       points_array = [ (i*step_size), 0.0, 1.0, 1.0]
       pdb.gimp_drawable_curves_spline(new_frame, option_var+1, 4, points_array) 
    
    #Beta ^ -1
    for i in range(0,int(FrameCount_var),1):
       dupe_frame = image.layers[2*i+int(FrameCount_var)].copy()
       #dupe_frame.name = "Copy of " + dupe_frame.name 
       image.add_layer(dupe_frame, int(FrameCount_var))
     
    #Alpha ^ -1
    for i in range(0,int(FrameCount_var),1):
       dupe_frame = image.layers[int(FrameCount_var) - i - 1].copy();
       #dupe_frame.name = "Copy of " + dupe_frame.name 
       image.add_layer(dupe_frame, len(image.layers) - 1)
       
    # for (i = 0; i < FrameCount_var; i++)
       # new_frame = base_layer.copy()
       # new_frame.name = "Frame" + str(i+1)
    
    #keep gif from stagnating
    
    for i in range(3, 1, -1):
       image.remove_layer(image.layers[i * int(FrameCount_var) - 1])
    
    image.remove_layer(base_layer)
    
    #merge black back into the original image
    
    pdb.gimp_drawable_set_visible(image.layers[len(image.layers)-2], True)
    pdb.gimp_drawable_set_visible(image.layers[len(image.layers)-1], True)
    pdb.gimp_image_merge_down(image, image.layers[len(image.layers) - 2], 0) 
    #pdb.gimp_image_merge_visible_layers(image, 0)
    
    #pdb.file_gif_save2(run-mode=0, image=image,loop=True, default-delay=10, default-dispose=1, force-delay=True, force-dispose=True)
    image.active_layer = image.layers[len(image.layers) -1]
    
    #set to indexed mode.
    pdb.gimp_image_convert_indexed(image, 0, 0, 255, False, False, "None")
    
    pdb.gimp_image_undo_group_end(image)
    

register(
    "python_fu_glow_selection",
    "creates a glow effect of the selected area",
    "creates a glow effect of the selected area",
    "https://github.com/jkutchka",
    "https://github.com/jkutchka",
    "2023",
    "<Image>/Filters/Glow Selection",
    "RGB*",
    [
     (PF_OPTION, "option_var", "Channel select", 0,
            ("Red", "Green", "Blue", "Alpha")
      ),
    #(PF_CHANNEL, "Channel_var", "channel", None),
    (PF_SLIDER, "FrameCount_var",  "Frame Count", 4, (0, 64, 1)),
    ],
    [],
    python_glow_selection
)

main()