"""
3D Particle System
Physics-based particle effects: fire, smoke, rain, and explosions
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, RadioButtons
import random


class Particle:
    """Single particle with physics properties"""
    
    def __init__(self, position, velocity, color, size, lifetime, mass=1.0):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0
        self.mass = mass
        self.alive = True
        self.alpha = 1.0
        
    def update(self, dt, gravity, wind, damping):
        """Update particle physics"""
        if not self.alive:
            return
        
        # Apply forces
        acceleration = gravity + wind / self.mass
        self.velocity += acceleration * dt
        self.velocity *= damping  # Air resistance
        
        # Update position
        self.position += self.velocity * dt
        
        # Update age
        self.age += dt
        
        # Update alpha based on lifetime
        self.alpha = max(0, 1 - (self.age / self.lifetime))
        
        # Check if particle should die
        if self.age >= self.lifetime:
            self.alive = False


class ParticleSystem:
    """Manages particle effects with physics simulation"""
    
    def __init__(self, effect_type='fire'):
        self.effect_type = effect_type
        self.particles = []
        self.max_particles = 500
        self.time = 0
        self.dt = 0.05
        self.paused = False
        
        # Physics parameters
        self.gravity = np.array([0, 0, -9.8])
        self.wind = np.array([0, 0, 0])
        self.damping = 0.98
        self.ground_level = 0
        self.collision_enabled = True
        
        # Emitter position
        self.emitter_pos = np.array([0.0, 0.0, 0.0])
        
        # Effect-specific parameters
        self._setup_effect()
    
    def _setup_effect(self):
        """Configure parameters based on effect type"""
        if self.effect_type == 'fire':
            self.emission_rate = 10  # particles per frame
            self.gravity = np.array([0, 0, 0.5])  # Slight upward
            self.wind = np.array([0.1, 0.1, 0])
            self.ground_level = 0
            
        elif self.effect_type == 'smoke':
            self.emission_rate = 5
            self.gravity = np.array([0, 0, 0.2])  # Float upward
            self.wind = np.array([0.5, 0.3, 0.1])
            self.ground_level = 0
            
        elif self.effect_type == 'rain':
            self.emission_rate = 15
            self.gravity = np.array([0, 0, -15.0])  # Strong downward
            self.wind = np.array([0.5, 0, 0])
            self.ground_level = -5
            self.emitter_pos = np.array([0.0, 0.0, 10.0])
            
        elif self.effect_type == 'explosion':
            self.emission_rate = 0  # One-time burst
            self.gravity = np.array([0, 0, -5.0])
            self.wind = np.array([0, 0, 0])
            self.ground_level = -2
    
    def emit_particles(self):
        """Emit new particles based on effect type"""
        if self.effect_type == 'fire':
            self._emit_fire()
        elif self.effect_type == 'smoke':
            self._emit_smoke()
        elif self.effect_type == 'rain':
            self._emit_rain()
        elif self.effect_type == 'explosion':
            if self.time < 0.1:  # Emit once at start
                self._emit_explosion()
    
    def _emit_fire(self):
        """Emit fire particles"""
        for _ in range(self.emission_rate):
            if len(self.particles) >= self.max_particles:
                break
            
            # Random spread
            offset = np.random.normal(0, 0.2, 3)
            position = self.emitter_pos + offset
            
            # Upward velocity with randomness
            velocity = np.array([
                np.random.uniform(-0.5, 0.5),
                np.random.uniform(-0.5, 0.5),
                np.random.uniform(2, 4)
            ])
            
            # Color gradient: yellow to red to black
            temp = np.random.uniform(0, 1)
            if temp < 0.3:
                color = '#FFFF00'  # Yellow (hot)
            elif temp < 0.6:
                color = '#FF8C00'  # Orange
            else:
                color = '#FF4500'  # Red
            
            size = np.random.uniform(20, 40)
            lifetime = np.random.uniform(1.5, 3.0)
            
            particle = Particle(position, velocity, color, size, lifetime)
            self.particles.append(particle)
    
    def _emit_smoke(self):
        """Emit smoke particles"""
        for _ in range(self.emission_rate):
            if len(self.particles) >= self.max_particles:
                break
            
            offset = np.random.normal(0, 0.3, 3)
            position = self.emitter_pos + offset + np.array([0, 0, 0.5])
            
            velocity = np.array([
                np.random.uniform(-0.3, 0.3),
                np.random.uniform(-0.3, 0.3),
                np.random.uniform(1, 2)
            ])
            
            # Gray smoke
            gray_value = np.random.randint(100, 200)
            color = f'#{gray_value:02x}{gray_value:02x}{gray_value:02x}'
            
            size = np.random.uniform(30, 60)
            lifetime = np.random.uniform(3.0, 5.0)
            
            particle = Particle(position, velocity, color, size, lifetime, mass=0.5)
            self.particles.append(particle)
    
    def _emit_rain(self):
        """Emit rain particles"""
        for _ in range(self.emission_rate):
            if len(self.particles) >= self.max_particles:
                break
            
            # Random horizontal spread
            position = self.emitter_pos + np.array([
                np.random.uniform(-5, 5),
                np.random.uniform(-5, 5),
                np.random.uniform(-1, 1)
            ])
            
            velocity = np.array([
                np.random.uniform(-0.5, 0.5),
                np.random.uniform(-0.5, 0.5),
                np.random.uniform(-5, -3)
            ])
            
            color = '#87CEEB'  # Sky blue
            size = np.random.uniform(10, 20)
            lifetime = np.random.uniform(3.0, 5.0)
            
            particle = Particle(position, velocity, color, size, lifetime, mass=2.0)
            self.particles.append(particle)
    
    def _emit_explosion(self):
        """Emit explosion particles (burst)"""
        num_particles = 200
        
        for _ in range(num_particles):
            if len(self.particles) >= self.max_particles:
                break
            
            # Random direction for explosion
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi)
            speed = np.random.uniform(3, 8)
            
            velocity = np.array([
                speed * np.sin(phi) * np.cos(theta),
                speed * np.sin(phi) * np.sin(theta),
                speed * np.cos(phi)
            ])
            
            position = self.emitter_pos.copy()
            
            # Color gradient
            color_choice = np.random.choice([
                '#FFFF00',  # Yellow
                '#FF8C00',  # Orange
                '#FF4500',  # Red
                '#FF6347'   # Tomato
            ])
            
            size = np.random.uniform(15, 35)
            lifetime = np.random.uniform(2.0, 4.0)
            
            particle = Particle(position, velocity, color_choice, size, lifetime)
            self.particles.append(particle)
    
    def update(self):
        """Update all particles"""
        if self.paused:
            return
        
        # Emit new particles
        self.emit_particles()
        
        # Update existing particles
        for particle in self.particles:
            if particle.alive:
                particle.update(self.dt, self.gravity, self.wind, self.damping)
                
                # Ground collision
                if self.collision_enabled and particle.position[2] < self.ground_level:
                    particle.position[2] = self.ground_level
                    
                    # Bounce or splash depending on effect
                    if self.effect_type == 'rain':
                        particle.alive = False  # Rain disappears on ground
                    elif self.effect_type in ['explosion', 'fire']:
                        particle.velocity[2] *= -0.3  # Bounce with energy loss
                        particle.velocity *= 0.7
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.alive]
        
        self.time += self.dt
    
    def get_particle_data(self):
        """Get particle positions, colors, and sizes for plotting"""
        if not self.particles:
            return np.array([]), np.array([]), [], []
        
        positions = np.array([p.position for p in self.particles])
        sizes = np.array([p.size * p.alpha for p in self.particles])
        colors = [p.color for p in self.particles]
        alphas = [p.alpha for p in self.particles]
        
        return positions, sizes, colors, alphas
    
    def visualize_interactive(self):
        """Create interactive 3D visualization"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        plt.subplots_adjust(left=0.15, bottom=0.15)
        
        def draw_frame(frame):
            """Draw single frame"""
            ax.clear()
            
            # Update physics
            self.update()
            
            # Get particle data
            positions, sizes, colors, alphas = self.get_particle_data()
            
            if len(positions) > 0:
                # Plot particles
                for i, pos in enumerate(positions):
                    ax.scatter(pos[0], pos[1], pos[2],
                             c=colors[i], s=sizes[i], alpha=alphas[i],
                             edgecolors='none')
            
            # Draw ground plane for effects that need it
            if self.effect_type in ['fire', 'rain', 'explosion']:
                ground_size = 10
                xx, yy = np.meshgrid(
                    np.linspace(-ground_size, ground_size, 2),
                    np.linspace(-ground_size, ground_size, 2)
                )
                zz = np.ones_like(xx) * self.ground_level
                ax.plot_surface(xx, yy, zz, alpha=0.2, color='gray')
            
            # Draw emitter
            ax.scatter(self.emitter_pos[0], self.emitter_pos[1], self.emitter_pos[2],
                      c='red', s=100, marker='x', linewidths=3)
            
            # Set axis properties
            limit = 8
            ax.set_xlim([-limit, limit])
            ax.set_ylim([-limit, limit])
            
            if self.effect_type == 'rain':
                ax.set_zlim([-5, 12])
            elif self.effect_type == 'smoke':
                ax.set_zlim([0, 15])
            else:
                ax.set_zlim([-3, 10])
            
            ax.set_xlabel('X', fontsize=10)
            ax.set_ylabel('Y', fontsize=10)
            ax.set_zlabel('Z', fontsize=10)
            
            # Title
            title = f'{self.effect_type.title()} Effect - Particles: {len(self.particles)}'
            if self.paused:
                title += ' [PAUSED]'
            ax.set_title(title, fontsize=14, fontweight='bold')
            
            # Style
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')
            ax.grid(True, alpha=0.2)
            
            return ax,
        
        # Create animation
        anim = FuncAnimation(fig, draw_frame, frames=None, interval=50, blit=False)
        
        # Control buttons
        ax_pause = plt.axes([0.2, 0.05, 0.15, 0.04])
        btn_pause = Button(ax_pause, 'Pause/Resume', color='lightgray', hovercolor='gray')
        
        ax_reset = plt.axes([0.4, 0.05, 0.15, 0.04])
        btn_reset = Button(ax_reset, 'Reset', color='lightblue', hovercolor='skyblue')
        
        ax_clear = plt.axes([0.6, 0.05, 0.15, 0.04])
        btn_clear = Button(ax_clear, 'Clear All', color='lightcoral', hovercolor='salmon')
        
        # Radio buttons for effect selection
        ax_radio = plt.axes([0.02, 0.4, 0.1, 0.2], facecolor='lightgray')
        radio = RadioButtons(ax_radio, ('Fire', 'Smoke', 'Rain', 'Explosion'))
        
        def toggle_pause(event):
            self.paused = not self.paused
        
        def reset_system(event):
            self.particles.clear()
            self.time = 0
            self.paused = False
        
        def clear_particles(event):
            self.particles.clear()
        
        def change_effect(label):
            effect_map = {
                'Fire': 'fire',
                'Smoke': 'smoke',
                'Rain': 'rain',
                'Explosion': 'explosion'
            }
            self.effect_type = effect_map[label]
            self._setup_effect()
            self.particles.clear()
            self.time = 0
        
        btn_pause.on_clicked(toggle_pause)
        btn_reset.on_clicked(reset_system)
        btn_clear.on_clicked(clear_particles)
        radio.on_clicked(change_effect)
        
        plt.show()


