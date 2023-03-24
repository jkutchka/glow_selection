# glow_selection
A Gimp plugin that creates an animated gif with the selected region glowing.

Place in your Gimp plugins directory.

1. Select a region with the selection tools
2. Go to Filters->Glow Selection
3. Set the color channel to red, green, or blue depending on what color you want to pulse
4. Set the frame count. 4-8 is usually good enough
5. Click Ok

6. Export to GIF
   A.  Give it a file name and save with extension .gif to load the gif options dialog box
7. Check the following:
   A. As animation
   B. Loop Forever
   C. Use delay entered above for all frames
   D. Use disposal entered above for all frames
8. Set the delay between frames.  10ms is good; gimp won't go lower.
9. Set Frame disposal where unspecified to "Cumulative Layers(combine)
10. Export.

