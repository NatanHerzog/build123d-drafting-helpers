from build123d import *
from math import *

# GDT FEATURE SYMBOLS
# Designed By: Natan Herzog
# Referenced From: gdtandbasics.com/gdt-symbols

class CrossHair(BaseSketchObject):
  def __init__(
    self,
    draft_font_size: int = 5,
    line_width: float = 0.2,
    mode: Mode = Mode.ADD,
  ):
    true_pos_sym = Compound([ Edge.make_line( (0,1.5*draft_font_size/2) , (0,-1.5*draft_font_size/2) ) , Edge.make_line( (-1.5*draft_font_size/2,0) , (1.5*draft_font_size/2,0) ) ])
    true_pos_traced = trace( true_pos_sym , line_width )
    super().__init__(obj=true_pos_traced, rotation=0, align=None, mode=mode)

class TruePosition(BaseSketchObject):
  def __init__(
    self,
    draft_font_size: int = 5,
    line_width: float = 0.2,
    mode: Mode = Mode.ADD,
  ):
    true_pos_sym = Compound([ Circle( radius = draft_font_size/2 ).edges()[0] , Edge.make_line( (0,1.5*draft_font_size/2) , (0,-1.5*draft_font_size/2) ) , Edge.make_line( (-1.5*draft_font_size/2,0) , (1.5*draft_font_size/2,0) ) ])
    true_pos_traced = trace( true_pos_sym , line_width )
    super().__init__(obj=true_pos_traced, rotation=0, align=None, mode=mode)



class DatumFeature(BaseSketchObject):
  def __init__(
    self,
    datum_label: str = "",
    draft_font_size: int = 5,
    line_width: float = 0.2,
    mode: Mode = Mode.ADD,
  ):
    feature_size = draft_font_size * 1.5
    triangle = Triangle( a = feature_size , B = 60 , C = 60 , align = (Align.CENTER , Align.MIN) )
    flagpole = Edge.make_line(
      triangle.vertices().sort_by(Axis.Y)[-1] + (0,-line_width),
      triangle.vertices().sort_by(Axis.Y)[-1] + (0,feature_size/3),
    )
    box = Pos( flagpole.vertices().sort_by(Axis.Y)[-1] ) * Rectangle( width = feature_size , height = feature_size , align = (Align.CENTER , Align.MIN) )
    box_edges = box.edges()
    label = Text( txt = datum_label , font_size = draft_font_size )
    label.position = box.center()

    datum = Compound([
      triangle ,
      trace( flagpole , line_width ) ,
      trace( box_edges , line_width ) ,
      label
      ] )
    super().__init__(obj=datum, rotation=0, align=None, mode=mode)



class CircledLetterLabel(BaseSketchObject):
  def __init__(
    self,
    feature_label: str = "",
    draft_font_size: int = 5,
    line_width: float = 0.2,
    mode: Mode = Mode.ADD,
  ):
    circle = Circle( radius = draft_font_size*1.5/2 )
    label_text = Text( txt = feature_label , font_size = draft_font_size )
    label_text.position = circle.center(CenterOf.BOUNDING_BOX)
    label = Compound([
      trace(circle , line_width),
      label_text
    ])
    super().__init__(obj=label, rotation=0, align=None, mode=mode)



class CounterBore(BaseSketchObject):
  def __init__(
    self,
    feature_size: float = 5,
    line_width: float = 0.2,
    mode: Mode = Mode.ADD,
  ):
    symbol_lines = Edge.make_line(
      (0,-feature_size/4) , (feature_size,-feature_size/4)
    )
    symbol_lines += Edge.make_line(
      (0,-feature_size/4) , (0,feature_size/4)
    )
    symbol_lines += Edge.make_line(
      (feature_size,-feature_size/4) , (feature_size,feature_size/4)
    )
    symbol = trace( symbol_lines , line_width )
    super().__init__(obj=symbol, rotation=0, align=None, mode=mode)



class Diameter(BaseSketchObject):
  def __init__(
    self,
    feature_size: float = 5 ,
    line_width: float = 0.2 ,
    mode: Mode = Mode.ADD,
  ):
    circle = Circle( radius = feature_size/2 )
    line = Edge.make_line( (1.2*feature_size/2 , 1.2*feature_size/2) , (-1.2*feature_size/2 , -1.2*feature_size/2) )
    symbol = Compound([
      trace( circle , line_width ),
      trace( line , line_width )
    ])

    super().__init__(obj=symbol, rotation=0, align=None, mode=mode)



