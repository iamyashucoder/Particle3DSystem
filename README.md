# 3D Particle System

A physics-based particle effects simulator featuring fire, smoke, rain, and explosions with realistic movement, gravity, wind, and collision detection.

## Features

- **4 Particle Effects**: Fire, smoke, rain, and explosion
- **Physics Simulation**: Gravity, wind, air resistance, and momentum
- **Collision Detection**: Ground plane interaction with bounce/splash
- **Interactive Controls**: Pause, reset, clear, and effect switching
- **Real-time Animation**: Smooth 60 FPS particle updates
- **Customizable Parameters**: Adjust emission rates, forces, and particle properties
- **Fade Effects**: Particles fade out naturally over their lifetime
![Demo Animation](./assets/demo.gif)
## Setup Instructions

### 1. Create Conda Environment

```bash
conda create -n particles3d python=3.9 -y
conda activate particles3d
```

### 2. Install Required Packages

```bash
pip install numpy matplotlib
```

Same dependencies as all previous projects!

### 3. Run the Demo

```bash
python main.py
```

## Particle Effects

### 🔥 Fire
- **Behavior**: Particles rise upward with heat
- **Physics**: Slight upward gravity, random drift
- **Colors**: Yellow (hot) → Orange → Red (cooling)
- **Lifetime**: 1.5 - 3.0 seconds
- **Use Cases**: Campfires, torches, explosions aftermath

### 💨 Smoke
- **Behavior**: Floats upward and drifts with wind
- **Physics**: Low mass, strong wind influence, slow rise
- **Colors**: Various shades of gray
- **Lifetime**: 3.0 - 5.0 seconds
- **Use Cases**: Chimneys, industrial sites, fog effects

### 🌧️ Rain
- **Behavior**: Falls rapidly from above
- **Physics**: High mass, strong downward gravity
- **Colors**: Sky blue
- **Lifetime**: 3.0 - 5.0 seconds (disappears on ground contact)
- **Use Cases**: Weather effects, waterfalls

### 💥 Explosion
- **Behavior**: Radial burst in all directions
- **Physics**: High initial velocity, gravity pulls down, bounces on ground
- **Colors**: Yellow, orange, red (fire colors)
- **Lifetime**: 2.0 - 4.0 seconds
- **Use Cases**: Bombs, fireworks, impacts

## Controls

### Mouse Controls
- **Click and drag**: Rotate the 3D view
- **Scroll wheel**: Zoom in/out
- **Right-click and drag**: Pan the view

### Button Controls
- **Pause/Resume**: Pause or resume particle simulation
- **Reset**: Clear all particles and restart system
- **Clear All**: Remove all existing particles immediately

### Radio Buttons
Switch between effects without restarting:
- **Fire**: Switch to fire effect
- **Smoke**: Switch to smoke effect
- **Rain**: Switch to rain effect
- **Explosion**: Switch to explosion effect

## Physics Parameters

### Gravity
Controls downward force on particles:
- Fire: `[0, 0, 0.5]` (slight upward)
- Smoke: `[0, 0, 0.2]` (float upward)
- Rain: `[0, 0, -15.0]` (strong downward)
- Explosion: `[0, 0, -5.0]` (moderate downward)

### Wind
Simulates air currents:
- Fire: `[0.1, 0.1, 0]` (gentle drift)
- Smoke: `[0.5, 0.3, 0.1]` (noticeable drift)
- Rain: `[0.5, 0, 0]` (horizontal wind)
- Explosion: `[0, 0, 0]` (no wind)

### Damping
Air resistance factor (0-1):
- Default: `0.98` (2% energy loss per frame)

## Customization

### Adjust Emission Rate
```python
# In ParticleSystem._setup_effect():
self.emission_rate = 20  # More particles per frame
```

### Change Particle Lifetime
```python
# In emit methods (e.g., _emit_fire):
lifetime = np.random.uniform(5.0, 10.0)  # Longer lasting
```

### Modify Gravity
```python
# In _setup_effect():
self.gravity = np.array([0, 0, -20.0])  # Stronger gravity
```

### Add Custom Colors
```python
# In emit methods:
color = '#00FF00'  # Green particles
```

### Adjust Particle Size
```python
# In emit methods:
size = np.random.uniform(50, 100)  # Larger particles
```

### Change Maximum Particles
```python
# In ParticleSystem.__init__:
self.max_particles = 1000  # More particles (may affect performance)
```

## Advanced Customization

### Create Custom Effect

Add a new effect type by creating an emit method:

```python
def _emit_sparkle(self):
    """Emit sparkle particles"""
    for _ in range(self.emission_rate):
        if len(self.particles) >= self.max_particles:
            break
        
        # Upward with random spread
        velocity = np.array([
            np.random.uniform(-2, 2),
            np.random.uniform(-2, 2),
            np.random.uniform(5, 10)
        ])
        
        position = self.emitter_pos.copy()
        color = np.random.choice(['#FFD700', '#FFFFFF', '#FFFF00'])
        size = np.random.uniform(10, 20)
        lifetime = np.random.uniform(1.0, 2.0)
        
        particle = Particle(position, velocity, color, size, lifetime, mass=0.5)
        self.particles.append(particle)
```

