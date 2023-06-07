<div align="center" markdown>
<img src="https://github.com/supervisely-ecosystem/volume-interpolation/assets/57998637/af1b9e46-9096-4060-b895-687fb4286951">

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
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/volume-interpolation.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/volume-interpolation.png)](https://supervise.ly)

</div>

# Overview

The Volume interpolation app uses an [ITK-based implementation](https://github.com/KitwareMedical/ITKMorphologicalContourInterpolation) of morphological contour interpolation that is based on a method proposed by Albu et al. in 2008. Interpolation is done by first determining correspondence between shapes on adjacent segmented slices by detecting overlaps, then aligning the corresponding shapes, generating a transition sequence of one-pixel dilations, and taking the median as result.

<p align="center">
  <img src="https://user-images.githubusercontent.com/48913536/178044045-9d785179-5b72-4b84-9bdb-00f16478e5af.gif" style="width:80%;"/>
</p>

# How To Run

### ⚠️ Notice

- The application may already be launched by the instance administrator (**Enterprise**) or the Supervisely team (**Community**). If the app is not available in the dropdown menu for selecting interpolation in the DICOM volume labeling tool, please contact your instance administrator. If the app responds slowly, please run additional application sessions in your team.
- **Enterprise only**: You can share a started application with all users on your instance using **share** button in front of a running session. We recommend running multiple sessions if a large number of users are using the app simultaneously.

---

1. Run the app from the Ecosystem or **App Sessions** page

<img src="https://github.com/supervisely-ecosystem/volume-interpolation/assets/57998637/a64ad2e3-7a04-4f76-9aed-a6f109d01a9d"/>

2. Press the **Run** button in the modal window

<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/48913536/178040333-94926f78-bef6-4a3f-8a56-d62d66cbfb62.png" width="650"/>
</div>

3. Wait for the app to deploy

<img src="https://github.com/supervisely-ecosystem/volume-interpolation/assets/57998637/be30836b-6739-42bb-ad18-c89db64376bc"/>

# How To Use

1. Select segmented object
2. Select interpolator (one time operation)
3. Press `Interpolate` button
4. Wait for the app to process slices, when interpolation is created, you will see it in figures of the selected object

**Controls:**

| Key                          | Description         |
| ---------------------------- | ------------------- |
| <kbd>Ctrl</kbd>+<kbd>I</kbd> | Apply interpolation |

<img src="https://user-images.githubusercontent.com/48913536/178040004-e38d9422-a799-474a-8892-b5780c2c2f34.png"/>

<img src="https://user-images.githubusercontent.com/48913536/178044073-0ddfa65a-5451-4252-8457-5c00c7e2c203.gif"/>

# Acknowledgment

This app is based on the great work of Kitware, Inc.

[ITKMorphologicalContourInterpolation](https://github.com/KitwareMedical/) ![GitHub Org's stars](https://img.shields.io/github/stars/KitwareMedical/ITKMorphologicalContourInterpolation?style=social)
