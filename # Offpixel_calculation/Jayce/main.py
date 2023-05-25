import numpy as np

def Make_Rot_Mat(yaw_deg, pitch_deg, roll_deg):
    yaw_rad = yaw_deg * np.pi / 180
    pitch_rad = pitch_deg * np.pi / 180
    roll_rad = roll_deg * np.pi / 180

    R_yaw = np.array([
        [np.cos(yaw_rad), -np.sin(yaw_rad), 0],
        [np.sin(yaw_rad), np.cos(yaw_rad), 0],
        [0, 0, 1]
    ])

    R_pitch = np.array([
        [np.cos(pitch_rad), 0, np.sin(pitch_rad)],
        [0, 1, 0],
        [-np.sin(pitch_rad), 0, np.cos(pitch_rad)]
    ])

    R_roll = np.array([
        [1, 0, 0],
        [0, np.cos(roll_rad), -np.sin(roll_rad)],
        [0, np.sin(roll_rad), np.cos(roll_rad)]
    ])

    R = R_yaw @ R_pitch @ R_roll
    return R

# position
P = np.full((3, 1), 0.0)
P[0, 0], P[1, 0], P[2, 0] = 1000, 500, 500 # 왼쪽 위 패치의 경우

# rotation
yaw_deg, pitch_deg, roll_deg = 0.5, -0.5, 0

R1 = Make_Rot_Mat(yaw_deg=0.5, pitch_deg=-0.5, roll_deg=0)
R2 = Make_Rot_Mat(yaw_deg=-0.5, pitch_deg=0.5, roll_deg=0)

P1 = R1 @ P
P2 = R2 @ P

f = 6.6
pitch_x = 0.0048
pitch_y = 0.0048

p1 = P1 * (f / P1[0, 0])
p2 = P2 * (f / P2[0, 0])
