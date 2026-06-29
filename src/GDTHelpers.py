from build123d import *
from math import *

# GDT FEATURE SYMBOLS
# Designed By: Natan Herzog
# Referenced From: gdtandbasics.com/gdt-symbols

#! Included features
#!  [-] Angularity
#!  [-] ArcLength
#!  [-] CircledLetterLabel 
#!  [ ] Circularity
#!  [-] Concentricity
#!  [-] ConicalTaper
#!  [-] ContinuousFeature
#!  [-] CounterBore
#!  [-] CounterSink
#!  [-] CrossHair
#!  [-] DatumFeature
#!  [-] DepthSymbol
#!  [-] Diameter
#!  [-] Flatness
#!  [-] MultipleFeatures
#!  [-] Parallelism
#!  [-] Perpendicularity
#!  [-] SurfaceProfile
#!  [-] ThirdAngleProjection
#!  [-] TruePosition
#!
#! Not Included Yet
#!  [ ] Cylindricity
#!  [ ] DatumTarget
#!  [ ] DimensionOrigin
#!  [ ] LineProfile
#!  [ ] PartingLine
#!  [ ] Runout
#!  [ ] Slope
#!  [ ] SphericalDiameter
#!  [ ] Spotface
#!  [ ] Straightness
#!  [ ] Symmetry
#!  [ ] TotalRunout
#! =====

