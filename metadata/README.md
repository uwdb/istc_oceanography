See also the full sensor data (50MB, 20MB) `GA02_CTD_Sensor_Data.txt` and `GA03_CTD_Sensor_Data.txt` on TX-E1.

The `cruise_reports` are downloaded.

### Mapping genetic DNA sequence dataset #s to the sensor metadata
Overview: 
For each station on each cruise, 
the oceanographers collected environmental metadata at a variety of depths.
The oceanographers also collected genetic samples at 1 to 10 different depths.

For example, at cruise GA02 station 1, 
we have environmental metadata at 48 depth measurements ranging from 10.1 dbar to 2344.9 dbar,
and we have two genomic samples with identifier 209 and 210 at depths 10 dbar and 50 dbar.
We can obtain estimates for the exact depths (and temperature, salinity, NITRIT, etc.)
by interpolating the environmental measurements to 10 and 50 dbar.

The file `geotraces_conversion_bystation.tsv` contains the mapping. 
However, the file is incomplete. 
We only have mappings to 242 samples, even though we have 397 (overlapped) samples available.
These include 45 stations. (Each station has multiple samples.)
The file `valid_stations.csv` contains a list of all stations on each cruise that we have a metadata link for.

The file `valid_samples_GA02_filenames.csv` (and GA03) contains a list of all genomic sampleID filenames that we have a metadata link for AND that we have sample data for (~10 samples we do not have files for).

The main environmental metadata file is `GA02_IDP2014_v2_Discrete_Sample_Data.xlsx` (also included the same file in .csv format).
You can join the mapping file to the metadata file on the `Station` column.
Do the interpolation on the depth column `CTDPRS [dbar]`.

Additional info from Vijay:

	The incompleteness in the mapping file is because they only gave us the data for sample in which we have 
	the full chemistry available from the GEOTRACES cruise. All of the other genomic libraries came from 
	either other Geotraces samples for which the chemists have not yet released the data, or from the Hawaii 
	and Bermuda timeseries stations, which provide some other metadata but not as extensive as Geotraces.

	They can probably give us some basic information about these other samples if you would like.

	You are correct about matching the station columns. A station is a unique location in the ocean where a 
	particular boat stopped to take samples. At any given station, 
	there may be many bottles of water which each have a unique code.