Then add it to the effect setup:
```python
elif self.effect_type == 'sparkle':
    self.emission_rate = 15
    self.gravity = np.array([0, 0, -2.0])
    self.wind = np.array([0.1, 0.1, 0])
```

### Modify Collision Response

Change how particles interact with ground:

```python
# In update() method:
if self.collision_enabled and particle.position[2] < self.ground_level:
    particle.position[2] = self.ground_level
    particle.velocity[2] *= -0.8  # More bouncy
    particle.velocity *= 0.9  # Different damping
```

## Project Structure

```
├── main.py          # Complete implementation
└── README.md        # This file
```

## Example Output

```
======================================================================
3D PARTICLE SYSTEM SIMULATOR
======================================================================

[1/3] Initializing particle system...
✓ Physics engine ready
✓ Collision detection enabled
✓ Gravity and wind simulation active

[2/3] Available particle effects:
  1. Fire      - Rising flames with heat distortion
  2. Smoke     - Floating smoke with wind drift
  3. Rain      - Falling raindrops with gravity
  4. Explosion - Radial burst with debris
  5. Demo All  - Show all effects in sequence

Select effect (1-5) [default: 5]: 1

[3/3] Launching particle system...

✓ Selected: FIRE effect

======================================================================
CONTROLS:
======================================================================
Mouse Controls:
  • Click and drag       - Rotate view
  • Scroll wheel         - Zoom in/out

Buttons:
  • Pause/Resume - Pause/resume particle simulation
  • Reset        - Reset system and clear particles
  • Clear All    - Remove all existing particles

Radio Buttons:
  • Use radio buttons to switch between effects
======================================================================

Close window to exit.
```

## Performance Tips

### For Better Frame Rate
1. **Reduce max particles**:
   ```python
   self.max_particles = 300
   ```

2. **Lower emission rate**:
   ```python
   self.emission_rate = 5
   ```

3. **Increase time step**:
   ```python
   self.dt = 0.1  # Faster simulation, less smooth
   ```

4. **Reduce particle lifetime**:
   ```python
   lifetime = np.random.uniform(1.0, 2.0)
   ```

### For Better Visual Quality
1. **Increase max particles**:
   ```python
   self.max_particles = 1000
   ```

2. **Increase emission rate**:
   ```python
   self.emission_rate = 20
   ```

3. **Add more color variation**:
   ```python
   colors = ['#FF0000', '#FF4500', '#FF8C00', '#FFD700', '#FFFF00']
   color = np.random.choice(colors)
   ```

## Technical Details

### Physics Integration
Uses **Euler integration** for position updates:
```
velocity += acceleration * dt
position += velocity * dt
```

### Force Application
Three forces affect particles:
1. **Gravity**: Constant downward (or upward) force
2. **Wind**: Constant directional force
3. **Damping**: Velocity-dependent air resistance

### Particle Lifecycle
1. **Emission**: Particle created with initial properties
2. **Update**: Physics applied each frame
3. **Aging**: Lifetime decreases, alpha fades
4. **Death**: Particle removed when lifetime expires

### Collision Detection
Simple ground plane collision:
- Checks if `particle.z < ground_level`
- Applies appropriate response (bounce/disappear)
- Velocity reflection for bouncing

## Educational Uses

### Physics Education
- Demonstrate gravity and air resistance
- Show projectile motion
- Illustrate vector addition of forces

### Computer Graphics
- Learn particle system architecture
- Understand real-time simulation
- Practice 3D visualization techniques

### Game Development
- Prototype visual effects
- Test particle parameters
- Design explosion mechanics

## Common Issues & Solutions

**Issue**: Particles fall through ground
- **Solution**: Increase collision check frequency or reduce dt

**Issue**: Effect looks unrealistic
- **Solution**: Adjust gravity, wind, and damping parameters

**Issue**: Too few/many particles
- **Solution**: Adjust emission_rate and max_particles

**Issue**: Particles disappear too quickly
- **Solution**: Increase particle lifetime

**Issue**: Simulation is too slow
- **Solution**: Reduce max_particles or increase dt

## Future Enhancements (DIY)

Want to extend the project? Try adding:

1. **Particle Interactions**: Particles affect each other
2. **Multiple Emitters**: Several sources at once
3. **Textured Particles**: Use images instead of dots
4. **Trails**: Leave motion trails behind particles
5. **Obstacles**: Add boxes or spheres for collisions
6. **Wind Zones**: Areas with different wind forces
7. **Color Gradients**: Smooth color transitions over lifetime
8. **Particle Attractors**: Points that pull particles
9. **Turbulence**: Noise-based random motion
10. **Mesh Emitters**: Emit from surfaces

## Requirements

- Python 3.9+
- numpy
- matplotlib

## Tips for Best Results

1. **Fire**: Use with smoke effect for realistic flames
2. **Rain**: Increase emission rate for heavy downpour
3. **Explosion**: Click reset to trigger another explosion
4. **Smoke**: Adjust wind for different drift patterns
5. **Combine Effects**: Run multiple systems simultaneously (requires code modification)

## License

Free to use and modify for educational and personal projects.

## Author

Created as a demonstration of physics-based particle systems and real-time 3D simulation.