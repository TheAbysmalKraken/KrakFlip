# KrakFlip
Pokemon Voltorb Flip Automated Solving Program

Requires mss, opencv, numpy, pynput

**DISCLAIMER**: This isn't a well made program. The logic works, but the interface is highly specific to the environment I was using when building it. Tt was an experiment and was never intended for use in other environments.
If you want to run the program you will need to adapt the constants containing the screen capture regions, pixel coordinates of particular screen points, and potentially the pixel colours as well (I'm sorry!). These are contained in `VFInterface.py`, which should be the only file you'll need to modify. Make sure the program is running on the same screen as the game if you have multiple screens.

While building this program I used a Pokemon Heartgold DS ROM running in the DeSmuMe emulator. The emulator was a maximised window (not fullscreen) on a 1920x1080 resolution monitor and had the two DS screens side-by-side, with the bottom screen on the right of the emulator. Again, I can't guarantee this setup will work for you.

The main file to run is `VFSolver.py`.
