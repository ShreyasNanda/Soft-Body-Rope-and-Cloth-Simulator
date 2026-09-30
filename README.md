# 2D Soft-Body Rope & Cloth Simulator

A real-time, interactive physical simulation of elastic structural networks built entirely from scratch in Python using Pygame. The engine leverages **Verlet Integration** and distance constraints to accurately model the behavioral properties of hanging ropes, dangling strings, and fully cohesive 2D woven cloth sheets.

## 🚀 Key Features
* **Verlet Integration Mechanics:** Bypasses traditional velocity calculations by computing kinetic motion directly from position changes over time, ensuring extreme numerical stability under high structural tension.
* **Elastic Constraint Network:** Employs relaxation algorithms to iteratively solve constraints across linked points (Hooke's Law approximation).
* **Grid-Based Cloth Mechanics:** Extends basic 1D string nodes into multi-dimensional grids connected by alternating horizontal and vertical links.
* **Interactive Controls:** Users can dynamically interact with node physics or view pinned anchor states in real time.

## 📦 Installation & Setup

1. **Clone your personal sandbox repository:**
   ```bash
   git clone https://github.com
   cd soft-body-simulator
   ```

2. **Install the graphics framework:**
   ```bash
   pip install pygame
   ```

3. **Run the simulation file:**
   ```bash
   python main.py
   ```

## 📐 How the Physics Works
The engine uses **Verlet Integration** to determine positions instead of explicitly storing changing velocities. The basic position update loop operates as follows:

$$\vec{x}_{new} = \vec{x}_{current} + (\vec{x}_{current} - \vec{x}_{old}) + \vec{a} \cdot \Delta t^2$$

Distance links then check the actual distance between points against their rest lengths and divide the error corrections equally between unpinned nodes to restore equilibrium across the elastic mesh.
