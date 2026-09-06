/*
 Laifen two-piece travel case — OpenSCAD Customizer V1.
 Original source-native geometry.  This is an editable customizer target, not
 a replacement for the reviewed build123d P1 R7 STEP authority.
*/

/* [Preset / device] */
device_length = 208;          // [1:1:300]
device_diameter = 29;         // [1:0.1:80] Reference only; bores are explicit.
axial_allowance = 5;          // [3:0.5:30]

/* [Envelope] */
outer_diameter = 39;          // [20:0.1:80]
body_bore = 30;               // [10:0.1:70]
cap_bore = 31;                // [10:0.1:70]
minimum_wall = 2.4;           // [1.8:0.1:6] Constraint/readout; bores and OD drive geometry.
floor_thickness = 3;          // [2:0.1:8]
end_chamfer = 1.2;            // [0.8:0.1:1.5]

/* [Split — one canonical source] */
split_mode = "distance";      // [distance:Distance from top,percentage:Percent from top]
split_distance_from_top = 84; // [20:0.1:250]
split_percent_from_top = 38.356; // [5:0.1:95] Used only in percentage mode.

/* [Thread] */
thread_pitch = 2;             // [1:0.1:5]
thread_turns = 3;             // [1:0.25:6]
thread_clearance = 0.25;      // [0.20:0.01:0.30]
thread_depth = 0.5;           // [0.25:0.05:1]
thread_root_wall = 1.4;       // [1.0:0.1:3]

/* [Surface] */
surface_style = "diamond";    // [smooth:Smooth,diamond:Diamond,ribs:Ribs,rings:Rings,spiral:Spiral]
diamond_axial_pitch = 4.8;    // [4.8:0.1:8]
diamond_arc_pitch = 3.63;     // [2:0.01:8]
diamond_depth = 0.45;         // [0.1:0.05:0.6]
diamond_phase_deg = 0;        // [0:1:360]
diamond_plateau_half_fraction = 0.18; // [0.10:0.01:0.30] Dimensionless half-fraction.
wave_spacing = 6.0;            // [4:0.1:16]
wave_depth = 0.45;             // [0.1:0.05:0.6]

/* [Drainage] */
drainage_mode = "bottom";    // [none:No drains,top:Cap closed-end drains,bottom:Body closed-end drains,both:Both closed-end drains]
drain_diameter = 3;           // [1:0.1:5]
drain_ring_radius = 9;        // [2:0.1:14]
drain_count = 7;              // [1:1:24] Center plus equally spaced ring holes.

/* [Output] */
output_mode = "assembled";   // [assembled:Closed assembly,body:Body only,cap:Cap only,print_layout:Print layout]
$fn = 96;
VFR04_PROBE_MODE = ""; // Hidden executable-math witness; not a public output mode.
VFR04_PROBE_HEIGHT = 7.13;
VFR04_PROBE_GLOBAL_OFFSET = 131.93;

// ----- one derivation layer -----
cavity_length = device_length + axial_allowance;
engagement = thread_pitch * thread_turns;
closure_overlap = engagement + 3;
closed_length = cavity_length + 2 * floor_thickness;
cap_height = split_mode == "percentage" ? closed_length * split_percent_from_top / 100 : split_distance_from_top;
body_height = closed_length - cap_height + closure_overlap;
body_thread_z = body_height - closure_overlap;
cap_close_z = body_height - closure_overlap;
outer_radius = outer_diameter / 2;
valley_radius = outer_radius - diamond_depth;
body_inner_radius = body_bore / 2;
cap_inner_radius = cap_bore / 2;
thread_root_radius = body_inner_radius + thread_root_wall;
thread_crest_radius = thread_root_radius + thread_depth;
// Internal Boolean overlap, deliberately smaller than print clearance.  It
// joins each helical root to its cylinder without moving either crest.
THREAD_EMBED_EPS = .05;
DRAIN_LIGAMENT = .4;
thread_transition = (closure_overlap-engagement)/2;

// VFR-04 pure field contract.  Both component callers use global Z relative
// to the same seam; no local phase or axial scaling is permitted.
function diamond_finite(x) = is_num(x) && x == x && abs(x) < 1e100;
function diamond_count(r_valley, target_arc) = floor(2 * PI * r_valley / target_arc + 0.5);
function diamond_wrap(t) = t - floor(t + 0.5);
function diamond_coordinates(theta_deg, z_global, phase_deg, seam_z, count, axial_pitch) =
  [count * (theta_deg - phase_deg) / 360, (z_global - seam_z) / axial_pitch];
function diamond_field(u, v, plateau_half_fraction) =
  let(m=max(abs(diamond_wrap(u+v)), abs(diamond_wrap(u-v))))
  min(1, max(0, (0.5-m)/(0.5-plateau_half_fraction)));
function diamond_radius(r_valley, depth, u, v, plateau_half_fraction) =
  r_valley + depth * diamond_field(u, v, plateau_half_fraction);
function diamond_global_z(role, local_z, seam_z) = role == "cap" ? seam_z + local_z : local_z;
function diamond_patch_coordinates(s, t) = [(s+t)/2, (s-t)/2];
function diamond_patch_inverse(u, v) = [u+v, u-v];
function diamond_plateau_width(actual_arc, axial_pitch, plateau_half_fraction) =
  2 * plateau_half_fraction * actual_arc * axial_pitch / sqrt(actual_arc*actual_arc + axial_pitch*axial_pitch);
function diamond_axial_slope(depth, axial_pitch, plateau_half_fraction) =
  depth / (axial_pitch * (0.5-plateau_half_fraction));

