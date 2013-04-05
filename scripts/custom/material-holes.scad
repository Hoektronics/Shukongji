width = 180;
height = 190;

//material
material(180, 190, 8.25, 3.1);

//base
//material(180, 190, 8.25, 2.5);

$fs = 0.1;

module material(width, height, thickness, holesize)
{
	halfwidth = width/2;
	halfheight = height/2;
	holex = halfwidth-3;
	holey = halfheight-3;

	difference()
	{
		translate([-halfwidth, -halfheight, 0])
			cube([width, height, thickness]);

		translate([-holex, -holey, thickness/2])
			cylinder(r=holesize/2, h=thickness+1, center=true);
		translate([holex, -holey, thickness/2])
			cylinder(r=holesize/2, h=thickness+1, center=true);
		translate([0, -holey, thickness/2])
			cylinder(r=holesize/2, h=thickness+1, center=true);
		translate([-holex, holey, thickness/2])
			cylinder(r=holesize/2, h=thickness+1, center=true);
		translate([holex, holey, thickness/2])
			cylinder(r=holesize/2, h=thickness+1, center=true);
		translate([0, holey, thickness/2])
			cylinder(r=holesize/2, h=thickness+1, center=true);
	}
}
