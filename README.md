# FermiData

- I downloaded all data files in a temporary directory with:

`wget -m -P . -nH --cut-dirs=4 -np -e robots=off https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/`

- donwloaded the spacecraft file from [here](https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/queries) with:

`wget https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/queries/L2102260113087E6D776947_SC00.fits`

- installed Miniconda following [here](https://docs.conda.io/en/latest/miniconda.html)

- installed the Fermi tools with (see also [here](https://github.com/fermi-lat/Fermitools-conda/wiki/Installation-Instructions))

`conda create -n fermi -c conda-forge -c fermi fermitools python=3`

- used the following commands to activate the environment:

```
source ~/.initconda.zsh
conda activate fermi
conda list fermi
```

- created the event list file:

`ls photon/lat_photon_weekly_w* > events.txt`

- combined the data files:

```
gtselect evclass=256 evtype=3 
Input FT1 file[] events.txt
Output FT1 file[] lat_alldata.fits
RA for new search center (degrees) (0:360) [INDEF] 0
Dec for new search center (degrees) (-90:90) [INDEF] 0
radius of new search region (degrees) (0:180) [INDEF] 180
start time (MET in s) (0:) [INDEF] INDEF
end time (MET in s) (0:) [INDEF] INDEF
lower energy limit (MeV) (0:) [] 30
upper energy limit (MeV) (0:) [] 300000
maximum zenith angle value (degrees) (0:180) [] 105
```

- ***See the suggested parameters [here](https://fermi.gsfc.nasa.gov/ssc/data/analysis/documentation/Cicerone/Cicerone_Data_Exploration/Data_preparation.html)*** ***for Diffuse Analysis the evclass should be 128!***

- Note that evtype=3 stands for FRONT+BACK event types

- selected from all events those which fall into periods where data quality is good:

```
gtmktime
Spacecraft data file[] L2102260113087E6D776947_SC00.fits
Filter expression[DATA_QUAL>0 && LAT_CONFIG==1 && ABS(ROCK_ANGLE)<52] 
Apply ROI-based zenith angle cut[yes] no
Event data file[] lat_alldata.fits
Output event file name[] myevents_fermi.fits
```

- and binned in log energy axis:

```
gtbin                                                                                                                                                                                                                                                         
This is gtbin version HEAD
Type of output file (CCUBE|CMAP|LC|PHA1|PHA2|HEALPIX) [] HEALPIX
Event data file name[] myevents_fermi.fits
Output file name[] myevents_fermi_healpix.fits
Spacecraft data file name[] L2102260113087E6D776947_SC00.fits
Ordering Scheme (RING|NESTED) [] NESTED
Order of the map (int between 0 and 12, included)[] 8
Coordinate system (CEL - celestial, GAL -galactic) (CEL|GAL) [] GAL
Region, leave empty for all-sky[] 
Do you want Energy binning ?[] yes
Algorithm for defining energy bins (FILE|LIN|LOG) [] LOG
Start value for first energy bin in MeV[] 100
Stop value for last energy bin in MeV[] 1000000
Number of logarithmically uniform energy bins[] 64
```

- calculated integrated livetime *whatever that means* as a function of sky position

```
gtltcube zmax = 105                                                                                                                                                                                                                                                            Event data file[] myevents_fermi.fits 
Spacecraft data file[] L2102260113087E6D776947_SC00.fits 
Output file[] myltcube.fits
Step size in cos(theta) (0.:1.) [0.025] 
Pixel size (degrees)[1]
Working on file L2102260113087E6D776947_SC00.fits
```

***Pixel size (degrees)[1] is this OK?***

- computed the binsize as: 

```
NSide = 2.**order
NPixels = 12. * nside * nside
PixelAreaRad = 4. * 3.14 / npixels # in rad^2
PixelAreaDeg = (180. / 3.14)**2. * PixelAreaRad # in deg^2
```

- generated the exposure map with `gtexpcube2`:

```
gtexpcube2 bincalc=CENTER, coordsys=GAL, binsz=0.23
Livetime cube file[] myltcube.fits
Counts map file[] myevents_fermi_healpix.fits
Output file name[] myexpcube.fits
```

***The energy axis must be the same as in gtbin***
***NBins 64 is too much?***