DIAMOND_ANGULAR_SUBDIVISIONS = 8;
DIAMOND_MAX_EXTERIOR_TRIANGLES = 250000;
diamond_lattice_count = diamond_count(valley_radius, diamond_arc_pitch);
diamond_actual_arc_pitch = 2 * PI * valley_radius / diamond_lattice_count;
diamond_default_plateau_width = diamond_depth == 0 ? 0 : diamond_plateau_width(diamond_actual_arc_pitch, diamond_axial_pitch, diamond_plateau_half_fraction);
diamond_default_axial_slope = diamond_depth == 0 ? 0 : diamond_axial_slope(diamond_depth, diamond_axial_pitch, diamond_plateau_half_fraction);
function diamond_angular_segments(count) = count * DIAMOND_ANGULAR_SUBDIVISIONS;
function diamond_axial_segments(height, axial_pitch) = ceil(height / (axial_pitch / DIAMOND_ANGULAR_SUBDIVISIONS));
function diamond_triangle_estimate(height, count, axial_pitch) =
  let(n=diamond_angular_segments(count), m=diamond_axial_segments(height, axial_pitch))
  2*n*m + 2*n;

assert(device_length > 0 && axial_allowance >= 3, "device/cavity dimensions invalid");
assert(cavity_length >= 2 * floor_thickness + engagement + 3, "insufficient cavity/end-clearance budget");
assert(outer_diameter > max(body_bore, cap_bore) + 2 * minimum_wall, "OD must exceed bores + 2*minimum wall");
assert(end_chamfer > 0 && end_chamfer < floor_thickness, "chamfer must remain inside floor");
assert(thread_pitch > 0 && thread_turns > 0 && thread_depth > 0, "thread values invalid");
assert(thread_clearance >= .20 && thread_clearance <= .30, "thread clearance must be 0.20–0.30 mm/side");
assert(cap_height > floor_thickness + closure_overlap + 2 && body_height > floor_thickness + closure_overlap + 2, "split leaves no floor/closure transition");
assert(drain_count == floor(drain_count) && drain_count >= 1 && drain_count <= 24, "drain count must be an integer in [1,24]");
assert(drain_diameter >= 1 && drain_diameter <= 5 && drain_ring_radius >= 2 && drain_ring_radius <= 14, "drain dimensions outside customizer range");
assert(drainage_mode == "none" || min(body_inner_radius,cap_inner_radius)-drain_diameter/2 >= DRAIN_LIGAMENT, "drain center ligament below 0.4mm");
assert(drainage_mode == "none" || drain_count < 2 || (min(body_inner_radius,cap_inner_radius)-(drain_ring_radius+drain_diameter/2) >= DRAIN_LIGAMENT && drain_ring_radius-drain_diameter >= DRAIN_LIGAMENT), "drain ring ligament below 0.4mm");
assert(drainage_mode == "none" || drain_count < 3 || 2*drain_ring_radius*sin(180/(drain_count-1))-drain_diameter >= DRAIN_LIGAMENT, "adjacent drain ligament below 0.4mm");
assert(closure_overlap > 0 && body_height > closure_overlap + floor_thickness, "body/thread interval invalid");
assert(outer_radius - (thread_crest_radius + thread_clearance) >= 1.8, "threaded cap wall below 1.8mm");
assert(thread_root_wall >= 1.2, "male root wall below 1.2mm");
assert(THREAD_EMBED_EPS > 0 && THREAD_EMBED_EPS < min(thread_depth, thread_clearance), "thread embed epsilon invalid");
assert(surface_style != "diamond" || diamond_depth == 0 ||
       (diamond_finite(diamond_axial_pitch) && diamond_finite(diamond_arc_pitch) && diamond_finite(diamond_depth) &&
        diamond_finite(diamond_phase_deg) && diamond_finite(diamond_plateau_half_fraction)),
       "diamond values must be finite");
assert(surface_style != "diamond" || diamond_depth == 0 || (diamond_lattice_count >= 8 && diamond_lattice_count <= 128),
       "diamond count must be in [8,128]");
assert(surface_style != "diamond" || diamond_depth == 0 ||
       (diamond_plateau_half_fraction > 0 && diamond_plateau_half_fraction < 0.5 && diamond_default_plateau_width >= 1),
       "diamond plateau developed width below 1.0mm");
assert(surface_style != "diamond" || diamond_depth == 0 || diamond_default_axial_slope <= 1,
       "diamond axial slope exceeds 1");
assert(surface_style != "diamond" || diamond_depth == 0 ||
       (valley_radius-body_inner_radius >= minimum_wall && valley_radius-cap_inner_radius >= minimum_wall),
       "diamond valley shell wall below minimum_wall");
assert(surface_style != "diamond" || diamond_depth == 0 ||
       valley_radius-(thread_crest_radius+thread_clearance) >= 1.8,
       "diamond female thread valley wall below 1.8mm");
assert(surface_style != "diamond" || diamond_depth == 0 ||
       valley_radius-(thread_root_radius+thread_clearance+.4) >= 1.8,
       "diamond female entry relief wall below 1.8mm");
assert(surface_style != "diamond" || diamond_depth == 0 ||
       (diamond_triangle_estimate(body_thread_z, diamond_lattice_count, diamond_axial_pitch) <= DIAMOND_MAX_EXTERIOR_TRIANGLES &&
        diamond_triangle_estimate(cap_height, diamond_lattice_count, diamond_axial_pitch) <= DIAMOND_MAX_EXTERIOR_TRIANGLES),
       "diamond exterior triangle estimate exceeds cap");
assert(!wave_active() ||
       (diamond_finite(wave_spacing) && diamond_finite(wave_depth) && wave_spacing >= 4 && wave_spacing <= 16 && wave_depth >= .1 && wave_depth <= .6),
       "wave values invalid");
assert(!wave_active() ||
       len([for(x=[outer_radius,body_inner_radius,cap_inner_radius,body_thread_z,cap_height,end_chamfer,minimum_wall,thread_crest_radius,thread_clearance])if(!diamond_finite(x))1])==0,
       "wave dimensions must be finite");
// PF-R1: additive OD requirements retain exact boundary equality without an epsilon.
assert(!wave_active() ||
       (outer_diameter >= body_bore+2*(minimum_wall+wave_depth+.01) &&
        outer_diameter >= cap_bore+2*(minimum_wall+wave_depth+.01) &&
        outer_diameter >= body_bore+2*((thread_root_wall+thread_depth+thread_clearance+1.8)+wave_depth+.01) &&
        outer_diameter >= body_bore+2*((thread_root_wall+thread_clearance+.4+1.8)+wave_depth+.01)),
       "wave valley ligament below minimum including chord reserve");
