# ARM_V1

A 5 degree-of-freedom robotic arm built with stepper motors, servos, inverse kinematics, and Raspberry Pi-based network control.

## Overview

ARM_V1 was my first robotic arm project. It used four NEMA 17 stepper motors and three servos to drive a 5 DOF arm. Control was handled through a Raspberry Pi connected to a computer over a socket-based interface.

The project combines a URDF arm model, inverse kinematics with `ikpy`, GPIO-based motor control, and networked command input.

## Hardware

- 4x NEMA 17 stepper motors
- 3x servos
- Raspberry Pi
- Custom mechanical arm assembly

## Software / Control

- Python-based motion control
- Inverse kinematics with `ikpy`
- URDF-based arm model
- Raspberry Pi GPIO motor and servo control
- Socket-based communication between a computer and the Pi

## What It Does

- Solves inverse kinematics for target arm positions
- Converts solved joint angles into motor and servo motion
- Supports direct/manual joint movement testing
- Supports sending position commands over a network connection

## Repository Structure

- `armcode2.py` — main inverse-kinematics and motion-control script
- `armfour.urdf` — URDF model of the robotic arm
- `armserverv1.py` — early socket-based arm server combining network input, IK, and motion execution
- `basicArmMovement.py` — manual joint and actuator movement test script
- `piArmServer.py` — Raspberry Pi-side coordinate server with motion execution and end-position error checking
- `_com1.py` — client-side script for sending coordinates or command sequences to the Pi
- `24programs` — currently empty
- `summer25/armbasicprgm.py` — later copy of the manual movement test script
- `summer25/armcode.py` — IK prototype and plotting script
- `summer25/armcode2.py` — later copy of the main IK and motion-control script
- `summer25/armfour.urdf` — duplicated or revised URDF model
- `summer25/armserverv1.py` — later server variant with network command-type handling
- `summer25/piArmServer.py` — Pi-side server variant supporting coordinate commands, angle commands, and claw control
- `summer25/pi_server.py` — lightweight socket server for network command testing
- `summer25/pi_server_subnet.py` — simpler socket communication test server
- `summer25/programs24` — note marking these as previous summer’s programs
- `README.md` — project overview

## Results

The arm was functional and could be controlled remotely, but mechanical slipping in the arm gears reduced precision and reliability.

## Status

Concluded.

## Future Work

- Improve the gearing and torque transfer
- Increase rigidity and repeatability
- Refine calibration and control

---

**Note:** This README was AI-generated with my input and review. All other project work is my own.
