from build123d import *
from math import *
from GDTHelpers import *


# HOLE CALLOUT COMPOUNDS
# Designed By: Natan Herzog


class HoleCalloutArrow( BaseSketchObject ):
  def __init__(
    self,
    dimensioned_hole: Edge,
    arrow_origin: float = 0.0,
    callout_horizontal_offsets: [float] = [10,10],
    callout_vertical_offset: float = 5,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
  ):
    callout_shaft = Polyline(
      dimensioned_hole@arrow_origin ,
      dimensioned_hole.center(CenterOf.BOUNDING_BOX) + Vector( callout_horizontal_offsets[0] , callout_vertical_offset ),
      dimensioned_hole.center(CenterOf.BOUNDING_BOX) + Vector( callout_horizontal_offsets[0] + callout_horizontal_offsets[1] , callout_vertical_offset ),
    )
    callout_arrow = Arrow(
      arrow_size = drafting_specs.font_size/2,
      shaft_path = callout_shaft,
      shaft_width = drafting_specs.line_width,
      head_at_start = True,
      head_type = HeadType.CURVED,
    )

    super().__init__( obj = callout_arrow , rotation = 0 , align = None , mode = mode )


#!! FULLY TOLERANCED HOLES
class CounterBoreHole( BaseSketchObject ):
  def __init__(
    self,
    hole_diameter: float = 0,
    diameter_tolerance: float = 0,
    counterbore_diameter: float = 0,
    counterbore_diameter_tolerance: float = 0,
    counterbore_depth: float = 0,
    counterbore_depth_tolerance: float = 0,
    num_features: int = 1,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD
  ):

    multiple_feature_note = MultipleFeatures( feature_count = num_features , drafting_specs=drafting_specs )
    text_origin = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( -multiple_feature_note.bounding_box().size.X/2 , 0 )
    diameter_sym = Pos( multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + drafting_specs.font_size , 0 ) ) * Diameter( drafting_specs )
    dimension_text = Text( txt = str(hole_diameter) + " \u00B1 " + str(diameter_tolerance) + " THRU ALL", font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = diameter_sym.center(CenterOf.BOUNDING_BOX) + ( drafting_specs.font_size , 0 )

    counterbore_sym = Pos( multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( -multiple_feature_note.bounding_box().size.X/2 , -1.5*drafting_specs.font_size ) ) * CounterBore( drafting_specs , align = (Align.MIN,Align.CENTER) )
    diameter_sym_2 = Pos( counterbore_sym.center(CenterOf.BOUNDING_BOX) + ( 1.5*drafting_specs.font_size,0 ) ) * Diameter( drafting_specs )
    counterbore_dimension_text = Text( txt = str(counterbore_diameter) + " \u00B1 " + str(counterbore_diameter_tolerance) , font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    counterbore_dimension_text.position = diameter_sym_2.center(CenterOf.BOUNDING_BOX) + ( drafting_specs.font_size , 0 )
    depth_sym = Pos( counterbore_dimension_text.center(CenterOf.BOUNDING_BOX) + Vector( counterbore_dimension_text.bounding_box().size.X/2 + 1*drafting_specs.font_size , 0 ) ) * DepthSymbol( drafting_specs )
    depth_text = Text( txt = str(counterbore_depth) + " \u00B1 " + str(counterbore_depth_tolerance) , font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    depth_text.position = counterbore_dimension_text.center(CenterOf.BOUNDING_BOX) + (counterbore_dimension_text.bounding_box().size.X/2 + 2*drafting_specs.font_size , 0)

    callout = Compound([
      multiple_feature_note,
      diameter_sym,
      dimension_text,
      counterbore_sym,
      diameter_sym_2,
      counterbore_dimension_text,
      depth_sym,
      depth_text,
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )


#TODO : add a class for ThreadedBlindHole to specify the depth of the hole as well as the depth of the threads


class ThreadedThruHole( BaseSketchObject ):
  def __init__(
    self,
    thread_type: str = "--",
    num_features: int = 1,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD
  ):  

    multiple_feature_note = MultipleFeatures( feature_count = num_features , drafting_specs=drafting_specs )
    dimension_text = Text( txt = "TAP FOR " + thread_type + " THRU ALL" , font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 0.5 * drafting_specs.font_size , 0 )

    callout = Compound([
      multiple_feature_note,
      dimension_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )


class UnthreadedBlindHole( BaseSketchObject ):
  def __init__(
    self,
    hole_diameter: float = 0,
    diameter_tolerance: float = 0,
    hole_depth: float = 0,
    depth_tolerance: float = 0,
    num_features: int = 1,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD
  ):

    multiple_feature_note = MultipleFeatures( feature_count = num_features , drafting_specs=drafting_specs )
    diameter_sym = Pos( multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 1 * drafting_specs.font_size , 0 ) ) * Diameter( drafting_specs )
    dimension_text = Text( txt = str(hole_diameter) + " \u00B1 " + str(diameter_tolerance) , font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = diameter_sym.center(CenterOf.BOUNDING_BOX) + ( drafting_specs.font_size , 0 )
    depth_sym = Pos( dimension_text.center(CenterOf.BOUNDING_BOX) + Vector( dimension_text.bounding_box().size.X/2 + 1*drafting_specs.font_size , 0 ) ) * DepthSymbol( drafting_specs )
    depth_text = Text( txt = str(hole_depth) + " \u00B1 " + str(depth_tolerance) , font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    depth_text.position = dimension_text.center(CenterOf.BOUNDING_BOX) + (dimension_text.bounding_box().size.X/2 + 2*drafting_specs.font_size , 0)

    callout = Compound([
      multiple_feature_note,
      diameter_sym,
      dimension_text,
      depth_sym,
      depth_text,
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )


class UnthreadedThruHole( BaseSketchObject ):
  def __init__(
    self,
    hole_diameter: float = 0,
    tolerance: float = 0,
    num_features: int = 1,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD
  ):

    multiple_feature_note = MultipleFeatures( feature_count = num_features , drafting_specs=drafting_specs )
    diameter_sym = Pos( multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 1 * drafting_specs.font_size , 0 ) ) * Diameter( drafting_specs )
    dimension_text = Text( txt = str(hole_diameter) + " \u00B1 " + str(tolerance) + " THRU ALL" , font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = diameter_sym.center() + ( drafting_specs.font_size , 0 )

    callout = Compound([
      multiple_feature_note,
      diameter_sym,
      dimension_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )




#!! UN-TOLERANCED HOLES
class HelicoilInsertBlindHole( BaseSketchObject ):
  def __init__(
    self,
    thread_type: str = "--",
    part_number: str = "--",
    thread_depth: float = 0,
    thread_depth_tolerance: float = 0,
    units: str = "",
    num_features: int = 1,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD
  ):  

    multiple_feature_note = MultipleFeatures( feature_count = num_features , drafting_specs=drafting_specs )
    dimension_text = Text( txt = "TAP FOR " + thread_type + " HELICOIL INSERT", font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 0.5 * drafting_specs.font_size , 0 )

    depth_sym = Pos( multiple_feature_note.bounding_box().min + ( drafting_specs.font_size/2 , -drafting_specs.font_size ) ) * DepthSymbol( drafting_specs )
    depth_txt = Text( txt = str(thread_depth) + " \u00B1 " + str(thread_depth_tolerance) + " " + units , font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    depth_txt.position = Vector( depth_sym.bounding_box().max.X , depth_sym.center(CenterOf.BOUNDING_BOX).Y ) + Vector( 0.5*drafting_specs.font_size , 0 )

    part_number_text = Text( txt = "P/N " + part_number , font_size = drafting_specs.font_size , align = (Align.MIN , Align.MAX) )
    part_number_text.position = depth_sym.bounding_box().min + ( 0 , -0.5*drafting_specs.font_size )

    callout = Compound([
      multiple_feature_note,
      dimension_text,
      depth_sym,
      depth_txt,
      part_number_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )


class HelicoilInsertHole( BaseSketchObject ):
  def __init__(
    self,
    thread_type: str = "--",
    part_number: str = "--",
    num_features: int = 1,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD
  ):  

    multiple_feature_note = MultipleFeatures( feature_count = num_features , drafting_specs=drafting_specs )
    dimension_text = Text( txt = "TAP FOR " + thread_type + " HELICOIL INSERT", font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 0.5 * drafting_specs.font_size , 0 )

    part_number_text = Text( txt = "P/N " + part_number , font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    part_number_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( -multiple_feature_note.bounding_box().size.X/2 , -1.5*drafting_specs.font_size )

    callout = Compound([
      multiple_feature_note,
      dimension_text,
      part_number_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )


class HelicoilInsertThruHole( BaseSketchObject ):
  def __init__(
    self,
    thread_type: str = "--",
    part_number: str = "--",
    num_features: int = 1,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD
  ):  

    multiple_feature_note = MultipleFeatures( feature_count = num_features , drafting_specs=drafting_specs )
    dimension_text = Text( txt = "TAP FOR " + thread_type + " HELICOIL INSERT", font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 0.5 * drafting_specs.font_size , 0 )

    depth_sym = Pos( multiple_feature_note.bounding_box().min + ( drafting_specs.font_size/2 , -drafting_specs.font_size ) ) * DepthSymbol( drafting_specs )
    thru_all_txt = Text( txt = "THRU ALL" , font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    thru_all_txt.position = Vector( depth_sym.bounding_box().max.X , depth_sym.center(CenterOf.BOUNDING_BOX).Y ) + Vector( 0.5*drafting_specs.font_size , 0 )

    part_number_text = Text( txt = "P/N " + part_number , font_size = drafting_specs.font_size , align = (Align.MIN , Align.MAX) )
    part_number_text.position = depth_sym.bounding_box().min + ( 0 , -0.5*drafting_specs.font_size )

    callout = Compound([
      multiple_feature_note,
      dimension_text,
      depth_sym,
      thru_all_txt,
      part_number_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )


class TappedHole( BaseSketchObject ):
  def __init__(
    self,
    thread_type: str = "--",
    num_features: int = 1,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD
  ):  

    multiple_feature_note = MultipleFeatures( feature_count = num_features , drafting_specs=drafting_specs )
    dimension_text = Text( txt = "TAP FOR " + thread_type , font_size = drafting_specs.font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 0.5 * drafting_specs.font_size , 0 )

    callout = Compound([
      multiple_feature_note,
      dimension_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )







if __name__ == "__main__":
  from ocp_vscode import *
  offset = 4*IN

  fully_defined_holes = Compound([
    Pos( X = (0 * offset) ) * CounterBoreHole(),
    Pos( X = (1 * offset) ) * ThreadedThruHole(),
    Pos( X = (2 * offset) ) * UnthreadedBlindHole(),
    Pos( X = (3 * offset) ) * UnthreadedThruHole(),
  ])
  undefined_holes = Compound([
    Pos( X = (4 * offset) ) * HelicoilInsertBlindHole(),
    Pos( X = (5 * offset) ) * HelicoilInsertHole(),
    Pos( X = (6 * offset) ) * HelicoilInsertThruHole(),
    Pos( X = (7 * offset) ) * TappedHole(),
  ])

  outline_offset = 0.5*IN
  show(
    fully_defined_holes,
    Edge.make_line(
      Vector(fully_defined_holes.bounding_box().min.X , fully_defined_holes.bounding_box().max.Y) + Vector( 0 , outline_offset ),
      fully_defined_holes.bounding_box().max + Vector( 0 , outline_offset ),
    ),
    undefined_holes,
    Edge.make_line(
      Vector(undefined_holes.bounding_box().min.X , undefined_holes.bounding_box().max.Y) + Vector( 0 , outline_offset ),
      undefined_holes.bounding_box().max + Vector( 0 , outline_offset ),
    ),
  )