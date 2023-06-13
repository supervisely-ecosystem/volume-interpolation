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

The Volume Interpolation app uses an [ITK-based implementation](https://github.com/KitwareMedical/ITKMorphologicalContourInterpolation) of morphological contour interpolation that is based on a method proposed by Albu et al. in 2008. Interpolation is done by first determining correspondence between shapes on adjacent segmented slices by detecting overlaps, then aligning the corresponding shapes, generating a transition sequence of one-pixel dilations, and taking the median as a result.

<p align="center">
  <img src="https://user-images.githubusercontent.com/48913536/178044045-9d785179-5b72-4b84-9bdb-00f16478e5af.gif" style="width:80%;"/>
</p>

# How To Run

### ⚠️ Notice

- The application may already be launched by the instance administrator (**Enterprise**) or the Supervisely team (**Community**). If the app is not available in the dropdown menu for selecting interpolation in the DICOM volume labeling tool, please contact your instance administrator. If the app responds slowly, please run additional application sessions in your team.
- **Enterprise only**: You can share a started application with all users on your instance using the **share** button in front of a running session. We recommend running multiple sessions if a large number of users are using the app simultaneously.

---

1. Run the app from the Ecosystem or **App Sessions** page

<img width="1280" alt="2023-06-13_18-02-00" src="https://github.com/supervisely-ecosystem/volume-interpolation/assets/57998637/70675d98-279b-45ae-af92-0bfb8684a4f0">

2. Press the **Run** button in the modal window

<div align="left" markdown>
<img width="403" alt="2023-06-13_18-04-14" src="https://github.com/supervisely-ecosystem/volume-interpolation/assets/57998637/b32c126d-205c-4f6b-9440-a24cd0801c99">
</div>

3. Wait for the app to deploy

<img width="1280" alt="2023-06-13_18-00-18" src="https://github.com/supervisely-ecosystem/volume-interpolation/assets/57998637/20af364a-555e-40fc-8e5f-78699c0f8901">

# How To Use

1. Select interpolator (one-time operation)
2. Select segmented object
3. Press `Interpolate` button
4. Wait for the app to process slices, when interpolation is created, you will see it in the figures of the selected object. Press `APPLY` to save the result or `CANCEL` to make edits.

**Controls:**

| Key                          | Description         |
| ---------------------------- | ------------------- |
| <kbd>Ctrl</kbd>+<kbd>I</kbd> | Apply interpolation |


<img width="1280" alt="2023-06-13_15-54-32" src="https://github.com/supervisely-ecosystem/volume-interpolation/assets/57998637/9adedecd-54fc-4639-b588-bb0f1cfceab4">


<img width="1280" src="https://github.com/supervisely-ecosystem/volume-interpolation/assets/57998637/43d4c40e-c688-4f03-bd9b-ed93f80cbe92"/>

# Acknowledgment

This app is based on the great work of Kitware, Inc.

[ITKMorphologicalContourInterpolation](https://github.com/KitwareMedical/) ![GitHub Org's stars](https://img.shields.io/github/stars/KitwareMedical/ITKMorphologicalContourInterpolation?style=social)
