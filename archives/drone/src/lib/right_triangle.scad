function RT_calc_side_with_c(x, c) =
  sqrt(pow(c, 2) - pow(x, 2));

function RT_calc_c_with_a_b(a, b) =
  sqrt(pow(a, 2) + pow(b, 2));

function RT_calc_a_with_c_alpha(c, alpha) =
  c * sin(alpha);

function RT_calc_a_with_c_beta(c, beta) =
  c * cos(beta);

function RT_calc_a_with_b_alpha(b, alpha) =
  b * tan(alpha);

function RT_calc_b_with_c_alpha(c, alpha) =
  c * cos(alpha);

function RT_calc_alpha_with_a_b(a, b) =
  atan(a / b);

function RT_calc_alpha_with_a_c(a, c) =
  asin(a / c);

function RT_calc_alpha_with_b_c(b, c) =
  acos(b / c);

function RT_calc_a_with_b_alpha(b, alpha) =
  b * tan(alpha);