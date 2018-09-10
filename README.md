# mview

Mview is a 3D visulization script written in python to view the molecular
structures contained in files like VASP POSCAR. The script utilizes
[ASE](https://wiki.fysik.dtu.dk/ase/ase/io/io.html) to read the structural
information from input files, therefore, the input file formats are not limited
to VASP POSCAR. In principle, any file format that can be recognized by ASE can
be used as input. For 3D visulization, it utilizes
[mayavi](https://docs.enthought.com/mayavi/mayavi/) to do the plotting work.

In addition, the script can also plot the vibration mode with arrows if the
vibrational modes are provided.

## Prerequisites

The following python library must be installed to run the script

* [numpy](https://wiki.fysik.dtu.dk/ase/ase/io/io.html)
* [ase](https://wiki.fysik.dtu.dk/ase/ase/io/io.html)
* [mayavi](https://docs.enthought.com/mayavi/mayavi/)

## Examples

The following line shows the possible functions of the script:

1. designate the input files by `-i POSCAR`
2. make a 2x2x1 supercell by `-r 2 2 1`
3. set the background color to black by `-bg 0 0 0`, where `0 0 0` is the RGB
   triplet, each with value in [0,1]
4. save the figure `-o out.png`. The output image format is determined by the
   suffix of the output file name.
5. show the second vibration mode with arrows `-n 2`. The OUTCAR containing the
   normal mode should be designated by `-outcar /path/to/OUTCAR`.
6. set the azimuth and elevation view angle by `-phi` and `-theta`.
7. do not show the mayavi UI `-q`

```bash
mview -i POSCAR -r 2 2 1 -bg 0 0 0 -o out.png -n 2 -phi 0 -theta 90 -q
```

The resulting image looks like this:

![mview_example](examples/out.png)