assert(!wave_active() ||
       (wave_triangle_estimate(body_thread_z)<=250000 && wave_triangle_estimate(cap_height)<=250000),
       "wave exterior triangle estimate exceeds cap");

assert(surface_style!="ribs" || wave_rib_count>=3,"ribs require at least three ridges");
assert(surface_style!="diamond" || (diamond_axial_pitch>=4.8 && diamond_axial_pitch<=8 && diamond_depth>=.1 && diamond_depth<=.6),"diamond control range invalid");
assert(surface_style!="diamond" || (diamond_arc_pitch==(diamond_axial_pitch==4.8?3.63:diamond_axial_pitch*(3.63/4.8)) && diamond_phase_deg==0 && diamond_plateau_half_fraction==.18),"diamond derived values changed");

module drain_pattern(h) {
  // VFR-08: callers provide the complete bounded axial interval.
  cylinder(d=drain_diameter, h=h, center=false);
  if (drain_count >= 2) for (i=[0:drain_count-2]) let(a=360*i/(drain_count-1)) translate([drain_ring_radius*cos(a), drain_ring_radius*sin(a), 0]) cylinder(d=drain_diameter, h=h, center=false);
}

// VFR-06: periodic knot lattice; all cuts owned by primitive numeric slots.
DIAMOND_UV_EPS=1e-10;
function diamond_quantize(x)=round(x*1e8)/1e8;
function diamond_sum(a,i=0,s=0)=i>=len(a)?s:diamond_sum(a,i+1,s+a[i]);
function v06_mod(x,n)=x-floor(x/n)*n;
function v06_k(p)=floor(p/3)+[-.5,-diamond_plateau_half_fraction,diamond_plateau_half_fraction][v06_mod(p,3)];
function v06_sgn(x)=abs(x)<=DIAMOND_UV_EPS?0:x<0?-1:1;
function v06_cfg(v0,v1,offset,role="none",height=0)=
  let(lo=floor(-6*v1)-3,hi=ceil(-6*v0)+3,R=hi-lo+1)
  assert(v1-v0>DIAMOND_UV_EPS,"V06 collapsed strip")
  [v0,v1,offset,role,height,lo,hi,R,3*(R+2),3*(3*R+2),6*R];
function v06_b(p,d,c)=[3*(d-c[5]+1)+v06_mod(p,3),floor(p/3)];
function v06_e(kind,p,d,c)=[kind==0?3*(d-c[5])+v06_mod(p,3):kind==1?3*(c[7]+1)+3*(d-c[5]+1)+v06_mod(p,3):6*(c[7]+1)+3*(d-c[5])+v06_mod(p,3),floor(p/3)];
function v06_q(v,c)=c[3]=="body"?outer_radius-end_chamfer+body_thread_z+diamond_axial_pitch*v:
  c[3]=="cap"?outer_radius-end_chamfer+c[4]-diamond_axial_pitch*v:
  c[3]=="trim_band"?outer_radius-end_chamfer+diamond_axial_pitch*(v-c[0]):1e6;
// Point data [owner slot, sector carry, u, v, affine field radius, h].
function v06_point(ref,uv,c)=let(v=abs(uv[1]-c[0])<=DIAMOND_UV_EPS?c[0]:abs(uv[1]-c[1])<=DIAMOND_UV_EPS?c[1]:uv[1],
  r=diamond_radius(valley_radius,diamond_depth,uv[0],v,diamond_plateau_half_fraction))
  [ref[0],ref[1],uv[0],v,r,r-v06_q(v,c)];
function v06_base(slot,c)=let(d=floor(slot/3)+c[5]-1,p=slot%3)
  v06_point([slot,0],diamond_patch_coordinates(v06_k(p),v06_k(p+d)),c);
function v06_shift(a,k)=[a[0],a[1]+k,a[2]+k,a[3],a[4],a[5]];
function v06_refbase(ref,b)=v06_shift(b[ref[0]],ref[1]);
function v06_anti(p,d)=let(x=v06_mod(p,3),y=v06_mod(p+d,3))(x==0&&y==2)||(x==2&&y==0);
function v06_edge_bases(e,c,b)=let(n=3*(c[7]+1),kind=e<n?0:e<2*n?1:2,t=e-kind*n,
  p=t%3,d=floor(t/3)+c[5]-(kind==1?1:0),
  refs=kind==0?[v06_b(p,d,c),v06_b(p+1,d-1,c)]:kind==1?[v06_b(p,d,c),v06_b(p,d+1,c)]:
    v06_anti(p,d)?[v06_b(p+1,d-1,c),v06_b(p,d+1,c)]:[v06_b(p,d,c),v06_b(p+1,d,c)])
  [for(ref=refs)v06_refbase(ref,b)];
function v06_lerp(a,b,t,slot)=[slot,0,a[2]+t*(b[2]-a[2]),a[3]+t*(b[3]-a[3]),a[4]+t*(b[4]-a[4]),a[5]+t*(b[5]-a[5])];
function v06_cut(a,b,cut,e,c)=let(z=c[cut],sa=v06_sgn(a[3]-z),sb=v06_sgn(b[3]-z))
  sa==0?a:sb==0?b:sa==sb?undef:
  let(x=v06_lerp(a,b,(z-a[3])/(b[3]-a[3]),c[8]+cut*c[9]+e)) [x[0],0,x[2],z,x[4],x[5]];
function v06_trim(a,b,e,c,ac)=let(sa=v06_sgn(a[5]),sb=v06_sgn(b[5]))
  sa==0?a:sb==0?b:sa==sb?undef:
  let(x=v06_lerp(a,b,-a[5]/(b[5]-a[5]),c[8]+2*c[9]+e))
  abs(x[3]-c[0])<=DIAMOND_UV_EPS?ac[0]:abs(x[3]-c[1])<=DIAMOND_UV_EPS?ac[1]:
  x[3]<c[0]||x[3]>c[1]?undef:[x[0],0,x[2],x[3],x[4],0];
