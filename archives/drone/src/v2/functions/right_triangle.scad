//! Right Triangle Geometry Functions
//! Standard triangle naming: opposite (side opposite angle), adjacent (side adjacent to angle), hypotenuse
//! All angle parameters are in degrees (converted to radians internally)

//! Calculate the other side of a right triangle given one side and the hypotenuse
//! @param known_side One known side length
//! @param hypotenuse Hypotenuse length
//! @returns The length of the other side
function calc_side_from_hypotenuse(known_side, hypotenuse) =
  sqrt(pow(hypotenuse, 2) - pow(known_side, 2));

//! Calculate the hypotenuse from two sides (Pythagorean theorem)
//! @param side_a Length of first side
//! @param side_b Length of second side
//! @returns Hypotenuse length
function calc_hypotenuse(side_a, side_b) =
  sqrt(pow(side_a, 2) + pow(side_b, 2));

//! Calculate the opposite side from hypotenuse and angle
//! @param hypotenuse Hypotenuse length
//! @param angle_deg Angle in degrees
//! @returns Length of side opposite the angle
function calc_opposite_from_hypotenuse(hypotenuse, angle_deg) =
  hypotenuse * sin(angle_deg);

//! Calculate the adjacent side from hypotenuse and angle
//! @param hypotenuse Hypotenuse length
//! @param angle_deg Angle in degrees
//! @returns Length of side adjacent to the angle
function calc_adjacent_from_hypotenuse(hypotenuse, angle_deg) =
  hypotenuse * cos(angle_deg);

//! Calculate the opposite side from adjacent side and angle
//! @param adjacent Length of adjacent side
//! @param angle_deg Angle in degrees
//! @returns Length of side opposite the angle
function calc_opposite_from_adjacent(adjacent, angle_deg) =
  adjacent * tan(angle_deg);

//! Calculate the adjacent side from opposite side and angle
//! @param opposite Length of opposite side
//! @param angle_deg Angle in degrees
//! @returns Length of side adjacent to the angle
function calc_adjacent_from_opposite(opposite, angle_deg) =
  opposite / tan(angle_deg);

//! Calculate angle from opposite and adjacent sides
//! @param opposite Length of side opposite the angle
//! @param adjacent Length of side adjacent to the angle
//! @returns Angle in degrees
function calc_angle_from_sides(opposite, adjacent) =
  atan(opposite / adjacent);

//! Calculate angle from opposite side and hypotenuse
//! @param opposite Length of side opposite the angle
//! @param hypotenuse Hypotenuse length
//! @returns Angle in degrees
function calc_angle_from_opposite_hypotenuse(opposite, hypotenuse) =
  asin(opposite / hypotenuse);

//! Calculate angle from adjacent side and hypotenuse
//! @param adjacent Length of side adjacent to the angle
//! @param hypotenuse Hypotenuse length
//! @returns Angle in degrees
function calc_angle_from_adjacent_hypotenuse(adjacent, hypotenuse) =
  acos(adjacent / hypotenuse);

// Legacy function names for backward compatibility (deprecated - use new names)
function RT_calc_side_with_c(x, c) = calc_side_from_hypotenuse(x, c);
function RT_calc_c_with_a_b(a, b) = calc_hypotenuse(a, b);
function RT_calc_a_with_c_alpha(c, alpha) = calc_opposite_from_hypotenuse(c, alpha);
function RT_calc_a_with_c_beta(c, beta) = calc_adjacent_from_hypotenuse(c, beta);
function RT_calc_a_with_b_alpha(b, alpha) = calc_opposite_from_adjacent(b, alpha);
function RT_calc_b_with_c_alpha(c, alpha) = calc_adjacent_from_hypotenuse(c, alpha);
function RT_calc_alpha_with_a_b(a, b) = calc_angle_from_sides(a, b);
function RT_calc_alpha_with_a_c(a, c) = calc_angle_from_opposite_hypotenuse(a, c);
function RT_calc_alpha_with_b_c(b, c) = calc_angle_from_adjacent_hypotenuse(b, c);