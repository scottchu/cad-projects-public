import {DEFAULT_STATE} from "./schema.mjs";
import {deepFreeze,deepMerge} from "./utils.mjs";
export const PRESET_PATCHES=deepFreeze({
 generic:{},
 laifen_wave_reference:{container:{height:219,outerDiameter:39,wall:2.4,floor:3,splitFromTop:84},closure:{mode:"screw",screw:{pitch:2,turns:3,leadRunoutTurns:1.5,formHeight:.45,radialClearance:.25}},ends:{linked:true,bottom:{profile:"chamfer",size:1.2}},surface:{pattern:"recessed_diamond",reliefMode:"inset",depth:.45,minWall:1.8,axialPitch:12,arcPitch:9}},
 wide_short_makeup_jar:{container:{height:55,outerDiameter:80,splitFromTop:27.5,crossSection:"regular_polygon",sideCount:6,cornerRoundness:.35,rotationDeg:15},closure:{mode:"bayonet",bayonet:{lockAngleDeg:90,lugCount:3,capture:2,rampRise:1,radialClearance:.3}},ends:{linked:true,bottom:{profile:"rounded_fillet",size:3}},surface:{pattern:"flowing_flutes",envelope:"fade_from_bottom",depth:.6}}
});
export const presetState=id=>deepMerge(DEFAULT_STATE,PRESET_PATCHES[id]||PRESET_PATCHES.generic);
export function fromR8Flat(flat){return deepMerge(DEFAULT_STATE,{container:{height:flat.H,outerDiameter:flat.OD,splitFromTop:flat.S},closure:{mode:flat.closureMode==="bayonet_twist_lock"?"bayonet":"screw",screw:{pitch:flat.p,turns:flat.N,leadRunoutTurns:flat.Lr,formHeight:flat.formHeight??.45,radialClearance:flat.clearance??.25},bayonet:{lockAngleDeg:flat.bayonetLockAngle,lugCount:flat.bayonetLugCount,capture:flat.bayonetCapture,rampRise:flat.bayonetRampRise,radialClearance:flat.bayonetClearance}},surface:{pattern:flat.pattern,depth:flat.depth,axialPitch:flat.axial,arcPitch:flat.arc}});}
