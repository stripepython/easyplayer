# Easy Player Document
Easyplayer is a python library that encapsulates the complex API of pygame2 to help users build games faster.

## Installation
Use `pip`:
```shell
pip install easyplayer
```
Use `git`:
```shell
git clone https://github.com/stripepython/easyplayer.git
cd easyplayer
pip install -r requirements.txt  
python setup.py install
```

Easy Player requires:
```
pygame==2.1.2
click==8.1.3
opencv-python==4.6.0.66
tqdm==4.64.0
requests==2.28.1
PyExecJS==1.5.1
pyttsx3==2.90
aiml==0.9.2
pythonnet==2.5.2
pydub==0.25.1
pillow==9.2.0
pypiwin32==223
pyaudio==0.2.11
```

If the installation fails, it can be installed manually.

## Introduce
Easyplayer is a python library that encapsulates the complex API of pygame2 to help users build games faster.  
It imitates `Scratch3`, so it is also suitable for children's programming development.  

## Operating environment
You need:
- A computer
- `python>=3.6`
- `pip`
- `Windows` or `Linux`
- `Anaconda`(**optional**)

It is recommended to run on `python3.8`, `Windows` OS.

The following is the recommended operating environment:
- `python3.8`
- `pip20.1.1`
- `Windows10`
- `Anaconda`

It passed the test in the above operating environment.
<div style="color:red">Note: Easy Player 0.x.x versions are all test versions, and some functions are unavailable!</div>

## Explain
Although this version is officially released, it still has unstable testing functions.  
Please use it carefully in actual development.

## Why
Let's compare `pygame` and `Easy Player` through a simple program.  
We will display a text with the content of `Hello World` on the window, and let the upper left corner of this text always follow the mouse pointer

- Use `pygame`:
```python
import sys
import pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Hello World')
font = pygame.font.Font(None, 26)
image = font.render('Hello World', True, (0, 0, 0))
rect = image.get_rect()
while True:
    screen.fill((255, 255, 255))
    screen.blit(image, rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    rect.x, rect.y = pygame.mouse.get_pos()
    pygame.display.update()
```

- Use `Easy Player`:
```python
import easyplayer as ep
window = ep.Window('Hello')
label = ep.Label('Hello World')
@window.when_draw
def draw():
    label.pos = window.mouse.pos
window.show()
```

Really easy? It will save you a lot of time.  
In contrast, its disadvantage is that it cannot run two windows at the same time.

In the following tutorial, you will understand the meaning and function of each sentence of code.  
Let's begin!

