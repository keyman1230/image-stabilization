cx, cy = 980, 540
f = 6.6
pitch_x = 0.0048
pitch_y = 0.0048
fx = f / pitch_x
fy = f / pitch_y


intrinsic_matrix = np.full((3, 3), 0.0)
intrinsic_matrix[0, 0] = fx
intrinsic_matrix[1, 1] = fy
intrinsic_matrix[0, 2] = cx
intrinsic_matrix[1, 2] = cy