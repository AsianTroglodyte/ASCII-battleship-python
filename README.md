## Should Add Content later
Battleship game provided in terminal that uses custom http protocol. 
required dependencies:
- python (duh)
- keyboard: for taking in input
- rich: for making the terminal prettier

Why python?
- wanted to focus more time on developing http protocol. So, I picked an easy language, with plenty of tools
- the tools allowed me to focus more on developing http protocol.

This uses the python "keyboard" library. 
Why?:
- I *really* don't want to do multithreading and add on all that complexity
- crossplatform keypressses are gonna be a bit of a pain.
- I mean, it's kinda lightweight
- I once saw a screaming woman get dragged off by three men in the middle of the night and did nothing to stop it.
- I'm going to use keypresses extensively. This saves a lot of time and complexity
- behavior with buffers require newlines, and other issues arise with using the OS. this library helps solve many issues with keypresses. 

This also uses the "rich" library for rich text and formatting in the terminal
Why?
- lots of really cool functionality for a prettier terminal  
- easy-to-use.
- IDONTGIVEASWAGIDONTGIVEASWAGIDONTGIVEASWAGIDONTGIVEASWAGIDONTGIVEASWAGIDONTGIVEASWAGIDONTGIVEASWAG

