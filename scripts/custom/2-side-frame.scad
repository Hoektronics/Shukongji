width = 42.3;
height = 32;
thickness = 10.75;

//frame
//frame(width, height, thickness, 3.05);

//base
frame(width, height, thickness, 2.5);

$fs = 0.1;

module frame(width, height, thickness, holesize)
{
	width = width+18;
	height = height+18;
	halfwidth = width/2;
	halfheight = height/2;
	holex = halfwidth-3+0.5;
	holey = halfheight-3+0.5;

	difference()
	{
		translate([-halfwidth, -halfheight, 0])
			cube([width, height, thickness]);

		translate([-holex, 0, thickness/2])
			cylinder(r=holesize/2, h=thickness+1, center=true);
		translate([holex, -holey, thickness/2])
			cylinder(r=holesize/2, h=thickness+1, center=true);
		translate([holex, holey, thickness/2])
			cylinder(r=holesize/2, h=thickness+1, center=true);
	}
}
