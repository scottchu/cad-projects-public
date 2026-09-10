include <../../spec/sma.scad>

function enough_space(value) =
  value > SMA_DIAMETER_REQUIRED ? 1 : 0;


