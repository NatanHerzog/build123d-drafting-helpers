from build123d import *
from math import *

# PROJECTION HELPERS
# Designed By: Natan Herzog
# Referenced From: https://build123d.readthedocs.io/en/latest/tech_drawing_tutorial.html

def projection(   # This is just a renamed version of the function in the docs above
  part: Part ,
  viewport_origin : VectorLike ,
  viewport_up : VectorLike ,
  page_origin : VectorLike ,
  scale_factor : float = 1.0 ,
) -> tuple[ ShapeList[ Edge ]  , ShapeList[ Edge ] ]:

  scaled_part = part if scale_factor == 1.0 else scale( part , scale_factor )
  visible , hidden = scaled_part.project_to_viewport(
    viewport_origin = viewport_origin ,
    viewport_up = viewport_up ,
    look_at = ( 0 , 0 , 0 )
  )
  visible = [ Pos( *page_origin ) * e for e in visible ]
  hidden = [ Pos( *page_origin ) * e for e in hidden ]
  return ShapeList( visible ) , ShapeList( hidden )


def allOrthographicViews(
  part: Part ,
  front_viewport_origin : VectorLike ,
  front_viewport_up : VectorLike ,
  horizontal_offset : float ,
  vertical_offset : float ,
  positions : {str : VectorLike} ,
  scale_factor : float = 1.0 ,
) -> tuple[ ShapeList[ Edge ] , ShapeList[ Edge ] ]:

  if positions == None:
    positions = {
      "front" : (0,0) ,
      "right" : ( horizontal_offset , 0 ),
      "left"  : (-horizontal_offset , 0 ),
      "back"  : (-2*horizontal_offset , 0 ),
      "top"   : ( 0 , vertical_offset ),
      "bottom": ( 0 ,-vertical_offset )
    }
  
  scaled_part = part if scale_factor == 1.0 else scale( part , scale_factor )

  front_view_normal = Vector( front_viewport_up ).cross( Vector( front_viewport_origin ) )
  up_axis = Axis( (0,0,0) , front_viewport_up )
  forward_axis = Axis( (0,0,0) , front_viewport_origin )
  right_axis = Axis( (0,0,0) , front_view_normal )

  right_viewport_origin = Vector( front_viewport_origin ).rotate( up_axis , 90 )
  left_viewport_origin = Vector( front_viewport_origin ).rotate( up_axis , 270 )
  back_viewport_origin = Vector( front_viewport_origin ).rotate( up_axis , 180 )
  top_viewport_origin = Vector( front_viewport_origin ).rotate( right_axis , 270 )
  bottom_viewport_origin = Vector( front_viewport_origin ).rotate( right_axis , 90 )
  
  right_viewport_up = Vector( front_viewport_up ).rotate( up_axis , 90 )
  left_viewport_up = Vector( front_viewport_up ).rotate( up_axis , 270 )
  back_viewport_up = Vector( front_viewport_up ).rotate( up_axis , 180 )
  top_viewport_up = Vector( front_viewport_up ).rotate( right_axis , 270 )
  bottom_viewport_up = Vector( front_viewport_up ).rotate( right_axis , 90 )

  front_visible , front_hidden = scaled_part.project_to_viewport(
    viewport_origin = front_viewport_origin,
    viewport_up = front_viewport_up,
    look_at = ( 0 , 0 , 0 )
  )
  right_visible , right_hidden = scaled_part.project_to_viewport(
    viewport_origin = right_viewport_origin,
    viewport_up = front_viewport_up,
    look_at = ( 0 , 0 , 0 )
  )
  left_visible , left_hidden = scaled_part.project_to_viewport(
    viewport_origin = left_viewport_origin,
    viewport_up = front_viewport_up,
    look_at = ( 0 , 0 , 0 )
  )
  back_visible , back_hidden = scaled_part.project_to_viewport(
    viewport_origin = back_viewport_origin,
    viewport_up = back_viewport_up,
    look_at = ( 0 , 0 , 0 )
  )
  top_visible , top_hidden = scaled_part.project_to_viewport(
    viewport_origin = top_viewport_origin,
    viewport_up = top_viewport_up,
    look_at = ( 0 , 0 , 0 )
  )
  bottom_visible , bottom_hidden = scaled_part.project_to_viewport(
    viewport_origin = bottom_viewport_origin,
    viewport_up = bottom_viewport_up,
    look_at = ( 0 , 0 , 0 )
  )

  iso_1_visible , iso_1_hidden = scaled_part.project_to_viewport(
    viewport_origin = Vector(front_viewport_origin) + Vector(front_viewport_up) - front_view_normal,
    viewport_up = front_viewport_up,
    look_at = (0,0,0)
  )
  iso_2_visible , iso_2_hidden = scaled_part.project_to_viewport(
    viewport_origin = Vector(front_viewport_origin) + Vector(front_viewport_up) + front_view_normal,
    viewport_up = front_viewport_up,
    look_at = (0,0,0)
  )
  iso_3_visible , iso_3_hidden = scaled_part.project_to_viewport(
    viewport_origin = Vector(front_viewport_origin) - Vector(front_viewport_up) + front_view_normal,
    viewport_up = front_viewport_up,
    look_at = (0,0,0)
  )
  iso_4_visible , iso_4_hidden = scaled_part.project_to_viewport(
    viewport_origin = Vector(front_viewport_origin) - Vector(front_viewport_up) - front_view_normal,
    viewport_up = front_viewport_up,
    look_at = (0,0,0)
  )

  #TODO : I am REALLY not confident that these are correct
  iso_5_visible , iso_5_hidden = scaled_part.project_to_viewport(
    viewport_origin = -Vector(front_viewport_origin) + Vector(front_viewport_up) - front_view_normal,
    viewport_up = front_viewport_up,
    look_at = (0,0,0)
  )
  iso_6_visible , iso_6_hidden = scaled_part.project_to_viewport(
    viewport_origin = -Vector(front_viewport_origin) + Vector(front_viewport_up) + front_view_normal,
    viewport_up = front_viewport_up,
    look_at = (0,0,0)
  )
  iso_7_visible , iso_7_hidden = scaled_part.project_to_viewport(
    viewport_origin = -Vector(front_viewport_origin) - Vector(front_viewport_up) + front_view_normal,
    viewport_up = front_viewport_up,
    look_at = (0,0,0)
  )
  iso_8_visible , iso_8_hidden = scaled_part.project_to_viewport(
    viewport_origin = -Vector(front_viewport_origin) - Vector(front_viewport_up) - front_view_normal,
    viewport_up = front_viewport_up,
    look_at = (0,0,0)
  )

  visible = {
    "front"   : Pos( positions["front"] )   * Compound( front_visible ),
    "right"   : Pos( positions["right"] )   * Compound( right_visible ),
    "left"    : Pos( positions["left"] )    * Compound( left_visible ),
    "back"    : Pos( positions["back"] )    * Compound( back_visible ),
    "top"     : Pos( positions["top"] )     * Compound( top_visible ),
    "bottom"  : Pos( positions["bottom"] )  * Compound( bottom_visible ),
    "iso 1"   : Compound( iso_1_visible ),
    "iso 2"   : Compound( iso_2_visible ),
    "iso 3"   : Compound( iso_3_visible ),
    "iso 4"   : Compound( iso_4_visible ),
    "iso 5"   : Compound( iso_5_visible ),
    "iso 6"   : Compound( iso_6_visible ),
    "iso 7"   : Compound( iso_7_visible ),
    "iso 8"   : Compound( iso_8_visible ),
  }
  hidden = {
    "front"   : Pos( positions["front"] )   * Compound( front_hidden ),
    "right"   : Pos( positions["right"] )   * Compound( right_hidden ),
    "left"    : Pos( positions["left"] )    * Compound( left_hidden ),
    "back"    : Pos( positions["back"] )    * Compound( back_hidden ),
    "top"     : Pos( positions["top"] )     * Compound( top_hidden ),
    "bottom"  : Pos( positions["bottom"] )  * Compound( bottom_hidden ),
    "iso 1"   : Compound( iso_1_hidden ),
    "iso 2"   : Compound( iso_2_hidden ),
    "iso 3"   : Compound( iso_3_hidden ),
    "iso 4"   : Compound( iso_4_hidden ),
    "iso 5"   : Compound( iso_5_hidden ),
    "iso 6"   : Compound( iso_6_hidden ),
    "iso 7"   : Compound( iso_7_hidden ),
    "iso 8"   : Compound( iso_8_hidden ),
  }
  return visible , hidden


