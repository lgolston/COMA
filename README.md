# COMA

Functions for:
- Calculating linear calibration equations based on low/high calibration cycles
- Exporting COMA data to ICARRT format
- Plotting flight data (with COMA and MMS files)
- Plotting flight data (using COMA and IWG1 files on MTS)
- Comparing COMA, ACOS, and COLD2
- Allan deviation plots from lab or flight data
- Comparing COMA against GEOS model
- Plotting raw spectra (similar to Colin script)
- Plotting baseline subtracted absorption

Dependencies
- cartopy (for mapping flight)
- openpyxl (for reading MadgeTech .xlsx file)
- hitran-api (HAPI, for spectral calculation)
