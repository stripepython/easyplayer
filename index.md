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
```python
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