class DepthSymbol(BaseSketchObject):
  def __init__(
    self,
    feature_size: float = 5 ,
    line_width: float = 0.2 ,
    mode: Mode = Mode.ADD,
  ):
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
      trace( lines , line_width ),
      trace( arrow , line_width )
    ])
    super().__init__(obj=symbol, rotation=0, align=None, mode=mode)



class MultipleFeatures(BaseSketchObject):
  def __init__(
    self,
    feature_count: int = 2,
    draft_font_size: int = 5,
    mode: Mode = Mode.ADD,
  ):
    label_text = Text( txt = str(feature_count)+"x" , font_size = draft_font_size , align = (Align.MIN,Align.CENTER) )
    super().__init__(obj=label_text, rotation=0, align=None, mode=mode)



class ThirdAngleProjection(BaseSketchObject):
  def __init__(
    self,
    feature_size: float = 10,
    line_width: float = 0.5,
    mode: Mode = Mode.ADD,
  ):
    horiz_offset = feature_size
    top_view = Pos( -horiz_offset ) * Compound([
      Circle( radius = feature_size/2 ),
      Circle( radius = feature_size/4 )
    ])
    right_view = Pos( horiz_offset ) * Polyline( [ (-feature_size/2,feature_size/4) , (feature_size/2,feature_size/2) , (feature_size/2,-feature_size/2) , (-feature_size/2,-feature_size/4) ] , close = True )
    lines = Pos(top_view.center(CenterOf.BOUNDING_BOX)) * Edge.make_line( (0,feature_size/2 + feature_size*0.2) , (0,-feature_size/2 - feature_size*0.2) )
    lines += Pos(top_view.center(CenterOf.BOUNDING_BOX)) * Edge.make_line( (-feature_size/2 - feature_size*0.2,0) , (5*feature_size/2 + feature_size*0.2,0) )

    symbol = Compound([
      trace( top_view , line_width ),
      trace( right_view , line_width ),
      trace( lines , line_width )
    ] )
    super().__init__(obj=symbol, rotation=0, align=None, mode=mode)


class GDTFeatureControlFrame(BaseSketchObject):

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
    block_dim: float = 0.5*IN,
    draft_font_size: int = 5,
    line_width: int = 0.1,
    feature_value: float = 0,
    num_feature_chars: int = 4,
    feature_modifier: str = "M",
    mode: Mode = Mode.ADD,
  ):
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
    A_label , B_label , C_label = Text( txt = "" , font_size = draft_font_size ) , Text( txt = "" , font_size = draft_font_size ) , Text( txt = "" , font_size = draft_font_size )

    if num_datums > 0:
      A_label = Text( txt = datum_labels[0] , font_size = draft_font_size )
      A_label.position = r3.center()
    if num_datums > 1:
      B_label = Text( txt = datum_labels[1] , font_size = draft_font_size )
      B_label.position = r4.center()
    if num_datums > 2:
      C_label = Text( txt = datum_labels[2] , font_size = draft_font_size )
      C_label.position = r5.center()

    datum_labels = Compound([A_label , B_label , C_label])

    #* Controlled Feature Symbol
    controlled_feature_sym = Pos( r1.center() ) * controlled_feature

    #* Diameter Symbol
    diam_sym_offset = (-block_dim,0)
    diam_sym = Pos( r2.center() + diam_sym_offset ) * Diameter( feature_size = draft_font_size , line_width = line_width )

    #* MMC Symbol
    modifier_sym_offset = (block_dim,0)
    modifier_sym = Pos( r2.center() + modifier_sym_offset ) * CircledLetterLabel( feature_label = feature_modifier , draft_font_size= draft_font_size , line_width = line_width )
    feature_value_string = str( feature_value )
    if len(feature_value_string) > num_feature_chars:
      feature_value_string = feature_value_string[0:num_feature_chars]
    tolerance_zone_value = Text( txt = feature_value_string , font_size = draft_font_size )
    tolerance_zone_value.position = r2.center()


    #* Trace Things
    boxes_traced = trace( boxes_edges, line_width , mode = mode.PRIVATE )

    gdt_mmc = Compound( [
      boxes_traced ,
      datum_labels ,
      controlled_feature_sym ,
      diam_sym ,
      modifier_sym,
      tolerance_zone_value
    ] )

    super().__init__(obj=gdt_mmc, rotation=0, align=None, mode=mode)