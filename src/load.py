def load(file_name):
	with open(file_name, "r") as f:
		lines = f.readlines()

	# Extract robot starting position
	robot_pos = tuple(map(int, lines[0].split()[2][1:-1].split(",")))

	# Extract points to visit
	points_to_visit = []
	obstacles = []
	for line in lines[1:]:
		if line.startswith("X"):
			obstacle_coords = []
			for coord in line.split()[2:]:
				obstacle_coords.append(tuple(map(int, coord[1:-1].split(","))))
			obstacles.append(obstacle_coords)
		else:
			point = tuple(map(int, line.split()[2][1:-1].split(",")))
			points_to_visit.append(point)

	return (robot_pos, points_to_visit, obstacles)