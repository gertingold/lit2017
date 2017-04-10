from pyx import canvas, color, graph, path, style, text, unit

def frontplane(xoff, yoff, z, nxmax, mymax, facecolor, edgecolor, trans):
    p = path.path(path.moveto(*projector(xoff, z, yoff)),
                  path.lineto(*projector(xoff+nxmax, z, yoff)),
                  path.lineto(*projector(xoff+nxmax, z, yoff+nymax)),
                  path.lineto(*projector(xoff, z, yoff+nymax)),
                  path.closepath())
    c.fill(p, [facecolor, color.transparency(trans)])
    c.stroke(p, [edgecolor])
    for nx in range(1, nxmax):
        x0, y0 = projector(xoff+nx, z, yoff)
        x1, y1 = projector(xoff+nx, z, yoff+nymax)
        c.stroke(path.line(x0, y0, x1, y1), [edgecolor])
    for ny in range(1, nymax):
        x0, y0 = projector(xoff, z, yoff+ny)
        x1, y1 = projector(xoff+nxmax, z, yoff+ny)
        c.stroke(path.line(x0, y0, x1, y1), [edgecolor])

def corner(nx, ny, z, facecolor, edgecolor, trans, xdir, ydir):
    if xdir:
        p = path.path(path.moveto(*projector(nx, z, ny)),
                      path.lineto(*projector(nx-1, z, ny)),
                      path.lineto(*projector(nx-1, z+1, ny)),
                      path.lineto(*projector(nx, z+1, ny)),
                      path.closepath())
        c.fill(p, [facecolor, color.transparency(trans)])
    if ydir:
        p = path.path(path.moveto(*projector(nx, z, ny)),
                      path.lineto(*projector(nx, z, ny+1)),
                      path.lineto(*projector(nx, z+1, ny+1)),
                      path.lineto(*projector(nx, z+1, ny)),
                      path.closepath())
        c.fill(p, [facecolor, color.transparency(trans)])
    x0, y0 = projector(nx, z, ny)
    x1, y1 = projector(nx, z+1, ny)
    c.stroke(path.line(x0, y0, x1, y1), [edgecolor])

projector = graph.graphxyz.central(60, -60, 25).point

unit.set(wscale=1.5, xscale=1.7)
text.set(text.LatexRunner, texenc='utf8')
text.preamble(r'''\usepackage[utf8x]{inputenc}
                  \usepackage{qswiss}''')
c = canvas.canvas()
nxmax = 7
nymax = 5
trans = 0.4

xoff = 5
yoff = 1
edgecolors = (color.rgb(0, 0, 0.8),
              color.rgb(0, 0.6, 0),
              color.rgb(0.8, 0, 0))
w = 0.3
facecolors = (color.rgb(w, w, 1),
              color.rgb(w, 1, w),
              color.rgb(1, w, w))
for nplane, (edgecolor, facecolor) in enumerate(zip(edgecolors, facecolors)):
    zoff = 1.04*(2-nplane)
    frontplane(xoff, yoff, zoff+1, nxmax, nymax, facecolor, edgecolor, trans)
    for nx in range(nxmax, -1, -1):
        for ny in range(nymax+1):
            corner(xoff+nx, yoff+ny, zoff, facecolor, edgecolor, trans,
                   nx != 0, ny != nymax)
    frontplane(xoff, yoff, zoff, nxmax, nymax, facecolor, edgecolor, trans)
x0, _ = projector(xoff+0.5*nxmax, 0, yoff)
y0 = -2.4
c.text(x0, y0, r"\sffamily Farbbild (RGB-Format)", [text.halign.center, text.valign.top])
c.text(x0, y0-0.7, r"\sffamily N$\times$M$\times$3-Array", [text.halign.center, text.valign.top])

xoff = -4
yoff = 0
edgecolor = color.grey(0)
w = 0.3
facecolor = color.grey(0.7)
nplane = 2
zoff = 1.04*(2-nplane)-2
frontplane(xoff, yoff, zoff+1, nxmax, nymax, facecolor, edgecolor, trans)
for nx in range(nxmax, -1, -1):
    for ny in range(nymax+1):
        corner(xoff+nx, yoff+ny, zoff, facecolor, edgecolor, trans,
               nx != 0, ny != nymax)
frontplane(xoff, yoff, zoff, nxmax, nymax, facecolor, edgecolor, trans)
x0, _ = projector(xoff+0.5*nxmax, zoff, yoff)
y0 = -2.4
c.text(x0, y0, r"\sffamily Schwarz-Weiß-Bild", [text.halign.center, text.valign.top])
c.text(x0, y0-0.7, r"\sffamily N$\times$M-Array", [text.halign.center, text.valign.top])
c.writePDFfile()