def demo_all_effects():
    """Demo all effects in sequence"""
    effects = ['fire', 'smoke', 'rain', 'explosion']
    
    for effect in effects:
        print(f"\n{'='*60}")
        print(f"Demonstrating: {effect.upper()} effect")
        print(f"{'='*60}")
        print("Close the window to continue to next effect...\n")
        
        system = ParticleSystem(effect_type=effect)
        system.visualize_interactive()


def main():
    """Main function"""
    print("=" * 70)
    print("3D PARTICLE SYSTEM SIMULATOR")
    print("=" * 70)
    
    print("\n[1/3] Initializing particle system...")
    print("✓ Physics engine ready")
    print("✓ Collision detection enabled")
    print("✓ Gravity and wind simulation active")
    
    print("\n[2/3] Available particle effects:")
    print("  1. Fire      - Rising flames with heat distortion")
    print("  2. Smoke     - Floating smoke with wind drift")
    print("  3. Rain      - Falling raindrops with gravity")
    print("  4. Explosion - Radial burst with debris")
    print("  5. Demo All  - Show all effects in sequence")
    
    choice = input("\nSelect effect (1-5) [default: 5]: ").strip()
    
    effect_map = {
        '1': 'fire',
        '2': 'smoke',
        '3': 'rain',
        '4': 'explosion',
        '5': 'demo',
        '': 'demo'
    }
    
    selection = effect_map.get(choice, 'demo')
    
    print(f"\n[3/3] Launching particle system...")
    
    if selection == 'demo':
        print("\n" + "=" * 70)
        print("DEMO MODE - All Effects")
        print("=" * 70)
        print("\nYou will see each effect in sequence.")
        print("Use the radio buttons to switch between effects manually.")
        print("\n" + "=" * 70)
        print("CONTROLS:")
        print("=" * 70)
        print("Mouse Controls:")
        print("  • Click and drag       - Rotate view")
        print("  • Scroll wheel         - Zoom in/out")
        print("\nButtons:")
        print("  • Pause/Resume - Pause/resume particle simulation")
        print("  • Reset        - Reset system and clear particles")
        print("  • Clear All    - Remove all existing particles")
        print("\nRadio Buttons:")
        print("  • Fire      - Switch to fire effect")
        print("  • Smoke     - Switch to smoke effect")
        print("  • Rain      - Switch to rain effect")
        print("  • Explosion - Switch to explosion effect")
        print("\nEffect Details:")
        print("  • Red X marks the emitter position")
        print("  • Gray plane represents ground (where applicable)")
        print("  • Particle count shown in title")
        print("=" * 70)
        print("\nStarting with FIRE effect...")
        print("Use radio buttons on the left to switch effects.")
        print("\nClose window to exit.\n")
        
        system = ParticleSystem(effect_type='fire')
        system.visualize_interactive()
    else:
        print(f"\n✓ Selected: {selection.upper()} effect")
        print("\n" + "=" * 70)
        print("CONTROLS:")
        print("=" * 70)
        print("Mouse Controls:")
        print("  • Click and drag       - Rotate view")
        print("  • Scroll wheel         - Zoom in/out")
        print("\nButtons:")
        print("  • Pause/Resume - Pause/resume particle simulation")
        print("  • Reset        - Reset system and clear particles")
        print("  • Clear All    - Remove all existing particles")
        print("\nRadio Buttons:")
        print("  • Use radio buttons to switch between effects")
        print("=" * 70)
        print("\nClose window to exit.\n")
        
        system = ParticleSystem(effect_type=selection)
        system.visualize_interactive()
    
    print("\n" + "=" * 70)
    print("Particle simulation ended!")
    print("=" * 70)


if __name__ == "__main__":
    main()