function v06_edge_data(e,c,b)=let(ab=v06_edge_bases(e,c,b),ac=[for(cut=[0:1])v06_cut(ab[0],ab[1],cut,e,c)])
  [ab,ac[0],ac[1],v06_trim(ab[0],ab[1],e,c,ac)];
// Face local masks contain the indices of incident original edges/cuts.
function v06_record(p,edges=[],cuts=[])=[p,edges,cuts];
function v06_common(a,b)=[for(x=a)if(len([for(y=b)if(x==y)1])>0)x];
function v06_same(a,b)=a[0][0]==b[0][0]&&a[0][1]==b[0][1];
function v06_clean(p)=len(p)==0?[]:let(q=[for(i=[0:len(p)-1])if(!v06_same(p[i],p[(i+len(p)-1)%len(p)]))p[i]])q;
function v06_cell(f,c)=let(cell=floor(f/2),p=cell%3,d=floor(cell/3)+c[5],j=f%2,
  A=v06_b(p,d,c),B=v06_b(p+1,d-1,c),C=v06_b(p+1,d,c),D=v06_b(p,d+1,c),
  ab=v06_e(0,p,d,c),bc=v06_e(1,p+1,d-1,c),cd=v06_e(0,p,d+1,c),da=v06_e(1,p,d,c),diag=v06_e(2,p,d,c))
  v06_anti(p,d)?(j==0?[[A,B,D],[ab,diag,da]]:[[B,C,D],[bc,cd,diag]]):
    (j==0?[[A,B,C],[ab,bc,diag]]:[[A,C,D],[diag,cd,da]]);
function v06_intersect(a,b,axis,cut,f,edgeRefs,ed,c)=
  let(common=v06_common(a[1],b[1]),cuts=v06_common(a[2],b[2]),
    aa=a[0],bb=b[0],limit=axis==3?c[cut]:0,
    t=(limit-aa[axis])/(bb[axis]-aa[axis]))
  abs(t)<=DIAMOND_UV_EPS?a:abs(t-1)<=DIAMOND_UV_EPS?b:
  len(common)>0?let(er=edgeRefs[common[0]],data=ed[er[0]][axis==3?1+cut:3])
    assert(!is_undef(data),"V06 missing edge owner")
    v06_record(v06_shift(data,er[1]),common,axis==3?[cut]:cuts):
  assert(axis==5&&len(cuts)==1,"V06 intersection class")
  let(x=v06_lerp(aa,bb,t,c[8]+3*c[9]+2*f+cuts[0]))v06_record([x[0],0,x[2],x[3],x[4],0],[],cuts);
function v06_clip(poly,axis,cut,greater,f,refs,ed,c)=len(poly)==0?[]:v06_clean(
  [for(i=[0:len(poly)-1])let(a=poly[i],b=poly[(i+1)%len(poly)],
    sa=v06_sgn(a[0][axis]-(axis==3?c[cut]:0)),sb=v06_sgn(b[0][axis]-(axis==3?c[cut]:0)),
    pin=greater?sa>=0:sa<=0,qin=greater?sb>=0:sb<=0)
  each pin&&qin?[b]:pin&&!qin?[v06_intersect(a,b,axis,cut,f,refs,ed,c)]:
    !pin&&qin?[v06_intersect(a,b,axis,cut,f,refs,ed,c),b]:[]]);
function v06_area(poly)=len(poly)<3?0:abs(diamond_sum([for(i=[0:len(poly)-1])
  poly[i][0][2]*poly[(i+1)%len(poly)][0][3]-poly[(i+1)%len(poly)][0][2]*poly[i][0][3]]))/2;
function v06_valid(poly)=v06_area(poly)>DIAMOND_UV_EPS?poly:[];
function v06_face(f,c,b,ed)=let(cell=v06_cell(f,c),raw=[for(i=[0:2])let(p=v06_refbase(cell[0][i],b))
  v06_record(p,[(i+2)%3,i],[for(cut=[0:1])if(abs(p[3]-c[cut])<=DIAMOND_UV_EPS)cut])],
  axial=v06_valid(v06_clip(v06_clip(raw,3,0,true,f,cell[1],ed,c),3,1,false,f,cell[1],ed,c)),
  signs=[for(p=axial)v06_sgn(p[0][5])],neg=len([for(s=signs)if(s<0)1])>0,pos=len([for(s=signs)if(s>0)1])>0)
  neg&&pos?[v06_valid(v06_clip(axial,5,0,false,f,cell[1],ed,c)),v06_valid(v06_clip(axial,5,0,true,f,cell[1],ed,c))]:
    pos?[[],axial]:[axial,[]];
function v06_center(poly,slot)=len(poly)<4?undef:[slot,0,for(axis=[2:5])diamond_sum([for(p=poly)p[0][axis]])/len(poly)];
function v06_owned(p,slot)=!is_undef(p)&&p[0]==slot&&p[1]==0?p:undef;
function v06_u(f,cut,polys,c)=let(slot=c[8]+3*c[9]+2*f+cut,found=[for(poly=polys)for(p=poly)if(p[0][0]==slot)p[0]])
  len(found)>0?found[0]:undef;
function v06_slots(c,b,ed,fs)=concat(
  [for(p=b)p[3]>=c[0]&&p[3]<=c[1]?p:undef],
  [for(kind=[0:2])for(e=[0:c[9]-1])v06_owned(ed[e][kind+1],c[8]+kind*c[9]+e)],
  [for(f=[0:c[10]-1])for(cut=[0:1])v06_u(f,cut,fs[f],c)],
  [for(f=[0:c[10]-1])for(branch=[0:1])v06_center(fs[f][branch],c[8]+3*c[9]+2*c[10]+2*f+branch)]);
