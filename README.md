# EdX Analysis

Many courses running on the [edx platform](https://www.edx.org/course) have their student learning data processed using the code [edx2bigquery](https://github.com/mitodl/edx2bigquery), and stored in [Google Bigquery](https://bigquery.cloud.google.com/). This repository is a demonstration of how the data stored in BigQuery could be presented on an interactive dashboard that could allow instructors and researchers to visualize and analyze student learning data.

## Getting Started

If you just want to play with the demo, go to [http://198.199.87.145/demo](http://198.199.87.145/demo).

If you are cloning/downloading the repository to build on top of it, we strongly recommend using a virutalenv. Follow the usual procedure to install the requirements, and then run the code by issuing the command "python run.py". Once the program is running, open a tab in your browser and type http://localhost:8050/ to access the dashboard.


## Notes

0. This code is not suitable for touchscreen devices, according to our tests.

1. The code is NOT production-grade, and not intended to be used directly with the BigQuery data to interpret student learning. We are working on the code. Email [anindyar@mit.edu](mailto:anindyar@mit.edu) if you'd like to be notified about the "new and improved" versions.

2. The sample dataset included here is representative but fake.

3. An earlier version of this demo (along with other useful jupyter notebooks) is available from [Vita Lampietti's Github account](https://github.com/vlampietti/edx_analysis).

4. Best way to find out what different quantities mean is to look through the [edx2BigQuery](https://github.com/mitodl/edx2bigquery) repository. More information on edX tracking log definitions are available [here](http://edx.readthedocs.io/projects/devdata/en/latest/internal_data_formats/tracking_logs/').

## Built With

[Dash by Plotly](https://plot.ly/products/dash/)

## Questions/Comments?

Please email your comments/suggestions to [anindyar@mit.edu](mailto:anindyar@mit.edu)