class Angularity(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    sym = Compound([
      Edge.make_line(
        (-drafting_specs.font_size/1.5 , -drafting_specs.font_size/2 ),
        ( drafting_specs.font_size/1.5 , -drafting_specs.font_size/2 )
      ),
      Edge.make_line(
        (-drafting_specs.font_size/1.5 , -drafting_specs.font_size/2 ),
        ( drafting_specs.font_size/1.5 ,  drafting_specs.font_size/2 )
      ),
    ])
    traced = trace( sym , drafting_specs.line_width )
    super().__init__(obj = traced , rotation = rotation , align = align , mode = mode )

class ArcLength(BaseSketchObject):
  def __init__(
    self,
    arc_length: float = 1.0,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    text = Text( txt = str(arc_length) , font_size = drafting_specs.font_size )
    arc_origin = ( text.center(CenterOf.BOUNDING_BOX).X , text.bounding_box().min.Y )
    top_right = text.bounding_box().max - arc_origin
    start_angle = asin( abs(top_right.Y / top_right.length) )
    arc_size = pi - 2*start_angle
    arc = CenterArc(
      center = arc_origin ,
      radius = top_right.length ,
      start_angle = start_angle * 180 / pi,
      arc_size = arc_size * 180 / pi
    )
    traced = trace( arc , drafting_specs.line_width )
    compound = Compound([ text , arc_traced ])
    super().__init__(obj = compound , rotation = rotation , align = align , mode = mode )

class CircledLetterLabel(BaseSketchObject):
  def __init__(
    self,
    feature_label: str = "",
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    circle = Circle( radius = drafting_specs.font_size*1.5/2 )
    label_text = Text( txt = feature_label , font_size = drafting_specs.font_size)
    label_text.position = circle.center(CenterOf.BOUNDING_BOX)
    label = Compound([
      trace(circle , drafting_specs.line_width),
      label_text
    ])
    super().__init__(obj=label, rotation=rotation, align=align, mode=mode)

class Circularity(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width=0.1),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    sym = Circle( radius = drafting_specs.font_size/2 )
    traced = trace( sym , drafting_specs.line_width )
    super().__init__(obj = traced , rotation = rotation , align = align , mode = mode )

class Concentricity(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    sym = Compound([ Circle( radius = drafting_specs.font_size/2 ) , Circle( radius = drafting_specs.font_size/2.5 ) ])
    traced = trace( sym , drafting_specs.line_width )
    super().__init__(obj = traced , rotation = rotation , align = align , mode = mode )

class ConicalTaper(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    sym = Compound([
      Edge.make_line(
        ( -drafting_specs.font_size , 0 ) , ( drafting_specs.font_size , 0 )
      ) ,
      Pos( X=-drafting_specs.font_size*1.5/6 ) * Triangle( a = drafting_specs.font_size , b = drafting_specs.font_size*1.5 , c = drafting_specs.font_size*1.5 , rotation = 270 ),
    ])
    traced = trace( sym , drafting_specs.line_width )
    super().__init__(obj = traced , rotation = rotation , align = align , mode = mode )

class ContinuousFeature(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    offset = drafting_specs.font_size * 0.125
    text = Text( txt = "CF" , font_size = drafting_specs.font_size )
    sym = Polyline(
      (text.bounding_box().min.X , text.bounding_box().min.Y - offset ),
      (text.bounding_box().max.X , text.bounding_box().min.Y - offset ),
      (text.bounding_box().max.X + 2*offset , 0),
      (text.bounding_box().max.X , text.bounding_box().max.Y + offset ),
      (text.bounding_box().min.X , text.bounding_box().max.Y + offset ),
      (text.bounding_box().min.X - 2*offset , 0),
      close = True,
    )
    traced = trace( sym , drafting_specs.line_width )
    result = Compound([ text , traced ])
    super().__init__( obj = result , rotation = rotation , align = align , mode = mode ) 

class CounterBore(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    feature_size = drafting_specs.font_size
    symbol_lines = Edge.make_line(
      (0,-feature_size/4) , (feature_size,-feature_size/4)
    )
    symbol_lines += Edge.make_line(
      (0,-feature_size/4) , (0,feature_size/4)
    )
    symbol_lines += Edge.make_line(
      (feature_size,-feature_size/4) , (feature_size,feature_size/4)
    )
    traced = trace( symbol_lines , drafting_specs.line_width )
    super().__init__(obj = traced , rotation=rotation, align=align, mode=mode)

class CounterSink(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    sym = Polyline(
      ( -drafting_specs.font_size/2 , drafting_specs.font_size/4 ),
      ( 0 , -drafting_specs.font_size/4 ),
      (  drafting_specs.font_size/2 , drafting_specs.font_size/4 ),
    )
    traced = trace( sym , drafting_specs.line_width )
    super().__init__(obj = traced , rotation = rotation , align = align , mode = mode )

class CrossHair(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    sym = Compound([
      Edge.make_line( (0,1.5*drafting_specs.font_size/2) , (0,-1.5*drafting_specs.font_size/2) ) ,
      Edge.make_line( (-1.5*drafting_specs.font_size/2,0) , (1.5*drafting_specs.font_size/2,0) ) ])
    traced = trace( sym , drafting_specs.line_width )
    super().__init__(obj=traced, rotation=rotation, align=align, mode=mode)

class DatumFeature(BaseSketchObject):
  def __init__(
    self,
    datum_label: str = "",
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    feature_size = drafting_specs.font_size * 1.5
    triangle = Triangle( a = feature_size , B = 60 , C = 60 , align = (Align.CENTER , Align.MIN) )
    flagpole = Edge.make_line(
      triangle.vertices().sort_by(Axis.Y)[-1] + (0,-drafting_specs.line_width),
      triangle.vertices().sort_by(Axis.Y)[-1] + (0,feature_size/3),
    )
    box = Pos( flagpole.vertices().sort_by(Axis.Y)[-1] ) * Rectangle( width = feature_size , height = feature_size , align = (Align.CENTER , Align.MIN) )
    box_edges = box.edges()
    label = Text( txt = datum_label , font_size = drafting_specs.font_size )
    label.position = box.center()

    datum = Compound([
      triangle ,
      trace( flagpole , drafting_specs.line_width ) ,
      trace( box_edges , drafting_specs.line_width ) ,
      label
      ] )
    super().__init__(obj=datum, rotation=rotation, align=align, mode=mode)

class DepthSymbol(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    feature_size = drafting_specs.font_size
    lines = Edge.make_line(
      (0,feature_size/2) , (0,-feature_size/2)
    )
    lines += Edge.make_line(
      (-feature_size/2 , feature_size/2) , (feature_size/2 , feature_size/2)
    )
    arrow = Edge.make_line(
      (-feature_size/5,-feature_size/2+feature_size/5) , (0,-feature_size/2)
    )
    arrow += Edge.make_line(
      (feature_size/5,-feature_size/2+feature_size/5) , (0,-feature_size/2)
    )
    symbol = Compound([
      trace( lines , drafting_specs.line_width ),
      trace( arrow , drafting_specs.line_width )
    ])
    super().__init__(obj=symbol, rotation=rotation, align=align, mode=mode)

class Diameter(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    feature_size = drafting_specs.font_size
    circle = Circle( radius = feature_size/2 )
    line = Edge.make_line( (1.2*feature_size/2 , 1.2*feature_size/2) , (-1.2*feature_size/2 , -1.2*feature_size/2) )
    symbol = Compound([
      trace( circle , drafting_specs.line_width ),
      trace( line , drafting_specs.line_width )
    ])

    super().__init__(obj=symbol, rotation=rotation, align=align, mode=mode)

class Flatness(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    internal_acute_angle = 70
    side_lean_length = drafting_specs.font_size * cos( internal_acute_angle * pi / 180 )
    sym = Polyline(
      (-drafting_specs.font_size/2 - side_lean_length/2 ,-drafting_specs.font_size/3),
      ( drafting_specs.font_size/2 - side_lean_length/2 ,-drafting_specs.font_size/3),
      ( drafting_specs.font_size/2 + side_lean_length/2 , drafting_specs.font_size/3),
      (-drafting_specs.font_size/2 + side_lean_length/2 , drafting_specs.font_size/3),
      close = True,
    )
    flatness_traced = trace( sym , drafting_specs.line_width )
    super().__init__(obj = traced , rotation = rotation , align = align , mode = mode )

class MultipleFeatures(BaseSketchObject):
  def __init__(
    self,
    feature_count: int = 2,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    label_text = Text( txt = str(feature_count)+"x" , font_size = drafting_specs.font_size , align = (Align.MIN,Align.CENTER) )
    super().__init__(obj=label_text, rotation=rotation, align=align, mode=mode)

class Parallelism(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    separation_factor = 5 
    line_angle = 70
    corner_offset = drafting_specs.font_size * cos( line_angle * pi / 180 )/2
    sym = Compound([
      Edge.make_line(
          (-drafting_specs.font_size/separation_factor - corner_offset , -drafting_specs.font_size/2) ,
          (-drafting_specs.font_size/separation_factor + corner_offset ,  drafting_specs.font_size/2)
        ),
      Edge.make_line(
          ( drafting_specs.font_size/separation_factor - corner_offset , -drafting_specs.font_size/2) ,
          ( drafting_specs.font_size/separation_factor + corner_offset ,  drafting_specs.font_size/2)
        ),
    ])
    traced = trace( sym , drafting_specs.line_width )
    super().__init__(obj = traced , rotation = rotation , align = align , mode = mode )

class Perpendicularity(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    sym = Compound([
      Edge.make_line( (-drafting_specs.font_size/1.5,-drafting_specs.font_size/2) , (drafting_specs.font_size/1.5,-drafting_specs.font_size/2) ),
      Edge.make_line( (0,-drafting_specs.font_size/2) , (0,drafting_specs.font_size/2) ),
    ])
    traced = trace( sym , drafting_specs.line_width )
    super().__init__(obj = traced , rotation = rotation , align = align , mode = mode )

class SurfaceProfile(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    sym = Compound([ Edge.make_line( (-drafting_specs.font_size/2,0) , (drafting_specs.font_size/2,0) ) , CenterArc( center = (0,0) , radius = drafting_specs.font_size/2 , start_angle = 0 , arc_size = 180 ) ])
    traced = trace( sym , drafting_specs.line_width )
    super().__init__(obj = traced , rotation = rotation , align = align , mode = mode)

class ThirdAngleProjection(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    feature_size = drafting_specs.font_size
    horiz_offset = feature_size
    top_view = Pos( -horiz_offset ) * Compound([
      Circle( radius = feature_size/2 ),
      Circle( radius = feature_size/4 )
    ])
    right_view = Pos( horiz_offset ) * Polyline( [ (-feature_size/2,feature_size/4) , (feature_size/2,feature_size/2) , (feature_size/2,-feature_size/2) , (-feature_size/2,-feature_size/4) ] , close = True )
    lines = Pos(top_view.center(CenterOf.BOUNDING_BOX)) * Edge.make_line( (0,feature_size/2 + feature_size*0.2) , (0,-feature_size/2 - feature_size*0.2) )
    lines += Pos(top_view.center(CenterOf.BOUNDING_BOX)) * Edge.make_line( (-feature_size/2 - feature_size*0.2,0) , (5*feature_size/2 + feature_size*0.2,0) )

    symbol = Compound([
      trace( top_view , drafting_specs.line_width ),
      trace( right_view , drafting_specs.line_width ),
      trace( lines , drafting_specs.line_width )
    ] )
    super().__init__(obj=symbol, rotation=rotation, align=align, mode=mode)

class TruePosition(BaseSketchObject):
  def __init__(
    self,
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1),
    mode: Mode = Mode.ADD,
    align: Align = Align.CENTER,
    rotation: float = 0,
  ):
    true_pos_traced = Compound([
      trace( Circle( radius = drafting_specs.font_size/2 ) , drafting_specs.line_width ),
      trace( Edge.make_line( (0,1.5*drafting_specs.font_size/2) , (0,-1.5*drafting_specs.font_size/2) ) , drafting_specs.line_width ),
      trace( Edge.make_line( (-1.5*drafting_specs.font_size/2,0) , (1.5*drafting_specs.font_size/2,0) ) , drafting_specs.line_width )
    ])
    super().__init__(obj=true_pos_traced, rotation=rotation, align=align, mode=mode)



class GDTFeatureControlFrame(BaseSketchObject):

  #TODO : NOTE THAT THIS FCF IS ONLY REALLY USABLE FOR POSITION TOLERANCE CALLOUTS AT PRESENT

  """Sketch Object: GDTFeatureControlFrame

    GD&T Feature Control Frame

    Args:
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.
    """

  def __init__(
    self,
    controlled_feature,
    num_datums: int = 3,
    datum_labels: [""] = ["A","B","C"],
    feature_value: float = 0,
    num_feature_chars: int = 4,
    feature_modifier: str = "M",
    drafting_specs: Draft = Draft( font_size = 5 , line_width = 0.1 ),
    mode: Mode = Mode.ADD,
  ):
    block_dim = drafting_specs.font_size * 1.75
    #* Boxes
    r1 = Rectangle( width = block_dim , height = block_dim , align = (Align.MIN , Align.CENTER) , mode = Mode.PRIVATE )
    r2 = Pos( r1.edges().sort_by(Axis.X)[-1].center() ) * Rectangle( width = 3*block_dim , height = block_dim , align = (Align.MIN , Align.CENTER) , mode = Mode.PRIVATE )
    if num_datums > 0:
      r3 = Pos( r2.edges().sort_by(Axis.X)[-1].center() ) * Rectangle( width = block_dim , height = block_dim , align = (Align.MIN , Align.CENTER) , mode = Mode.PRIVATE )
    if num_datums > 1:
      r4 = Pos( r3.edges().sort_by(Axis.X)[-1].center() ) * Rectangle( width = block_dim , height = block_dim , align = (Align.MIN , Align.CENTER) , mode = Mode.PRIVATE )
    if num_datums == 3:
      r5 = Pos( r4.edges().sort_by(Axis.X)[-1].center() ) * Rectangle( width = block_dim , height = block_dim , align = (Align.MIN , Align.CENTER) , mode = Mode.PRIVATE )


    if num_datums == 0:
      boxes_edges = Edge.make_line( r1.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[-1] , r2.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1] )
      boxes_edges += Edge.make_line( r1.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0] , r2.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0] )
    elif num_datums == 1:
      boxes_edges = Edge.make_line( r1.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[-1] , r3.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1] )
      boxes_edges += Edge.make_line( r1.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0] , r3.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0] )
    elif num_datums == 2:
      boxes_edges = Edge.make_line( r1.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[-1] , r4.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1] )
      boxes_edges += Edge.make_line( r1.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0] , r4.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0] )
    else:
      boxes_edges = Edge.make_line( r1.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[-1] , r5.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1] )
      boxes_edges += Edge.make_line( r1.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0] , r5.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0] )
    boxes_edges += Edge.make_line( r1.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[-1] , r1.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0] )
    boxes_edges += Edge.make_line( r1.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1] , r1.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0] )
    boxes_edges += Edge.make_line( r2.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1] , r2.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0] )
    if num_datums > 0:
      boxes_edges += Edge.make_line( r3.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1] , r3.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0] )
    if num_datums > 1:
      boxes_edges += Edge.make_line( r4.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1] , r4.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0] )
    if num_datums > 2:
      boxes_edges += Edge.make_line( r5.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1] , r5.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0] )
      

    #* Datum box labels
    A_label , B_label , C_label = Text( txt = "" , font_size = drafting_specs.font_size ) , Text( txt = "" , font_size = drafting_specs.font_size ) , Text( txt = "" , font_size = drafting_specs.font_size )

    if num_datums > 0:
      A_label = Text( txt = datum_labels[0] , font_size = drafting_specs.font_size )
      A_label.position = r3.center()
    if num_datums > 1:
      B_label = Text( txt = datum_labels[1] , font_size = drafting_specs.font_size )
      B_label.position = r4.center()
    if num_datums > 2:
      C_label = Text( txt = datum_labels[2] , font_size = drafting_specs.font_size )
      C_label.position = r5.center()

    datum_labels = Compound([A_label , B_label , C_label])

    #* Controlled Feature Symbol
    controlled_feature_sym = Pos( r1.center() ) * controlled_feature

    #* Diameter Symbol
    diam_sym_offset = (-block_dim,0)
    diam_sym = Pos( r2.center() + diam_sym_offset ) * Diameter( drafting_specs )

    #* MMC Symbol
    modifier_sym_offset = (block_dim,0)
    modifier_sym = Pos( r2.center() + modifier_sym_offset ) * CircledLetterLabel( feature_label = feature_modifier , drafting_specs = drafting_specs )
    feature_value_string = str( feature_value )
    if len(feature_value_string) > num_feature_chars:
      feature_value_string = feature_value_string[0:num_feature_chars]
    tolerance_zone_value = Text( txt = feature_value_string , font_size = drafting_specs.font_size )
    tolerance_zone_value.position = r2.center()


    #* Trace Things
    boxes_traced = trace( boxes_edges, drafting_specs.line_width )

    gdt_mmc = Compound( [
      boxes_traced ,
      datum_labels ,
      controlled_feature_sym ,
      diam_sym ,
      modifier_sym,
      tolerance_zone_value
    ] )

    super().__init__(obj=gdt_mmc, rotation=0, align=None, mode=mode)





if __name__ == "__main__":
  from ocp_vscode import *
  show(
    GDTFeatureControlFrame( controlled_feature = TruePosition() )
  )