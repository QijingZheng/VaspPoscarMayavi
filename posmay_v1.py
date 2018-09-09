#!/usr/bin/env python

import numpy as np
from mayavi import mlab
from ase.io import read

import time

################################################################################

# Name, Atomic Number, Radius and Color for elements in the periodic table
ElementsNARC = np.loadtxt('elements.ini', dtype=str)
EleName      = list(ElementsNARC[:,0])
EleAnum      = np.array(ElementsNARC[:,1], dtype=int)
EleRadius    = np.array(ElementsNARC[:,2], dtype=float)
EleColors    = np.array(ElementsNARC[:,-3:], dtype=float)

# the maximum bond length between two elements
N = len(EleName)
B = np.loadtxt('bonds.ini', dtype=str)
maxBondLength = np.ones((N, N))
for e1, e2, L in B:
    i1 = EleName.index(e1)
    i2 = EleName.index(e2)
    maxBondLength[i1, i2] = maxBondLength[i2, i1] = float(L)

################################################################################

poscar       = read('POSCAR', format='vasp')
px, py, pz   = poscar.positions.T
nions        = poscar.get_number_of_atoms()
cell         = poscar.cell

atomsSymbols = poscar.get_chemical_symbols()
atomsIndex   = [EleName.index(nn) for nn in atomsSymbols]
atomsSize    = np.array([EleRadius[ii] for ii in atomsIndex])
atomsColor   = np.array([EleColors[ii] for ii in atomsIndex])

atomsSymbolsUniq = list(set(atomsSymbols))
ntype = len(atomsSymbolsUniq)
atomsLUT = np.array([EleColors[EleName.index(ss)] for ss in atomsSymbolsUniq])
# print atomsLUT
colorScalars = [atomsSymbolsUniq.index(xx) for xx in atomsSymbols]
colorVectors = [[atomsSymbolsUniq.index(xx), 0, 0] for xx in atomsSymbols]

mlab.figure(1, bgcolor=(0, 0, 0), size=(800, 800))
mlab.clf()

t1 = time.time()

# Plot the atoms
# for ii in range(nions):
#     atom = mlab.points3d([px[ii]], [py[ii]], [pz[ii]],
#                          [atomsSize[ii]],
#                          color=tuple(atomsColor[ii]),
#                          resolution=60,
#                          scale_factor=1.0)

for itype in range(ntype):
    iname = atomsSymbolsUniq[itype]
    atomsID = np.arange(nions, dtype=int)[np.array(atomsSymbols) == iname]
    iatoms = mlab.points3d(
                 px[atomsID], py[atomsID], pz[atomsID],
                 color=tuple(EleColors[EleName.index(iname)]),
                 resolution=60,
                 scale_factor=1.0,
            )

t2 = time.time()

# atoms = mlab.points3d(px, py, pz, atomsSize, resolution=60, scale_factor=1.0)
# atoms.glyph.color_mode = 'color_by_vector'
# # atoms.mlab_source.dataset.point_data.scalars = colorScalars
# atoms.mlab_source.dataset.point_data.vectors = colorVectors
# # # # atoms.mlab_source.dataset.point_data.scalars = atomsSize
#
# lut_atomsColor = np.ones((ntype, 4), dtype=int) * 255
# lut_atomsColor[:,:3] = np.array(atomsLUT * 255, dtype=int)
# atoms.module_manager.scalar_lut_manager.lut.table = lut_atomsColor
# # print colorScalars, lut_atomsColor

t3 = time.time()

# plot the bonds
ijs = []
for ii in range(nions):
    for jj in range(ii):
        e_i = atomsSymbols[ii]
        e_j = atomsSymbols[jj]

        i_i = EleName.index(e_i)
        i_j = EleName.index(e_j)

        D = poscar.get_distance(ii, jj)
        if D < maxBondLength[i_i, i_j]:
            # print('kaka')
            ijs.append((ii, jj))

            mx = (px[ii] + px[jj]) / 2.
            my = (py[ii] + py[jj]) / 2.
            mz = (pz[ii] + pz[jj]) / 2.

            c_i = atomsColor[ii]
            c_j = atomsColor[jj]

            mlab.plot3d([px[ii], mx], [py[ii], my], [pz[ii], mz],
                        tube_radius=0.1,
                        color=tuple(c_i),
                        )
            mlab.plot3d([px[jj], mx], [py[jj], my], [pz[jj], mz],
                        tube_radius=0.1,
                        color=tuple(c_j),
                        )

t4 = time.time()

print(t2 - t1, t3 - t2, t4 - t3)

mlab.orientation_axes()
# mlab.outline()

# mlab.outline(
#     # atoms,
#     # [cell[:,0].min(), cell[:,0].max(),
#     #  cell[:,1].min(), cell[:,1].max(),
#     #  cell[:,2].min(), cell[:,2].max()]
# )

# mlab.view(132, 54, 45, [21, 20, 21.5])
# mlab.view()

# mlab.show()
