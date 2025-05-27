# mobius.py

import numpy as np

class MobiusStrip:
    def __init__(self, R=1.0, w=0.3, n=300):
        # Initialize Möbius strip parameters
        self.R = R            # Radius of the central circle
        self.w = w            # Width of the strip
        self.n = n            # Resolution of mesh
        self._build_grid()    # Build u-v grid
        self._compute_surface()  # Compute x, y, z coordinates

    def _build_grid(self):
        # Generate mesh grid for u and v parameters
        u = np.linspace(0, 2 * np.pi, self.n)
        v = np.linspace(-self.w / 2, self.w / 2, self.n)
        self.u, self.v = np.meshgrid(u, v, indexing='ij')

    def _compute_surface(self):
        # Compute x, y, z coordinates using parametric equations
        u, v = self.u, self.v
        self.x = (self.R + v * np.cos(u / 2)) * np.cos(u)
        self.y = (self.R + v * np.cos(u / 2)) * np.sin(u)
        self.z = v * np.sin(u / 2)

    def get_surface(self):
        # Return the surface mesh
        return self.x, self.y, self.z

    def surface_area(self):
        # Approximate surface area using numerical integration
        du = 2 * np.pi / (self.n - 1)
        dv = self.w / (self.n - 1)

        dx_du = np.gradient(self.x, axis=0) / du
        dx_dv = np.gradient(self.x, axis=1) / dv
        dy_du = np.gradient(self.y, axis=0) / du
        dy_dv = np.gradient(self.y, axis=1) / dv
        dz_du = np.gradient(self.z, axis=0) / du
        dz_dv = np.gradient(self.z, axis=1) / dv

        # Compute cross product of the partial derivatives
        cross_x = dy_du * dz_dv - dz_du * dy_dv
        cross_y = dz_du * dx_dv - dx_du * dz_dv
        cross_z = dx_du * dy_dv - dy_du * dx_dv

        # Surface area element
        dA = np.sqrt(cross_x**2 + cross_y**2 + cross_z**2)
        return np.sum(dA) * du * dv

    def edge_length(self):
        # Approximate edge length of the Möbius strip
        u = np.linspace(0, 2 * np.pi, self.n)
        v = self.w / 2

        x = (self.R + v * np.cos(u / 2)) * np.cos(u)
        y = (self.R + v * np.cos(u / 2)) * np.sin(u)
        z = v * np.sin(u / 2)

        # Compute Euclidean distances between consecutive edge points
        dx = np.diff(x)
        dy = np.diff(y)
        dz = np.diff(z)

        return np.sum(np.sqrt(dx**2 + dy**2 + dz**2))
