# 🧵 2D Soft-Body Rope & Cloth Simulator

A real-time, interactive physical simulation of elastic structural networks built entirely from scratch in Python using Pygame. The engine leverages **Verlet Integration** and distance constraints to accurately model the behavioral properties of hanging ropes, dangling strings, and fully cohesive 2D woven cloth sheets.

---

## 🚀 Key Features

* **Verlet Integration Mechanics:** Bypasses traditional velocity calculations by computing kinetic motion directly from position changes over time, ensuring extreme numerical stability under high structural tension.
* **Elastic Constraint Network:** Employs relaxation algorithms to iteratively solve constraints across linked points (Hooke's Law approximation).
* **Grid-Based Cloth Mechanics:** Extends basic 1D string nodes into multi-dimensional grids connected by alternating horizontal and vertical links.
* **Interactive Controls:** Users can dynamically interact with node physics or view pinned anchor states in real time.

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ShreyasNanda/Soft-Body-Rope-and-Cloth-Simulator
cd Soft-Body-Rope-and-Cloth-Simulator
```

### 2. Install the Graphics Framework
Make sure you have Python installed, then fetch the Pygame dependencies:
```bash
pip install pygame
```

### 3. Launch the Simulations
Since the engine is divided into distinct execution components, you can choose to run either simulator individually:

* **To launch the Rope/String simulation:**
  ```bash
  python "2D Rope simulator.py"
  ```
* **To launch the Cloth/Mesh simulation:**
  ```bash
  python "2D Cloth simulator.py"
  ```

> 💡 *Note: Ensure you include the quotation marks in your terminal prompt exactly as shown above to properly handle the spaces in the filenames.*

---

## 📐 How the Physics Works

The engine uses **Verlet Integration** to determine positions instead of explicitly storing changing velocities. The basic position update loop operates as follows:

$$\vec{x}_{new} = \vec{x}_{current} + (\vec{x}_{current} - \vec{x}_{old}) + \vec{a} \cdot \Delta t^2$$

Distance links then check the actual distance between points against their rest lengths and divide the error corrections equally between unpinned nodes to restore equilibrium across the elastic mesh.