// Exclusive prefix, one divide-and-conquer traversal, logarithmic stack depth.
function v06_prefix(a,lo=0,hi=undef)=let(end=is_undef(hi)?len(a):hi,n=end-lo)
  n==0?[[],0]:n==1?[[0],a[lo]]:let(mid=lo+floor(n/2),l=v06_prefix(a,lo,mid),r=v06_prefix(a,mid,end))
  [concat(l[0],[for(x=r[0])x+l[1]]),l[1]+r[1]];
function v06_index(p,rank,k=0)=diamond_lattice_count*rank[p[0]]+v06_mod(p[1]+k,diamond_lattice_count);
function v06_xyz(p,k,c)=let(theta=diamond_phase_deg+360*(p[2]+k)/diamond_lattice_count,r=min(p[4],v06_q(p[3],c)))
  [diamond_quantize(r*cos(theta)),diamond_quantize(r*sin(theta)),diamond_quantize(body_thread_z+diamond_axial_pitch*p[3]-c[2])];
function v06_poly_faces(poly,center,rank,k)=len(poly)==0?[]:len(poly)==3?[[for(p=poly)v06_index(p[0],rank,k)]]:
  [for(i=[0:len(poly)-1])[v06_index(center,rank,k),v06_index(poly[i][0],rank,k),v06_index(poly[(i+1)%len(poly)][0],rank,k)]];
function v06_sort(a)=len(a)<=1?a:let(p=a[floor(len(a)/2)][0])concat(v06_sort([for(x=a)if(x[0]<p)x]),[for(x=a)if(x[0]==p)x],v06_sort([for(x=a)if(x[0]>p)x]));
function v06_ring(c,fs,cut)=let(z=c[cut],near=[for(f=[0:c[10]-1])let(d=floor(f/6)+c[5])if(d>=floor(-6*z)-3&&d<=ceil(-6*z)+3)f],
  raw=[for(f=near)for(poly=fs[f])for(p=poly)if(abs(p[0][3]-z)<=DIAMOND_UV_EPS)
    let(u=p[0][2],whole=floor(u+DIAMOND_UV_EPS),frac=u-whole)
    [abs(frac)<=DIAMOND_UV_EPS?0:frac,[p[0][0],p[0][1]-whole]]],sorted=v06_sort(raw))
  [for(i=[0:len(sorted)-1])each i==0||abs(sorted[i][0]-sorted[i-1][0])>DIAMOND_UV_EPS?[sorted[i]]:
    assert(sorted[i][1]==sorted[i-1][1],"V06 ring nonalias coincidence")[]];
// Data layout: points, inward SCAD side faces, endpoint rings, config, slots,
// rank, source face polygons. Production and private proofs call this function.
function v06_data(v0,v1,offset,role="none",height=0)=let(c=v06_cfg(v0,v1,offset,role,height),
  b=[for(slot=[0:c[8]-1])v06_base(slot,c)],ed=[for(e=[0:c[9]-1])v06_edge_data(e,c,b)],
  fs=[for(f=[0:c[10]-1])v06_face(f,c,b,ed)],slots=v06_slots(c,b,ed,fs),
  prefix=v06_prefix([for(p=slots)is_undef(p)?0:1]),rank=prefix[0],
  points=[for(p=slots)if(!is_undef(p))for(k=[0:diamond_lattice_count-1])v06_xyz(p,k,c)],
  faces=[for(f=[0:c[10]-1])for(branch=[0:1])for(k=[0:diamond_lattice_count-1])each
    v06_poly_faces(fs[f][branch],slots[c[8]+3*c[9]+2*c[10]+2*f+branch],rank,k)])
  [points,faces,[for(cut=[0:1])v06_ring(c,fs,cut)],c,slots,rank,fs];
function v06_ring_indices(data,cut)=let(r=data[2][cut])
  [for(k=[0:diamond_lattice_count-1])for(t=r)v06_index(t[1],data[5],k)];
function v06_disk(ring,center,positive)= [for(i=[0:len(ring)-1])positive?[center,ring[(i+1)%len(ring)],ring[i]]:[center,ring[i],ring[(i+1)%len(ring)]]];
function v06_closed_band(data)=let(n=len(data[0]),c=data[3],points=concat(data[0],[[0,0,body_thread_z+diamond_axial_pitch*c[0]-c[2]],[0,0,body_thread_z+diamond_axial_pitch*c[1]-c[2]]]),
  faces=concat(data[1],v06_disk(v06_ring_indices(data,0),n,false),v06_disk(v06_ring_indices(data,1),n+1,true))) [points,faces];
module diamond_exterior(z1,global_offset) {
  data=v06_data((global_offset-body_thread_z)/diamond_axial_pitch,(global_offset+z1-body_thread_z)/diamond_axial_pitch,global_offset);
  mesh=v06_closed_band(data); polyhedron(points=mesh[0],faces=mesh[1],convexity=10);
}

// PF-DIRECT: sector-specific sampled field with shared chamfer edge ownership.
// Every horizontal, vertical and diagonal grid edge owns at most one trim
// intersection. Both sides of the cusp use that same index. All faces use the
// existing v06 inward SCAD winding; the inner profile/zipper are unchanged.
function wave_active()=surface_style=="ribs"||surface_style=="rings"||surface_style=="spiral";
wave_rib_count=floor(2*PI*(outer_radius-wave_depth)/wave_spacing+.5);
WAVE_ANGULAR_SAMPLES=surface_style=="ribs"?max(192,32*wave_rib_count):192;
function wave_segments(h)=surface_style=="ribs"?1:ceil(h/(wave_spacing/16));
function wave_triangle_estimate(h)=let(n=WAVE_ANGULAR_SAMPLES,m=wave_segments(h))
  2*n*(m+2)+4*n*min(m+1,ceil(end_chamfer*m/h)+2)+2*n;
function wave_radius(theta,z_global)=outer_radius-wave_depth*(1-cos(surface_style=="ribs"?wave_rib_count*theta:surface_style=="rings"?360*(z_global-body_thread_z)/wave_spacing:6*theta-360*(z_global-body_thread_z)/wave_spacing))/2;
function wave_cone(z,h,role)=outer_radius-max(0,end_chamfer-(role=="body"?z:h-z));
function wave_rows(h,role)=let(m=wave_segments(h),br=role=="body"?end_chamfer:h-end_chamfer,
  sorted=v06_sort(concat([for(j=[0:m])[h*j/m]],[ [br] ])))
  [for(j=[0:len(sorted)-1])if(j==0||abs(sorted[j][0]-sorted[j-1][0])>DIAMOND_UV_EPS)sorted[j][0]];
