from build123d import *
from math import *

# HOLE CALLOUT COMPOUNDS
# Designed By: Natan Herzog
# Referenced From: https://build123d.readthedocs.io/en/latest/_modules/drafting.html#TechnicalDrawing


class Drawing(BaseSketchObject):
    """Sketch Object: Drawing

    The border of a technical drawing with external frame and text box.

    Args:
        designed_by (str, optional)         : Defaults to "DRAWING AUTHOR".
        design_date (date, optional)        : Defaults to date.today().
        project_name (str, optional)        : Defaults to "PROJECT NAME".
        part_name (str, optional)           : Defaults to "PART NAME".
        drawing_number (str, optional)      : Defaults to "DWG-#".
        projection_type (int, optional)     : Defaults to 3.
        drawing_scale (int, optional)       : Defaults to 1.
        units (str, optional)               : Defaults to "IN".
        sheet_number (int, optional)        : Defaults to 1.
        sheet_count (int, optional)         : Defaults to 1.
        page_size (PageSize, optional)      : Defaults to PageSize.A4.
        nominal_text_size (float, optional) : size of title text. Defaults to 10.0.
        line_width (float, optional)        : Defaults to 0.5.
        mode (Mode, optional)               : combination mode. Defaults to Mode.ADD.
    """

    page_sizes = {
        PageSize.A0: (1189 * MM, 841 * MM),
        PageSize.A1: (841 * MM, 594 * MM),
        PageSize.A2: (594 * MM, 420 * MM),
        PageSize.A3: (420 * MM, 297 * MM),
        PageSize.A4: (297 * MM, 210 * MM),
        PageSize.A5: (210 * MM, 148.5 * MM),
        PageSize.A6: (148.5 * MM, 105 * MM),
        PageSize.A7: (105 * MM, 74 * MM),
        PageSize.A8: (74 * MM, 52 * MM),
        PageSize.A9: (52 * MM, 37 * MM),
        PageSize.A10: (37 * MM, 26 * MM),
        PageSize.LETTER: (11 * IN, 8.5 * IN),
        PageSize.LEGAL: (14 * IN, 8.5 * IN),
        PageSize.LEDGER: (17 * IN, 11 * IN),
    }
    margin = 5 * MM

    def __init__(
        self,
        designed_by: str = "DRAWING AUTHOR",
        design_date: date | None = None,
        project_name: str = "PROJECT NAME",
        part_name: str = "PART NAME",
        drawing_number: str = "DWG-#",
        projection_type: int = 3,
        drawing_scale: float = 1,
        units: str = "IN",
        sheet_number: int = 1,
        sheet_count: int = 1,
        page_size: PageSize = PageSize.A2,
        nominal_text_size: float = 10.0,
        line_width: float = 1,
        mode: Mode = Mode.ADD,
    ):
        # pylint: disable=too-many-locals

        if design_date is None:
            design_date = date.today()

        page_dim = VTGDrawing.page_sizes[page_size]
        
        
        #* Frame
        frame_width = page_dim[0] - 2 * VTGDrawing.margin - 2 * nominal_text_size
        frame_height = 2 * frame_width / 3
        frame_wire = Wire.make_polygon(
            [
                (-frame_width / 2, frame_height / 2),
                (frame_width / 2, frame_height / 2),
                (frame_width / 2, -frame_height / 2),
                (-frame_width / 2, -frame_height / 2),
            ],
        )
        frame = trace(frame_wire, line_width, mode=Mode.PRIVATE)
        
        
        #* Ticks
        tick_lines = []
        for i in range(20):
            if i in [0, 6, 10, 16]:  # corners
                continue
            u_value = i / 20
            pos = frame_wire.position_at(u_value)
            tick_lines.append(
                Edge.make_line(
                    pos,
                    pos
                    + Vector(nominal_text_size, 0).rotate(
                        Axis.Z, frame_wire.tangent_angle_at(u_value) + 90
                    ),
                )
            )
        ticks = trace(tick_lines, line_width, mode=Mode.PRIVATE)
        # Numbers
        grid_labels = Sketch()
        y_centers = {0: -3 / 8, 1: -1 / 8, 2: 1 / 8, 3: 3 / 8}
        for label in range(4):
            for x_index in [-0.5, 0.5]:
                grid_labels += Pos(
                    x_index * (frame_width + 1.25 * nominal_text_size),
                    y_centers[label] * frame_height,
                ) * Sketch(
                    Compound.make_text(str(label + 1), nominal_text_size).wrapped
                )

        
        
        #* Letters
        x_centers = {
            0: -5 / 12,
            1: -3 / 12,
            2: -1 / 12,
            3: 1 / 12,
            4: 3 / 12,
            5: 5 / 12,
        }
        for i, grid_label in enumerate(["F", "E", "D", "C", "B", "A"]):
            for y_index in [-0.5, 0.5]:
                grid_labels += Pos(
                    x_centers[i] * frame_width,
                    y_index * (frame_height + 1.25 * nominal_text_size),
                ) * Sketch(Compound.make_text(grid_label, nominal_text_size).wrapped)

        
        
        #* Text Box Frame
        text_frame_botleft = frame_wire.edges().sort_by(Axis.Y)[0]@0.5
        text_frame_topright = frame_wire.edges().sort_by(Axis.X)[-1]@0.75
        text_frame_topleft = (text_frame_botleft.X , text_frame_topright.Y)
        text_frame_curve = Wire.make_polygon( [text_frame_botleft , text_frame_topleft , text_frame_topright] , close = False )



        #* Text Positioning Boxes
        row_height = frame_height / 20
        text_box = Pos(frame.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]) * Rectangle( width = frame_width/2 , height = frame_height/4 , align = (Align.MAX , Align.MIN) )
        
        row1_col1_box = Pos(text_box.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[-1]) * Rectangle( width = frame_width/2/6 - line_width/2 , height = row_height , align = (Align.MIN , Align.MAX) )
        row1_col2_box = Pos(row1_col1_box.edges().sort_by(Axis.X)[-1].center()) * Rectangle( width = frame_width/2*5/6 , height = row_height , align = (Align.MIN , Align.CENTER) )
        
        row2_col1_box = Pos(row1_col1_box.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0]) * Rectangle( width = frame_width/2/6 - line_width/2 , height = row_height , align = (Align.MIN , Align.MAX) )
        row2_col2_box = Pos(row2_col1_box.edges().sort_by(Axis.X)[-1].center()) * Rectangle( width = frame_width/2 - frame_width/2/6 - frame_width/9 , height = row_height , align = (Align.MIN , Align.CENTER) )
        row2_col3_box = Pos(row2_col2_box.edges().sort_by(Axis.X)[-1].center()) * Rectangle( width = frame_width/9 , height = row_height , align = (Align.MIN , Align.CENTER) )
        
        row3_col1_box = Pos(row2_col1_box.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0]) * Rectangle( width = frame_width/2/6 - line_width/2 , height = row_height , align = (Align.MIN , Align.MAX) )
        row3_col2_box = Pos(row3_col1_box.edges().sort_by(Axis.X)[-1].center()) * Rectangle( width = frame_width/2 - frame_width/2/6 - frame_width/9 , height = row_height , align = (Align.MIN , Align.CENTER) )
        row3_col3_box = Pos(row3_col2_box.edges().sort_by(Axis.X)[-1].center()) * Rectangle( width = frame_width/9 , height = row_height , align = (Align.MIN , Align.CENTER) )
        
        row4_col1_box = Pos(row3_col1_box.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0]) * Rectangle( width = frame_width/6 - line_width/2, height = 2*row_height , align = (Align.MIN , Align.MAX) )
        row4_col2_box = Pos(row4_col1_box.edges().sort_by(Axis.X)[-1].center()) * Rectangle( width = frame_width/9 , height = 2*row_height , align = (Align.MIN , Align.CENTER) )
        row4_col3_box = Pos(row4_col2_box.edges().sort_by(Axis.X)[-1].center()) * Rectangle( width = frame_width/9 , height = 2*row_height , align = (Align.MIN , Align.CENTER) )
        row4_col4_box = Pos(row4_col3_box.edges().sort_by(Axis.X)[-1].center()) * Rectangle( width = frame_width/9 , height = 2*row_height , align = (Align.MIN , Align.CENTER) )


        #* Text Box Edges
        #! ROW 1
        text_frame_curve += Edge.make_line(
          row1_col1_box.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0],
          row1_col2_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )
        text_frame_curve += Edge.make_line(
          row1_col1_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1],
          row1_col1_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )

        #! ROW 2
        text_frame_curve += Edge.make_line(
          row2_col1_box.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0],
          row2_col3_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )
        text_frame_curve += Edge.make_line(
          row2_col1_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1],
          row2_col1_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )
        text_frame_curve += Edge.make_line(
          row2_col2_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1],
          row2_col2_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )
        
        #! ROW 3
        text_frame_curve += Edge.make_line(
          row3_col1_box.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[0],
          row3_col3_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )
        text_frame_curve += Edge.make_line(
          row3_col1_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1],
          row3_col1_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )
        text_frame_curve += Edge.make_line(
          row3_col2_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1],
          row3_col2_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )
        
        #! ROW 4
        text_frame_curve += Edge.make_line(
          row4_col1_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1],
          row4_col1_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )
        text_frame_curve += Edge.make_line(
          row4_col2_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1],
          row4_col2_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )
        text_frame_curve += Edge.make_line(
          row4_col3_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[-1],
          row4_col3_box.vertices().group_by(Axis.X)[-1].sort_by(Axis.Y)[0]
        )


        #* Text Labels
        project_label = Text( txt = "PROJECT" , font_size = nominal_text_size/1.5 , align = (Align.MAX , Align.CENTER) )
        project_label.position = row1_col1_box.edges().sort_by(Axis.X)[-1].center() + (-nominal_text_size/2,0,0)
        project_name_text = Text( txt = project_name , font_size = nominal_text_size , align = (Align.MIN , Align.CENTER) )
        project_name_text.position = row1_col2_box.edges().sort_by(Axis.X)[0].center() + (nominal_text_size/2,0,0)
        
        part_label = Text( txt = "PART" , font_size = nominal_text_size/1.5 , align = (Align.MAX , Align.CENTER) )
        part_label.position = row2_col1_box.edges().sort_by(Axis.X)[-1].center() + (-nominal_text_size/2,0,0)
        part_name_text = Text( txt = part_name , font_size = nominal_text_size , align = (Align.MIN , Align.CENTER) )
        part_name_text.position = row2_col2_box.edges().sort_by(Axis.X)[0].center() + (nominal_text_size/2,0,0)
        part_number_text = Text( txt = drawing_number , font_size = nominal_text_size/1.5 , align = (Align.CENTER , Align.CENTER) )
        part_number_text.position = row2_col3_box.center()

        designed_label = Text( txt = "DESIGNED" , font_size = nominal_text_size/1.5 , align = (Align.MAX , Align.CENTER) )
        designed_label.position = row3_col1_box.edges().sort_by(Axis.X)[-1].center() + (-nominal_text_size/2,0,0)
        designed_text = Text( txt = designed_by , font_size = nominal_text_size/1.5 , align = (Align.MIN , Align.CENTER) )
        designed_text.position = row3_col2_box.edges().sort_by(Axis.X)[0].center() + (nominal_text_size/2,0,0)
        date_text = Text( txt = design_date.isoformat() , font_size = nominal_text_size/1.5 , align = (Align.CENTER , Align.CENTER) )
        date_text.position = row3_col3_box.center()

        scale_label = Text( txt = "SCALE" , font_size = nominal_text_size/1.5 , align = (Align.CENTER , Align.MIN) )
        scale_label.position = row4_col2_box.center() + (0,nominal_text_size/1.5,0)
        scale_text = Text( txt = "1 : " + str(drawing_scale)[0:4] , font_size = nominal_text_size , align = (Align.CENTER , Align.MIN) )
        scale_text.position = row4_col2_box.center() + (0,-nominal_text_size,0)
        
        units_label = Text( txt = "UNITS" , font_size = nominal_text_size/1.5 , align = (Align.CENTER , Align.MIN) )
        units_label.position = row4_col3_box.center() + (0,nominal_text_size/1.5,0)
        units_text = Text( txt = units , font_size = nominal_text_size , align = (Align.CENTER , Align.MIN) )
        units_text.position = row4_col3_box.center() + (0,-nominal_text_size,0)
        
        page_label = Text( txt = "PAGE" , font_size = nominal_text_size/1.5 , align = (Align.CENTER , Align.MIN) )
        page_label.position = row4_col4_box.center() + (0,nominal_text_size/1.5,0)
        page_text = Text( txt = str(sheet_number) + " / " + str(sheet_count) , font_size = nominal_text_size , align = (Align.CENTER , Align.MIN) )
        page_text.position = row4_col4_box.center() + (0,-nominal_text_size,0)

        projection = Pos(row4_col1_box.center()) * ThirdAngleProjection( feature_size = nominal_text_size*1.5 , line_width = 1 )


        text_frame = trace( text_frame_curve , line_width , mode = Mode.PRIVATE )


        technical_drawing = Compound(
            children=[
              frame, ticks, grid_labels,
              text_frame ,
              project_label , project_name_text ,
              part_label , part_name_text , part_number_text ,
              designed_label , designed_text , date_text,
              scale_label , scale_text,
              units_label , units_text ,
              page_label , page_text,
              projection,
            ]
        )

        super().__init__(obj=technical_drawing, rotation=0, align=None, mode=mode)