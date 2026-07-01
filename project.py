import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('data/multi_1782907477.132166.csv')

# Extract accelerometer columns (G-Force)
ax = df['gFx'].values
ay = df['gFy'].values
az = df['gFz'].values

# Extract gyroscope columns
gx = df['wx'].values
gy = df['wy'].values
gz = df['wz'].values

# Calculate time step
df['time'] = pd.to_datetime(df['time'])
dt = df['time'].diff().dt.total_seconds().median()
print(f"Time step between readings: {dt:.4f} seconds")

# Calculate Pitch and Roll from accelerometer
pitch = np.arctan2(ax, np.sqrt(ay**2 + az**2)) * (180.0 / np.pi)
roll  = np.arctan2(ay, np.sqrt(ax**2 + az**2)) * (180.0 / np.pi)

# Calculate Yaw from gyroscope integration
yaw = np.zeros(len(gz))
for i in range(1, len(gz)):
    yaw[i] = yaw[i-1] + gz[i] * dt

# Convert yaw from radians to degrees
yaw = np.degrees(yaw)

# Time axis in seconds
time_seconds = (df['time'] - df['time'].iloc[0]).dt.total_seconds().values

# Drift analysis - check yaw during the first 10 seconds when phone was still
stationary_samples = int(10 / dt)
drift_over_10s = yaw[stationary_samples] - yaw[0]
drift_per_second = drift_over_10s / 10
print(f"Gyroscope drift over first 10 seconds: {drift_over_10s:.4f} degrees")
print(f"Drift rate: {drift_per_second:.4f} degrees per second")
print(f"Projected drift over 60 seconds: {drift_per_second * 60:.2f} degrees")

# Plot
fig, (p1, p2, p3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

p1.plot(time_seconds, yaw,   color='#1F3864', linewidth=1.5)
p1.set_ylabel('Yaw (degrees)', fontsize=11)
p1.set_title('Yaw, Pitch and Roll from iPhone IMU Data', fontsize=13, fontweight='bold')
p1.grid(True, alpha=0.3)

p2.plot(time_seconds, pitch, color='#C00000', linewidth=1.5)
p2.set_ylabel('Pitch (degrees)', fontsize=11)
p2.grid(True, alpha=0.3)

p3.plot(time_seconds, roll,  color='#375623', linewidth=1.5)
p3.set_ylabel('Roll (degrees)', fontsize=11)
p3.set_xlabel('Time (seconds)', fontsize=11)
p3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/yaw_pitch_roll.png', dpi=150, bbox_inches='tight')
plt.show()
print("Done. Plot saved to results folder.")