// UV point data: angle, local Z, affine sampled radius, field-minus-cone.
function wave_point(col,row,zs,h,role)=let(theta=360*col/WAVE_ANGULAR_SAMPLES,z=zs[row],
  r=wave_radius(theta,(role=="body"?0:body_thread_z)+z))
  [theta,z,r,r-wave_cone(z,h,role)];
function wave_base_id(row,col)=row*WAVE_ANGULAR_SAMPLES+v06_mod(col,WAVE_ANGULAR_SAMPLES);
function wave_edge_id(kind,row,col,rows)=kind==0?wave_base_id(row,col):
  WAVE_ANGULAR_SAMPLES*rows+(kind-1)*WAVE_ANGULAR_SAMPLES*(rows-1)+wave_base_id(row,col);
function wave_edge_ends(e,zs,h,role)=let(n=WAVE_ANGULAR_SAMPLES,rows=len(zs),
  kind=e<n*rows?0:e<n*(2*rows-1)?1:2,
  t=e-(kind==0?0:n*rows+(kind-1)*n*(rows-1)),row=floor(t/n),col=t%n)
  [wave_point(col,row,zs,h,role),wave_point(col+(kind==1?0:1),row+(kind==0?0:1),zs,h,role)];
function wave_edge_cut(e,zs,h,role)=let(n=WAVE_ANGULAR_SAMPLES,rows=len(zs),kind=e<n*rows?0:e<n*(2*rows-1)?1:2,t=e-(kind==0?0:n*rows+(kind-1)*n*(rows-1)),row=floor(t/n))
  wave_cone(zs[row],h,role)==outer_radius && wave_cone(zs[row+(kind==0?0:1)],h,role)==outer_radius ? undef :
  let(ab=wave_edge_ends(e,zs,h,role),a=ab[0],b=ab[1])
  v06_sgn(a[3])*v06_sgn(b[3])!=-1?undef:
  let(t=-a[3]/(b[3]-a[3]))[for(k=[0:3])k==3?0:a[k]+t*(b[k]-a[k])];
function wave_xyz(p,h,role)=let(r=min(p[2],wave_cone(p[1],h,role)))
  [diamond_quantize(r*cos(p[0])),diamond_quantize(r*sin(p[0])),diamond_quantize(p[1])];
// Vertex records hold their primitive slot and sign; intersection slots follow
// the grid slots. The owner lookup avoids recomputing a cut from reversed edges.
function wave_clip(ids,edges,slots,positive)=v06_clean_wave([for(i=[0:2])
  let(a=ids[i],b=ids[(i+1)%3],sa=v06_sgn(slots[a][3]),sb=v06_sgn(slots[b][3]),
    ain=positive?sa>=0:sa<=0,bin=positive?sb>=0:sb<=0,
    cut=sa==0?a:sb==0?b:edges[i])
  each ain&&bin?[b]:ain&&!bin?[cut]:!ain&&bin?[cut,b]:[]]);
function v06_clean_wave(ids)=len(ids)==0?[]:[for(i=[0:len(ids)-1])if(ids[i]!=ids[(i+len(ids)-1)%len(ids)])ids[i]];
function wave_face_polys(row,col,zs,slots,h,role)=let(rows=len(zs),base=rows*WAVE_ANGULAR_SAMPLES,
  a=wave_base_id(row,col),b=wave_base_id(row,col+1),c=wave_base_id(row+1,col+1),d=wave_base_id(row+1,col),
  ab=base+wave_edge_id(0,row,col,rows),bc=base+wave_edge_id(1,row,col+1,rows),
  cd=base+wave_edge_id(0,row+1,col,rows),da=base+wave_edge_id(1,row,col,rows),
  ac=base+wave_edge_id(2,row,col,rows),
  uncut=wave_cone(zs[row],h,role)==outer_radius && wave_cone(zs[row+1],h,role)==outer_radius)
  uncut?[[a,c,b],[a,d,c]]:[for(tri=[[[a,c,b],[ac,bc,ab]],[[a,d,c],[da,cd,ac]]])
    let(signs=[for(id=tri[0])v06_sgn(slots[id][3])],
      cross=min(signs)<0&&max(signs)>0)
    each cross?[wave_clip(tri[0],tri[1],slots,false),wave_clip(tri[0],tri[1],slots,true)]:[tri[0]]];
function wave_ring(row,zs,slots,rank)=let(base=len(zs)*WAVE_ANGULAR_SAMPLES)
  [for(col=[0:WAVE_ANGULAR_SAMPLES-1])let(id=wave_base_id(row,col),
    cut=base+wave_edge_id(0,row,col,len(zs)))each
    concat([[slots[id][0],rank[id]]],is_undef(slots[cut])?[]:[[slots[cut][0],rank[cut]]])];
function wave_data(h,role)=let(zs=wave_rows(h,role),rows=len(zs),n=WAVE_ANGULAR_SAMPLES,
  slots=concat([for(row=[0:rows-1])for(col=[0:n-1])wave_point(col,row,zs,h,role)],
    [for(e=[0:n*(3*rows-2)-1])wave_edge_cut(e,zs,h,role)]),
  rank=v06_prefix([for(p=slots)is_undef(p)?0:1])[0],
  points=[for(p=slots)if(!is_undef(p))wave_xyz(p,h,role)],
  faces=[for(row=[0:rows-2])for(col=[0:n-1])for(poly=wave_face_polys(row,col,zs,slots,h,role))
    if(len(poly)>=3)for(k=[1:len(poly)-2])[rank[poly[0]],rank[poly[k]],rank[poly[k+1]]]],
  rings=[wave_ring(0,zs,slots,rank),wave_ring(rows-1,zs,slots,rank)])
  assert(len(faces)+len(rings[0])+len(rings[1])<=250000,"actual wave exterior allocation exceeds cap")
  [points,faces,rings];
