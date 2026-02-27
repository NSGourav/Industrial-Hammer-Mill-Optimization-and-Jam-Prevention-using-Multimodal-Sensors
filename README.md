# Industrial Hammer Mill Optimization and Jam Prevention using Multimodal Sensors

## Problem Statement
In industrial operations, hammer mills are critical for material processing. In this system, the hammer mill processes iron mesh to remove rust. However, unexpected jams frequently occur, leading to costly downtime, maintenance delays, and production inefficiencies. These jam events are difficult to predict using conventional monitoring systems, resulting in reactive maintenance and unscheduled shutdowns.

This project addresses the problem by designing and deploying a synchronized multimodal perception and data acquisition system to monitor material flow characteristics and machine load conditions. The objective was to build a robust edge-based sensing architecture capable of capturing, fusing, and structuring heterogeneous industrial signals (sensors) for downstream anomaly analysis.

## Overview
This project presents the design and deployment of a multimodal industrial monitoring system built on an NVIDIA Jetson Orin Nano. The system integrates RGB-D perception, conveyor velocity sensing, and motor current monitoring into a unified edge-computing pipeline, enabling real-time multimodal sensor synchronization and industrial-grade data fusion.

Using depth-guided mesh segmentation and frame-wise volume estimation, the pipeline generates structured multimodal datasets by merging visual features with conveyor speed and motor current signals. The complete sensing, synchronization, and logging architecture was deployed and validated under real industrial operating conditions.

## System Architecture
The system follows an edge-based multimodal acquisition and synchronization architecture.

###  Hardware Components
- NVIDIA Jetson Orin Nano  
- Intel RealSense L515 (RGB-D + point cloud)  
- Tachometer (conveyor belt velocity measurement)  
- Hammer mill & crusher motor current sensors  
- AWS cloud logging  
- Remote SSH monitoring

All sensor streams are timestamped and synchronized before dataset generation.

## Data Acquisition
The system captures:
- RGB images  
- 16-bit depth images  
- Point cloud data (.ply)  
- Conveyor belt velocity (tachometer)  
- Motor current signals

All modalities are timestamp-aligned and fused to ensure deterministic multimodal synchronization across perception and machine-state signals.
## Processing Workflow

### Image Enhancement
**RGB Processing**
- Color contrast enhancement  
- Noise reduction  
- Motion blur reduction
**Depth Processing**
- Depth image completion  
- Depth refinement  

### Multimodal Fusion & Mesh Segmentation
- Weighted RGB–Depth fusion  
- Edge detection on RGB frames  
- Depth-guided iron mesh segmentation  
- Isolation of material region from background
 
Segmentation is primarily driven by depth information and refined using RGB features.

### Volume Estimation
- Extraction of segmented mesh region  
- Depth-based height profile computation  
- Frame-wise material volume estimation  

### Multimodal Sensor Fusion & Structured Data Pipeline
For each synchronized frame:
- Estimated material volume  
- Conveyor velocity  
- Motor current

These parameters are merged using timestamps to produce structured datasets suitable for regression-based jam-condition analysis.

*(This phase focused on perception, synchronization, and structured data generation; closed-loop predictive deployment was outside current scope.)*

## Technologies Used
Jetson Orin Nano • Intel RealSense L515 • RGB-D Processing • Depth Completion • Edge Detection • Multimodal Fusion • Python • OpenCV • AWS S3 • Linux • SSH

## Colab Experiments
📓 Image Processing: [Open Image Processing Notebook](https://colab.research.google.com/drive/1XWoZyhsCpmAs5MtlCFcBB17cX8sed00x?usp=sharing) 