## Document
### Start Using
Let's create the first Easy Player project.  
First, create any `.py` file, import `Easy Player`:
```python
import easyplayer as ep
```
The `ep` module alias is our recommended name.  
Then, create a window:
```python
import easyplayer as ep
window = ep.Window('My First Easy Player Program')
```
After text, create a text object:
```python
import easyplayer as ep
window = ep.Window('My First Easy Player Program')
label = ep.Label('Hello, Easy Player!')
```
Easy player provides a component queue system, which allows you to avoid writing complex main loops and rendering functions.  
Easy player encapsulates it as a `pack` function, which saves a lot of time:
```python
import easyplayer as ep
window = ep.Window('My First Easy Player Program')
label = ep.Label('Hello, Easy Player!')
label.pack()
```
Finally, main loop and show the window:
```python
import easyplayer as ep
window = ep.Window('My First Easy Player Program')
label = ep.Label('Hello, Easy Player!')
label.pack()
window.show()
```
You will see the effect as shown in the figure in `Windows10`:
![Running Effect](https://img-blog.csdnimg.cn/74bd40abaeb34ab19445559b83bccbe4.png)

### Know Easy Player completely
This section will analyze the functions of Easy Player in detail.
You can use it as a document for Easy Player.

#### easyplayer.\_\_init_\_
Easy Player top level module.
Various APIs are defined, and most functions are automatically integrated.

#### easyplayer.\_\_main_\_
Command line program for Easy Player.  
The function is to download mblock pictures or view versions.

You can test the installation of easyplayer in this way:
```shell
python -m easyplayer -v
```

This is the command line parameter supported by Easy Player:

| Parameter Name | Parameter Shortcuts | Effect |
| ----- | ----- | ----- |
| --version | -v | View version information. |
| --install-images | -i | Install mblock picture. See the description of `easyplayer.utils.mblock` for details. |
| --clear-images | -c | Clear mblock picture. |
| --uninstall-images | -u | Uninstall mblock picture. |

#### easyplayer.exceptions
This module integrates all exception classes of Easy Player.  
Please save the following exception quick look-up table, which will help you read this document.

| Exception | Description | Father |
| ----- | ----- | ----- |
| EasyPlayerError | Base Easy Player exception | Exception |
| EasyPlayerWarning | Easy Player warning | Warning |
| EasyPlayerSaverError | Window saver error | EasyPlayerError |
| EasyPlayerModuleError | Module not installed error | EasyPlayerError, ModuleNotFoundError |
| EasyPlayerOSError | Exception caused by operating system | EasyPlayerError |
| EasyPlayerHandleError | Some operating systems do not support getting handle operation | EasyPlayerOSError |
| EasyPlayerWidgetsError | Widget errors | EasyPlayerError |
| EasyPlayerCanvasError | Canvas widget error | EasyPlayerWidgetsError |
| EasyPlayerCameraError | Camera widget error | EasyPlayerWidgetsError |
| EasyPlayerTextTooLongError | Text out of the entry widget exception | EasyPlayerWidgetsError |
| EasyPlayerOnlyReadError | Global variable manager read-only variable exception | EasyPlayerError |
| EasyPlayerCoordinateError | Coordinate auxiliary system is abnormal | EasyPlayerError |
| EasyPlayerTranslateError | Abnormal translation function | EasyPlayerError |
| EasyPlayerChatterError | Abnormal function of chat robot | EasyPlayerError |

#### easyplayer.version
Easy Player version manager module.  
It provides a `version` variable.

**easyplayer.version.version**  
It is an instantiated object of class `easyplayer.version._Version`.  
It is a subclass of `tuple`.

An example of use is shown below:
```python
import easyplayer as ep
if ep.version < (1, 0, 0):  # Judge the version number
    raise SystemExit('Version wrong.')   # Exit the program when the version number is incompatible
```

#### easyplayer.core.window
Easy Player window class module.

##### easyplayer.core.window.Window
Easy Player window object.

Usage:
```
Window(
    title: Optional[str] = '', 
    size: Optional[Tuple[int, int]] = (640, 480),
    icon: Optional[str] = None, 
    style: StyleType = easyplayer.core.styles.normal, 
    fps: int = 60,
    on_center: bool = False, 
    window_pos: Optional[Tuple[int, int]] = None,
    vsync: bool = False, 
    depth: int = 0
)
```

Parameters:

| Parameter Name | Effect | Parameter Type |
| ------ | ------ | ----- |
| `title` | Window title. | `str` |
| `size` | Window size. The first term of a two-tuple is width(weight), and the second term is height. | `Optional[Tuple[int, int]]` |
| `icon` | Window favicon. Icons in PNG and other formats are supported. | `Optional[str]` |
| `style` | Window style. Refer to the description of `easyplayer.core.styles` for details | `easyplayer.core.styles.StyleType` |
| `fps` | FPS. | `int` |
| `on_center` | Is the window in the center of the screen when it pops up. | `bool` |
| `window_pos` | Position when the window pops up. Specifying this parameter will override the function of the `on_center` parameter | `Optional[Tuple[int, int]]` |
| `vsync` | Is vsync. For more information, please refer to the documentation of `pygame` | `bool` |
| `depth` | Window depth. | `int` |