function wave_direct(role)=let(body=role=="body",h=body?body_thread_z:cap_height,data=wave_data(h,role),
  profile=v06_profile(role),n=len(data[0]),center=n+96*len(profile),
  points=concat(data[0],v06_internal_points(profile),[[0,0,body?0:cap_height],[0,0,profile[len(profile)-1][1]]]),
  outerDisk=v06_disk([for(x=data[2][body?0:1])x[1]],center,!body),
  join=v06_zip(data[2][body?1:0],n,body),floorRing=[for(j=[0:95])n+96*(len(profile)-1)+j],
  faces=concat(data[1],outerDisk,join,v06_internal_faces(profile,n,!body),v06_disk(floorRing,center+1,body)))
  [points,faces];
module wave_direct_shell(role) { mesh=wave_direct(role); polyhedron(points=mesh[0],faces=mesh[1],convexity=10); }
module wave_body_shell() {
  difference() {
    union() { wave_direct_shell("body"); translate([0,0,body_thread_z+thread_transition]) body_thread(); }
    if (drainage_mode=="bottom"||drainage_mode=="both") translate([0,0,-.1]) drain_pattern(floor_thickness+.2);
  }
}
module wave_cap_shell() {
  difference() {
    wave_direct_shell("cap"); translate([0,0,thread_transition]) female_thread_groove();
    if (drainage_mode=="top"||drainage_mode=="both") translate([0,0,cap_height-floor_thickness-.1]) drain_pattern(floor_thickness+.2);
  }
}

module body_thread() {
  // right-hand active helix, centered in the 9 mm closure overlap.
  linear_extrude(height=engagement, twist=360*engagement/thread_pitch, slices=max(24,ceil(engagement/thread_pitch*24)))
    translate([thread_root_radius,0]) polygon([[-THREAD_EMBED_EPS,-thread_pitch*.32],[thread_depth,0],[-THREAD_EMBED_EPS,thread_pitch*.32]]);
}

module female_thread_void() {
  // Root clearance spans the complete overlap; only the central 6 mm is grooved.
  cylinder(r=thread_root_radius+thread_clearance, h=closure_overlap);
  // 45-degree entry/elephant-foot relief, bounded to the first 0.4 mm.
  cylinder(r1=thread_root_radius+thread_clearance+.4, r2=thread_root_radius+thread_clearance, h=.4);
}

module female_thread_groove() {
  linear_extrude(height=engagement, twist=360*engagement/thread_pitch, slices=max(24,ceil(engagement/thread_pitch*24)))
    translate([thread_root_radius+thread_clearance,0]) polygon([[-THREAD_EMBED_EPS,-thread_pitch*.32],[thread_depth,0],[-THREAD_EMBED_EPS,thread_pitch*.32]]);
}

module body_outer_envelope() {
  rotate_extrude() polygon([[0,0],[outer_radius-end_chamfer,0],[outer_radius,end_chamfer],
                            [outer_radius,body_thread_z],[0,body_thread_z]]);
}

module cap_outer_envelope() {
  rotate_extrude() polygon([[0,0],[outer_radius,0],[outer_radius,cap_height-end_chamfer],
                            [outer_radius-end_chamfer,cap_height],[0,cap_height]]);
}

module body_outer_blank() {
  if (surface_style == "diamond" && diamond_depth > 0)
    intersection() { diamond_exterior(body_thread_z, 0); body_outer_envelope(); }
  else body_outer_envelope();
}

module cap_outer_blank() {
  if (surface_style == "diamond" && diamond_depth > 0)
    intersection() { diamond_exterior(cap_height, cap_close_z); cap_outer_envelope(); }
  else cap_outer_envelope();
}

function v06_rev(f)=[f[2],f[1],f[0]];
function v06_profile(role)=role=="body"?
  [[thread_root_radius,body_thread_z],[thread_root_radius,body_height],[body_inner_radius,body_height],[body_inner_radius,floor_thickness]]:
  let(root=thread_root_radius+thread_clearance,eq=root+.4-cap_inner_radius,
    zs=concat([0],eq>0&&eq<.4?[eq]:[],[.4,closure_overlap]),
    raw=concat([for(z=zs)[max(cap_inner_radius,root+max(0,.4-z)),z]],[[cap_inner_radius,closure_overlap],[cap_inner_radius,cap_height-floor_thickness+.01]]))
  [for(i=[0:len(raw)-1])if(i==0||raw[i]!=raw[i-1])raw[i]];
function v06_internal_points(profile)=[for(r=profile)for(j=[0:95])[r[0]*cos(360*j/96),r[0]*sin(360*j/96),r[1]]];
function v06_internal_faces(profile,n,reverse=false)=[for(r=[0:len(profile)-2])for(j=[0:95])
  let(a=n+96*r+j,b=n+96*r+(j+1)%96,c=n+96*(r+1)+j,d=n+96*(r+1)+(j+1)%96)
  each reverse?[[b,d,a],[d,c,a]]:[[a,d,b],[a,c,d]]];
function v06_outer_angles(data,cut)=let(r=data[2][cut],raw=[for(k=[0:diamond_lattice_count-1])for(t=r)
  [v06_mod(diamond_phase_deg+360*(k+t[0])/diamond_lattice_count,360),v06_index(t[1],data[5],k)]],
  angles=[for(x=raw)x[0]],small=min(angles),start=[for(i=[0:len(raw)-1])if(raw[i][0]==small)i][0])
  [for(i=[0:len(raw)-1])raw[(i+start)%len(raw)]];
