from qgis import processing


def simplifyPolyg(infile, outfile, threshold=0.2):
    processing.run("native:simplifygeometries", \
        {'INPUT':infile, \
        'METHOD':0, \
        'TOLERANCE':threshold, \
        'OUTPUT':outfile})


if __name__ == "__main__":
    infile = r"C:\Users\Geoyee\Desktop\dd\shp.shp"
    outfile = r"C:\Users\Geoyee\Desktop\dd\shp_simp.shp"
    simplifyPolyg(infile, outfile)