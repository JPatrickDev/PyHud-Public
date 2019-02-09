# PyHud
A Python "Operating System", designed for making custom dashboards/tablets. 

### Project Overview
This project is designed for use with a Raspberry Pi B+, but should work on any device that can run Python and pygame.

The project is a program that behaves like a mobile operating system, it can run 3rd party applications developed using its libraries and provides an easy to use touch interface to switch between and view applications. To a user it would behave just as if the system was a standalone mobile operating system.

However the project actually runs on Python3 and pygame, meaning it can be ran easily on many different devices and display sizes, with the User Interface System automatically scaling the display to fit.  

The rendering engine is also fairly efficient, hopefully allowing a smooth user experience on low-end devices. 

### Features
* Rendering engine only redraws the parts of the screen that have changed, allowing good performance on lower-end devices. 
* UI Elements are designed to be used with touch-input, but a mouse will also work fine. 
* The UI System automatically resizes apps to match the current screen size, allowing one app to run on many devices. 
* Built on pygame - Lots of documentation available.
* Extensible - Build your own apps and create new UI Elements.

### Creating new Apps
Please see the systemapps folder for some examples of existing applications. Hopefully this is enough to get you started with development until I have time to create some more formal tutorials.
 
Once you have made an application, it can be placed in the apps/ folder, where it will be available for use via the app grid or can be placed on a Home Page by editing the app/internal/appLayout.json file. 

### Contributing
You can make a pull request, and instead of merging the pull I can integrate your changes in to my Private repository ready for the next major release.
I will aim to then provide you with the latest version(from Private Repository) that includes your changes as soon as possible, both as a thank you for providing your changes, and so you can check to make sure it's been integrated successfully. 

### This Repository
This Repo will be updated with every major release of PyHud, and some minor releases as well if they are important enough. 