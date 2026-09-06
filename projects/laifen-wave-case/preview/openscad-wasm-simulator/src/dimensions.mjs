/** Source-coordinate anchors on the y=0 section; dimensions describe generated values. */
export function dimensionAnchor(values,dimension) {
  const D=values.body_bore,T=values.floor_thickness,H=values.device_length+values.axial_allowance,W=(values.outer_diameter-D)/2;
  const seam=H+2*T-values.split_distance_from_top;
  // The adapter requires seam>T+2. The midpoint lies above the floor and
  // below the thread/shoulder; T also exceeds the immutable end chamfer.
  const sectionZ=(T+seam)/2;
  if(dimension==='diameter')return {a:[-D/2,0,sectionZ],b:[D/2,0,sectionZ],label:`Inside diameter ${D} mm`};
  if(dimension==='wall')return {a:[D/2,0,sectionZ],b:[D/2+W,0,sectionZ],label:`Wall thickness ${W} mm`};
  if(dimension==='ends') {
    // All seven hole centers lie at radius <= ring. Stay beyond their outer
    // radial envelope and inside the bore, also clear of the outer chamfer.
    const x=(values.drain_ring_radius+values.drain_diameter/2+D/2)/2;
    return {a:[x,0,0],b:[x,0,T],label:`Top & bottom ${T} mm`};
  }
  return {a:[0,0,T],b:[0,0,H+T],label:`Inside height ${H} mm`};
}
