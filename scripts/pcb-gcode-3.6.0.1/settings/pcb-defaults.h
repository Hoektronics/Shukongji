//
// Default values for generating gcode from a PCB.
//
// These settings were last changed with pcb-gcode-setup: 1/4/13 9:30 PM
//
//
// Changes you make in this file will be overwritten if you use pcb-gcode-setup.
//

int SINGLE_PASS = NO;
real ISO_MIN = 0.100000;
real ISO_MAX = 0.250000;
real ISO_STEP = 0.150000;

int GENERATE_TOP_OUTLINES = YES;
int GENERATE_TOP_DRILL = YES;
int GENERATE_TOP_FILL = NO;

int GENERATE_BOTTOM_OUTLINES = NO;
int GENERATE_BOTTOM_DRILL = NO;
int GENERATE_BOTTOM_FILL = NO;
int MIRROR_BOTTOM = NO;
int SIMPLE_DRILL_CODE = NO;

int GENERATE_MILLING = NO;

int GENERATE_TEXT = NO;

int SPOT_DRILL = NO;
real SPOT_DRILL_DEPTH = -0.300000;

int DO_TOOL_CHANGE_WITH_ZERO_STEP = YES;

int FLIP_BOARD_IN_Y = NO;

//int OUTPUT_UNITS = U_MICRONS;
int OUTPUT_UNITS = U_MILLIMETERS;
//int OUTPUT_UNITS = U_MILS;
//int OUTPUT_UNITS = U_INCHES;
