from build123d import *
from math import *

# HOLE CALLOUT COMPOUNDS
# Designed By: Natan Herzog

class HoleCalloutArrow( BaseSketchObject ):
  def __init__(
    self,
    dimensioned_hole: Edge,
    arrow_origin: float = 0.0,
    callout_horizontal_offsets: [float] = [10,10],
    callout_vertical_offset: float = 5,
    font_size: float = 10,
    line_width: float = 0.5,
    mode: Mode = Mode.ADD,
  ):
    callout_shaft = Polyline(
      dimensioned_hole@arrow_origin ,
      dimensioned_hole.center(CenterOf.BOUNDING_BOX) + Vector( callout_horizontal_offsets[0] , callout_vertical_offset ),
      dimensioned_hole.center(CenterOf.BOUNDING_BOX) + Vector( callout_horizontal_offsets[0] + callout_horizontal_offsets[1] , callout_vertical_offset ),
    )
    callout_arrow = Arrow(
      arrow_size = font_size/2,
      shaft_path = callout_shaft,
      shaft_width = line_width,
      head_at_start = True,
      head_type = HeadType.CURVED,
    )

    super().__init__( obj = callout_arrow , rotation = 0 , align = None , mode = mode )



class ThruHoleLabel( BaseSketchObject ):
  def __init__(
    self,
    hole_diameter: float,
    tolerance: float,
    num_features: int = 1,
    font_size: float = 10,
    line_width: float = 0.5,
    mode: Mode = Mode.ADD
  ):

    multiple_feature_note = MultipleFeatures( feature_count = num_features , draft_font_size = font_size )
    diameter_sym = Pos( multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 1 * font_size , 0 ) ) * Diameter( feature_size = font_size , line_width = line_width)
    dimension_text = Text( txt = str(hole_diameter) + " \u00B1 " + str(tolerance) + " THRU ALL" , font_size = font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = diameter_sym.center() + ( font_size , 0 )

    callout = Compound([
      multiple_feature_note,
      diameter_sym,
      dimension_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )


class UnthreadedHoleLabel( BaseSketchObject ):
  def __init__(
    self,
    hole_diameter: float,
    diameter_tolerance: float,
    hole_depth: float,
    depth_tolerance: float,
    num_features: int = 1,
    font_size: float = 10,
    line_width: float = 0.5,
    mode: Mode = Mode.ADD
  ):

    multiple_feature_note = MultipleFeatures( feature_count = num_features , draft_font_size = font_size )
    diameter_sym = Pos( multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 1 * font_size , 0 ) ) * Diameter( feature_size = font_size , line_width = line_width)
    dimension_text = Text( txt = str(hole_diameter) + " \u00B1 " + str(diameter_tolerance) , font_size = font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = diameter_sym.center(CenterOf.BOUNDING_BOX) + ( font_size , 0 )
    depth_sym = Pos( dimension_text.center(CenterOf.BOUNDING_BOX) + Vector( dimension_text.bounding_box().size.X/2 + 1*font_size , 0 ) ) * DepthSymbol( feature_size = font_size , line_width = line_width )
    depth_text = Text( txt = str(hole_depth) + " \u00B1 " + str(depth_tolerance) , font_size = font_size , align = (Align.MIN , Align.CENTER) )
    depth_text.position = dimension_text.center(CenterOf.BOUNDING_BOX) + (dimension_text.bounding_box().size.X/2 + 2*font_size , 0)

    callout = Compound([
      multiple_feature_note,
      diameter_sym,
      dimension_text,
      depth_sym,
      depth_text,
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )


class CounterBoreHoleLabel( BaseSketchObject ):
  def __init__(
    self,
    hole_diameter: float,
    diameter_tolerance: float,
    counterbore_diameter: float,
    counterbore_diameter_tolerance: float,
    counterbore_depth: float,
    counterbore_depth_tolerance: float,
    num_features: int = 1,
    font_size: float = 10,
    line_width: float = 0.5,
    mode: Mode = Mode.ADD
  ):

    multiple_feature_note = MultipleFeatures( feature_count = num_features , draft_font_size = font_size )
    text_origin = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( -multiple_feature_note.bounding_box().size.X/2 , 0 )
    diameter_sym = Pos( multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + font_size , 0 ) ) * Diameter( feature_size = font_size , line_width = line_width)
    dimension_text = Text( txt = str(hole_diameter) + " \u00B1 " + str(diameter_tolerance) + " THRU ALL", font_size = font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = diameter_sym.center(CenterOf.BOUNDING_BOX) + ( font_size , 0 )

    counterbore_sym = Pos( multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( -multiple_feature_note.bounding_box().size.X/2 , -1.5*font_size ) ) * CounterBore( feature_size = font_size , line_width = line_width )
    diameter_sym_2 = Pos( counterbore_sym.center(CenterOf.BOUNDING_BOX) + ( 1.5*font_size,0 ) ) * Diameter( feature_size = font_size , line_width = line_width )
    counterbore_dimension_text = Text( txt = str(counterbore_diameter) + " \u00B1 " + str(counterbore_diameter_tolerance) , font_size = font_size , align = (Align.MIN , Align.CENTER) )
    counterbore_dimension_text.position = diameter_sym_2.center(CenterOf.BOUNDING_BOX) + ( font_size , 0 )
    depth_sym = Pos( counterbore_dimension_text.center(CenterOf.BOUNDING_BOX) + Vector( counterbore_dimension_text.bounding_box().size.X/2 + 1*font_size , 0 ) ) * DepthSymbol( feature_size = font_size , line_width = line_width )
    depth_text = Text( txt = str(counterbore_depth) + " \u00B1 " + str(counterbore_depth_tolerance) , font_size = font_size , align = (Align.MIN , Align.CENTER) )
    depth_text.position = counterbore_dimension_text.center(CenterOf.BOUNDING_BOX) + (counterbore_dimension_text.bounding_box().size.X/2 + 2*font_size , 0)


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



class TappedThruHole( BaseSketchObject ):
  def __init__(
    self,
    thread_type: str,
    num_features: int = 1,
    font_size: float = 10,
    line_width: float = 0.5,
    mode: Mode = Mode.ADD
  ):  

    multiple_feature_note = MultipleFeatures( feature_count = num_features , draft_font_size = font_size )
    dimension_text = Text( txt = thread_type + " THRU ALL" , font_size = font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 0.5 * font_size , 0 )

    callout = Compound([
      multiple_feature_note,
      dimension_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )



class TappedHole( BaseSketchObject ):
  def __init__(
    self,
    thread_type: str,
    num_features: int = 1,
    font_size: float = 10,
    line_width: float = 0.5,
    mode: Mode = Mode.ADD
  ):  

    multiple_feature_note = MultipleFeatures( feature_count = num_features , draft_font_size = font_size )
    dimension_text = Text( txt = "TAP FOR " + thread_type , font_size = font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 0.5 * font_size , 0 )

    callout = Compound([
      multiple_feature_note,
      dimension_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )



class HelicoilInsertHole( BaseSketchObject ):
  def __init__(
    self,
    thread_type: str,
    part_number: str,
    num_features: int = 1,
    font_size: float = 10,
    line_width: float = 0.5,
    mode: Mode = Mode.ADD
  ):  

    multiple_feature_note = MultipleFeatures( feature_count = num_features , draft_font_size = font_size )
    dimension_text = Text( txt = "TAP FOR " + thread_type + " HELICOIL INSERT", font_size = font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 0.5 * font_size , 0 )

    part_number_text = Text( txt = "P/N " + part_number , font_size = font_size , align = (Align.MIN , Align.CENTER) )
    part_number_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( -multiple_feature_note.bounding_box().size.X/2 , -1.5*font_size )

    callout = Compound([
      multiple_feature_note,
      dimension_text,
      part_number_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )


class HelicoilInsertThruHole( BaseSketchObject ):
  def __init__(
    self,
    thread_type: str,
    part_number: str,
    num_features: int = 1,
    font_size: float = 10,
    line_width: float = 0.5,
    mode: Mode = Mode.ADD
  ):  

    multiple_feature_note = MultipleFeatures( feature_count = num_features , draft_font_size = font_size )
    dimension_text = Text( txt = "TAP FOR " + thread_type + " HELICOIL INSERT", font_size = font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 0.5 * font_size , 0 )

    depth_sym = Pos( multiple_feature_note.bounding_box().min + ( font_size/2 , -font_size ) ) * DepthSymbol( feature_size = font_size , line_width = line_width )
    thru_all_txt = Text( txt = "THRU ALL" , font_size = font_size , align = (Align.MIN , Align.CENTER) )
    thru_all_txt.position = Vector( depth_sym.bounding_box().max.X , depth_sym.center(CenterOf.BOUNDING_BOX).Y ) + Vector( 0.5*font_size , 0 )

    part_number_text = Text( txt = "P/N " + part_number , font_size = font_size , align = (Align.MIN , Align.MAX) )
    part_number_text.position = depth_sym.bounding_box().min + ( 0 , -0.5*font_size )

    callout = Compound([
      multiple_feature_note,
      dimension_text,
      depth_sym,
      thru_all_txt,
      part_number_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )


class HelicoilInsertBlindHole( BaseSketchObject ):
  def __init__(
    self,
    thread_type: str,
    thread_depth: float,
    thread_depth_tolerance: float,
    part_number: str,
    units: str = "",
    num_features: int = 1,
    font_size: float = 10,
    line_width: float = 0.5,
    mode: Mode = Mode.ADD
  ):  

    multiple_feature_note = MultipleFeatures( feature_count = num_features , draft_font_size = font_size )
    dimension_text = Text( txt = "TAP FOR " + thread_type + " HELICOIL INSERT", font_size = font_size , align = (Align.MIN , Align.CENTER) )
    dimension_text.position = multiple_feature_note.center(CenterOf.BOUNDING_BOX) + Vector( multiple_feature_note.bounding_box().size.X/2 + 0.5 * font_size , 0 )

    depth_sym = Pos( multiple_feature_note.bounding_box().min + ( font_size/2 , -font_size ) ) * DepthSymbol( feature_size = font_size , line_width = line_width )
    depth_txt = Text( txt = str(thread_depth) + " \u00B1 " + str(thread_depth_tolerance) + " " + units , font_size = font_size , align = (Align.MIN , Align.CENTER) )
    depth_txt.position = Vector( depth_sym.bounding_box().max.X , depth_sym.center(CenterOf.BOUNDING_BOX).Y ) + Vector( 0.5*font_size , 0 )

    part_number_text = Text( txt = "P/N " + part_number , font_size = font_size , align = (Align.MIN , Align.MAX) )
    part_number_text.position = depth_sym.bounding_box().min + ( 0 , -0.5*font_size )

    callout = Compound([
      multiple_feature_note,
      dimension_text,
      depth_sym,
      depth_txt,
      part_number_text
    ])

    super().__init__( obj = callout , rotation = 0 , align = None , mode = mode )