// Zipper outputs SCAD -Z faces. Outer cycle begins at its smallest physical
// angle; inner start immediately precedes it, retaining the original 96 datum.
function v06_zip(o,inner,positive,i=0,j=0,out=[])=let(m=len(o),n=96,start=floor(o[0][0]/(360/n)),
  oi=o[i%m][1],ij=inner+v06_mod(start+j,n),onext=i<m?(i+1<m?o[i+1][0]:o[0][0]+360):1e100,
  inext=j<n?(start+j+1)*360/n:1e100,
  a=i<m&&onext<=inext+DIAMOND_UV_EPS,b=j<n&&inext<=onext+DIAMOND_UV_EPS,
  ni=o[(i+1)%m][1],nj=inner+v06_mod(start+j+1,n),
  fs=a&&b?[[oi,ij,ni],[ni,ij,nj]]:a?[[oi,ij,ni]]:[[oi,ij,nj]])
  i==m&&j==n?out:v06_zip(o,inner,positive,i+(a?1:0),j+(b?1:0),concat(out,positive?fs:[for(f=fs)v06_rev(f)]));
function v06_direct(role)=let(body=role=="body",data=v06_data(body?-body_thread_z/diamond_axial_pitch:0,body?0:cap_height/diamond_axial_pitch,body?0:cap_close_z,role,cap_height),
  profile=v06_profile(role),n=len(data[0]),center=n+96*len(profile),
  points=concat(data[0],v06_internal_points(profile),[[0,0,body?0:cap_height],[0,0,profile[len(profile)-1][1]]]),
  outerDisk=v06_disk(v06_ring_indices(data,body?0:1),center,!body),
  join=v06_zip(v06_outer_angles(data,body?1:0),n,body),
  floorRing=[for(j=[0:95])n+96*(len(profile)-1)+j],
  faces=concat(data[1],outerDisk,join,v06_internal_faces(profile,n,!body),v06_disk(floorRing,center+1,body)))
  [points,faces,data,profile];
module v06_direct_shell(role) { mesh=v06_direct(role); polyhedron(points=mesh[0],faces=mesh[1],convexity=10); }
module v06_body_shell() {
  difference() {
    union() {
      v06_direct_shell("body");
      translate([0,0,body_thread_z+thread_transition]) body_thread();
    }
    if (drainage_mode == "bottom" || drainage_mode == "both") translate([0,0,-.1]) drain_pattern(floor_thickness+.2);
  }
}
module v06_cap_shell() {
  difference() {
    v06_direct_shell("cap");
    translate([0,0,thread_transition]) female_thread_groove();
    if (drainage_mode == "top" || drainage_mode == "both") translate([0,0,cap_height-floor_thickness-.1]) drain_pattern(floor_thickness+.2);
  }
}

module body_shell() {
  if (surface_style == "diamond" && diamond_depth > 0) v06_body_shell();
  else if (wave_active()) wave_body_shell();
  else difference() {
    union() {
      body_outer_blank();
      // positive external shoulder: cap closes here, not against the device.
      if (surface_style != "diamond" || diamond_depth == 0)
        translate([0,0,body_thread_z-1]) cylinder(r=outer_radius, h=1);
      translate([0,0,body_thread_z]) cylinder(r=thread_root_radius, h=closure_overlap);
      translate([0,0,body_thread_z+thread_transition]) body_thread();
    }
    translate([0,0,floor_thickness]) cylinder(r=body_inner_radius, h=body_height-floor_thickness+.1);
    if (drainage_mode == "bottom" || drainage_mode == "both") translate([0,0,-.1]) drain_pattern(floor_thickness+.2);
  }
}

module cap_shell() {
  if (surface_style == "diamond" && diamond_depth > 0) v06_cap_shell();
  else if (wave_active()) wave_cap_shell();
  else difference() {
    union() {
      cap_outer_blank();
    }
    // cap is open at local Z=0; its closed end is the top floor.
    cylinder(r=cap_inner_radius, h=cap_height-floor_thickness+.01);
    female_thread_void();
    translate([0,0,thread_transition]) female_thread_groove();
    if (drainage_mode == "top" || drainage_mode == "both") translate([0,0,cap_height-floor_thickness-.1]) drain_pattern(floor_thickness+.2);
  }
}

module closed_assembly() {
  color("#7097b3") body_shell();
  translate([0,0,cap_close_z]) color("#77b09a") cap_shell();
}

module print_layout() {
  translate([outer_diameter/2+3.5,0,0]) color("#7097b3") body_shell();
  // VFR-08: print closed-end-down/open-end-up while preserving cap geometry.
  translate([-outer_diameter/2-3.5,0,cap_height])
    rotate([180,0,0]) color("#77b09a") cap_shell();
}

if (VFR04_PROBE_MODE == "short_band")
  diamond_exterior(VFR04_PROBE_HEIGHT, VFR04_PROBE_GLOBAL_OFFSET);
else if (VFR04_PROBE_MODE == "math") {
  echo("VFR04_COUNT", diamond_lattice_count);
  echo("VFR04_HALF_UP", diamond_count(8.5*diamond_arc_pitch/(2*PI), diamond_arc_pitch));
  echo("VFR04_WRAP", diamond_wrap(-1.5), diamond_wrap(-0.5), diamond_wrap(0.5), diamond_wrap(1.5));
  echo("VFR04_FIELD", diamond_field(0,0,diamond_plateau_half_fraction), diamond_field(0.5,0,diamond_plateau_half_fraction));
  echo("VFR04_PATCH", diamond_patch_inverse(diamond_patch_coordinates(1.25,-0.75)[0], diamond_patch_coordinates(1.25,-0.75)[1]));
  echo("VFR04_SEAM", diamond_coordinates(0, diamond_global_z("body",body_thread_z,body_thread_z), diamond_phase_deg, body_thread_z, diamond_lattice_count, diamond_axial_pitch),
                       diamond_coordinates(0, diamond_global_z("cap",0,body_thread_z), diamond_phase_deg, body_thread_z, diamond_lattice_count, diamond_axial_pitch));
  echo("VFR04_WIDTH_SLOPE", diamond_default_plateau_width, diamond_default_axial_slope);
  cube([.01,.01,.01]);
}
else if (output_mode == "body") body_shell();
else if (output_mode == "cap") cap_shell();
else if (output_mode == "print_layout") print_layout();
else closed_assembly();
