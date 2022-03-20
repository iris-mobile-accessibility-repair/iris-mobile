# iris-mobile
The goal of Iris is to automatically repair the color-based accessibility issues in Android apps while maintaining the original UI design style of the repaired app as much as possible. We have made the source code of Iris and the corresponding dataset publicly available. We hope this project can help more developers solve the problem of color-based accessibility issues. Please feel free to contact us if you have any questions and issues. We will continue to maintain this project. Thanks for your feedback.

## Environment Configuration
* Ubuntu/Macbook
* Python: 2.7
* APKTool: 2.4.1
* Java environment (jdk): jdk1.8.0_45

## Usage
The **code_Release** folder is the resource code of this project, where **main.py** is used to build the reference database, and **repair_repack_class.py** is used to automatically repair the input app. And the **database** folder is a part of the reference database that has been built.
* Input: the apk resource file and the detection results(detect by Xbot) of an app
* Output: a new apk file repaired by Iris
* Usage: python main.py [results_folder], python repair_repack_class.py [apk(s)_folder]

## Website
* Dataset of Iris: 
https://sites.google.com/view/iris-mobile/home
* Dataset of 100 apps: 
https://drive.google.com/drive/folders/1MOEnN1j54HkRvTsigTodIpUo0IEWcOIJ?usp=sharing
* Website of Xbot (used as a detection tool): 
https://github.com/tjusenchen/Xbot
