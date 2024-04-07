# loading Libaries
import openeo
from tqdm import tqdm

# defining functions to handle Months lengths considering leap years
def is_leap_year(year):
    """Returns True if the given year is a leap year, False otherwise."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_month_lengths(year):
    """Returns a dictionary with the months as zero-padded strings and the number of days as values, adjusted for leap years."""
    return {
        "01": 31,
        "02": 29 if is_leap_year(year) else 28,
        "03": 31,
        "04": 30,
        "05": 31,
        "06": 30,
        "07": 31,
        "08": 31,
        "09": 30,
        "10": 31,
        "11": 30,
        "12": 31
    }

# connecting to the openEO backend
connection = openeo.connect('openeo.dataspace.copernicus.eu')
connection.describe_collection('SENTINEL2_L2A')
connection.authenticate_oidc()

# defining the spatial and temporal extent
years = [str(y) for y in range(2017, 2024)] # end year not included
months = [str(y).zfill(2) for y in range(6, 9)] # end month not included
west = 8.3
south = 47.53
east = 8.9
north = 47.84

# starting Tasks year by year
for year in tqdm(years, desc='Downloading data'):
    month_lengths_list = get_month_lengths(int(year))
    for month in tqdm(months, desc='Downloading data'):
        month_length = month_lengths_list[month]
        datacube = connection.load_collection(
            'SENTINEL2_L2A',
            spatial_extent={
                'west': west, 
                'south': south, 
                'east': east, 
                'north': north,
                'crs': 'EPSG:4326'},
            temporal_extent=[f'{year}-{month}-01', f'{year}-{month}-{month_length}'],
            bands=['B04', 'B08', 'SCL'],
            max_cloud_cover=85,
        )

        # selecting individual bands from the data cube and rescaling the digital number values to physical reflectances
        red = datacube.band('B04') * 0.0001
        nir = datacube.band('B08') * 0.0001

        # computing NDVI
        evi_cube = (nir - red) / (nir + red)

        # selecting the 'SCL' band from the data cube and building a mask to mask out everything but class 4 (vegetation)
        scl_band = datacube.band('SCL')
        mask = (scl_band != 4)

        # Resample the EVI cube to the spatial resolution of the mask (SCL band has a resolution of 20m, B04 and B08 have a resolution of 10m)
        evi_cube_resampled = evi_cube.resample_cube_spatial(mask)

        # Apply the mask to the `evi_cube` cutting all pixels that are not vegetation including the pixels with clouds
        evi_cube_masked = evi_cube_resampled.mask(mask)

        # Download the reprojected data cube
        evi_cube_masked.download(f'data/NDVI_test/ndvi_sh_{year}{month}.nc')