if __name__ == "__main__":
  from ocp_vscode import *

  a = Box( 1 , 1 , 1 ) + Pos( (0.5,0.5,0.5) ) * Sphere( radius = 0.2 )

  view_origin = (1,0,0)
  view_up = (0,0,1)

  a_vis_1 , a_hid_1 = projection(
    part = a,
    viewport_origin= view_origin,
    viewport_up = view_up ,
    page_origin = (0,0),
    scale_factor = 1.0
  )

  a_vis_2 , a_hid_2 = allOrthographicViews(
    part = a,
    front_viewport_origin= view_origin,
    front_viewport_up = view_up,
    horizontal_offset= 2 ,
    vertical_offset= 2,
    positions = None,
    scale_factor = 1.0
  )

  show(
    a ,
    Compound([
      Compound( a_hid_2["front"] ),
      Compound( a_hid_2["right"] ),
      Compound( a_hid_2["left"] ),
      Compound( a_hid_2["back"] ),
      Compound( a_hid_2["back"] ),
      Compound( a_hid_2["top"] ),
      Compound( a_hid_2["bottom"] ),
    ]),
    Compound([
      Compound( a_vis_2["front"] ),
      Compound( a_vis_2["right"] ),
      Compound( a_vis_2["left"] ),
      Compound( a_vis_2["back"] ),
      Compound( a_vis_2["back"] ),
      Compound( a_vis_2["top"] ),
      Compound( a_vis_2["bottom"] ),
    ]),
    colors = [
      "#CCC" , "#CCC" , "#000",
    ]
  )