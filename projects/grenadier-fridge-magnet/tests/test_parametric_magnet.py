"""Risk checks: frame flip, coupled XY/Z, lost holes, invalid knobs and levels."""
import importlib.util
from pathlib import Path
import sys
import numpy as np
import pytest
SRC=Path(__file__).resolve().parents[1]/'src'
sys.path.insert(0,str(SRC))
from parametric_magnet import Parameters, transform_xy, inverse_xy, validate_features, FEATURES, semantic_masks, extrude_mask

def test_transform_and_independent_height():
    uv=np.array([[0,0],[627,627],[1254,1254],[113,917]])
    for scale in (0.01,1,7):
        p=Parameters(xy_scale=scale)
        np.testing.assert_allclose(inverse_xy(transform_xy(uv,p),p),uv,atol=1e-10)
        assert transform_xy([[628,626]],p)[0,0]>0 and transform_xy([[628,626]],p)[0,1]>0
        assert p.flat_face_depth_mm==Parameters().flat_face_depth_mm
    for kwargs in ({'xy_scale':0},{'back_thickness_mm':-1},{'xy_scale':float('nan')},{'low_depth_mm':0.8}):
        with pytest.raises(ValueError):Parameters(**kwargs).validate()

def test_identity_only_schema():
    validate_features(FEATURES)
    with pytest.raises(ValueError):validate_features(FEATURES|{'plate':FEATURES['plate']|{'xy_scale':1.1}})

def test_semantics_partition_and_plate_coplanarity():
    masks=semantic_masks(np.ones((1254,1254),dtype=bool))
    assert np.all(sum(m.astype(int) for m in masks.values())==1)
    assert masks['high'][880,450]
    assert masks['low'][350,500]
    assert masks['high'][720,137]

def test_closed_hole_and_diagonal_components():
    mask=np.ones((5,5),bool);mask[1:4,1:4]=False
    mesh,count=extrude_mask(mask,1.2,0.8,Parameters())
    assert count==1 and mesh.is_watertight and mesh.is_winding_consistent
    assert np.isclose(mesh.volume,16*0.01*0.8)
    diagonal=np.eye(2,dtype=bool)
    mesh,count=extrude_mask(diagonal,1.2,0.8,Parameters())
    assert count==2 and mesh.is_watertight

def test_hole_touching_outer_boundary_pinched_grid_regression():
    # A hole meeting the outside at a single grid vertex extrudes to a
    # coincident vertical edge: fan splitting must keep indexed shells closed.
    mask=np.ones((4,4),bool);mask[0,0]=False;mask[1,1]=False
    mesh,count=extrude_mask(mask,1.2,0.8,Parameters())
    assert mesh.is_watertight and mesh.is_winding_consistent
    assert np.isclose(mesh.volume,14*0.01*0.8)

def test_backing_shortest_bridge_preserves_face_and_is_connected():
    from parametric_magnet import backing_connectivity
    from scipy import ndimage
    face=np.zeros((8,8),bool);face[2:5,2:5]=True;face[5,5]=True;face[2,6]=True
    saved=face.copy()
    repaired,delta=backing_connectivity(face)
    np.testing.assert_array_equal(face,saved)
    assert np.all(repaired[face]) and ndimage.label(repaired)[1]==1
    assert delta['max_cells_per_link']<=2 and delta['added_count']<=4
    np.testing.assert_array_equal(repaired,backing_connectivity(face)[0])
    mesh,count=extrude_mask(repaired,0,1.2,Parameters())
    assert count==1 and len(mesh.split())==1 and mesh.is_watertight

def test_glb_linear_color_transfer_roundtrip_and_single_multiplier():
    from parametric_magnet import PALETTE, srgb_to_linear, linear_to_srgb, encode_glb_materials
    for color,value in PALETTE.items():
        rgb=np.array([int(value[i:i+2],16) for i in (1,3,5)])
        recovered=linear_to_srgb(srgb_to_linear(rgb/255))
        np.testing.assert_allclose(recovered,rgb/255,atol=1e-6)
        np.testing.assert_array_equal(np.rint(recovered*255),rgb)
        tree={'meshes':[{'name':color+'-flat','primitives':[{'attributes':{'POSITION':1,'COLOR_0':2},'indices':0}]}]}
        encode_glb_materials(tree)
        primitive=tree['meshes'][0]['primitives'][0]
        assert primitive['attributes']=={'POSITION':1} and primitive['indices']==0
        np.testing.assert_allclose(tree['materials'][0]['pbrMetallicRoughness']['baseColorFactor'][:3],srgb_to_linear(rgb/255),atol=1e-15)
    np.testing.assert_allclose(linear_to_srgb(srgb_to_linear([0,1])),[0,1],atol=1e-15)
