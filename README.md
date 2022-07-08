<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/48913536/178039963-3d46e749-8200-4594-b3b5-8b85a5a5f774.png">

# Volume Interpolation



<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#How-To-Use">How To Use</a> •
  <a href="#Acknowledgment">Acknowledgment</a>
</p>


[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/volume-interpolation)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/volume-interpolation)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/volume-interpolation&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/volume-interpolation&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/volume-interpolation&counter=runs&label=runs&123)](https://supervise.ly)


</div>

# Overview

Volume interpolation app implements `fill between slices` algorithm from [Slicer 3D](https://www.slicer.org/) to Supervisely. This method will fill the skipped slices by interpolating between segmented slices (you can skip any number of slices between segmented slices) and create complete segmentation for selected object.

<p align="center">
  <img src="https://user-images.githubusercontent.com/48913536/178044045-9d785179-5b72-4b84-9bdb-00f16478e5af.gif" style="width:80%;"/>
</p>    

# How To Run

### ⚠️ Notice  
 * The application may already be launched by the instance administrator (**Enterprise**) or the Supervisely team (**Community**). If the app is not available in dropdown interpolator menu in Labeling tool, please contact us. If the app responds slowly, please run additional application sessions in your team.
 * **Enterprise only**: You can share started application with all users on your instance using **share** button in front of running session. We recommend to run multiple sessions if large number of users are using app simultaneously.

---

1. Run app from the ecosystem or **App sessions** page

<img src="https://user-images.githubusercontent.com/48913536/178039979-fdbbac46-e92a-485a-be89-a8257555293d.png"/>

2. Press the **Run** button in the modal window

<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/48913536/178040333-94926f78-bef6-4a3f-8a56-d62d66cbfb62.png" width="650"/>
</div>

3. Wait for the app to deploy

<img src="https://user-images.githubusercontent.com/48913536/178039984-396e806e-4001-4a44-b8b0-d408aef8c9da.png"/>

# How To Use

1. Select segmented object
2. Select interpolator (one time operation)
3. Press `Interpolate` button
4. Wait for the app to process slices, when interpolation is created, you will see it in figures of the selected object

**Controls:**

| Key                                                           | Description                               |
| ------------------------------------------------------------- | ------------------------------------------|
| <kbd>TBD</kbd>                                                | Apply interpolation                       |

<img src="https://user-images.githubusercontent.com/48913536/178040004-e38d9422-a799-474a-8892-b5780c2c2f34.png"/>

<img src="https://user-images.githubusercontent.com/48913536/178044073-0ddfa65a-5451-4252-8457-5c00c7e2c203.gif"/>
# Acknowledgment

This app is based on the great work by `Slicer 3D` team [github](https://github.com/Slicer/Slicer)). ![GitHub Org's stars](https://img.shields.io/github/stars/Slicer/Slicer?style=social)
