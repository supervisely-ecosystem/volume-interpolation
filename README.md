<div align="center" markdown>
<img src="">

# Volume Interpolation

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#How-To-Use">How To Use</a>
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

# How To Run 

1. Run app from the ecosystem

<img src="https://user-images.githubusercontent.com/48913536/176165104-e8b38e55-fb9a-4843-8d7a-ac3760732ef9.png"/>

2. Define export settings in modal window and press the **Run** button

<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/48913536/176164020-a2e940ea-8da6-4dc7-a62e-903a8529f921.png" width="650"/>
</div>

# How To Use 

1. Wait for the app to process your data, once done, a link for download will become available

<img src="https://user-images.githubusercontent.com/48913536/176164021-5be40b84-842f-447f-93eb-99c5d9d1ab23.png"/>

2. Result archive will be available for download by link at `Tasks` page or from `Team Files` by the following path:

* `Team Files`->`Export pointclouds project in Supervisely format`->`<task_id>_<projectId>_<projectName>.tar`
<img src="https://user-images.githubusercontent.com/48913536/176164028-3e535f5a-a31a-4b24-b55c-955e2fad0f2a.png"/>
