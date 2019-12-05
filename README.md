# Augur

branch | status
   --- | ---
master | [![Build Status](https://travis-ci.org/chaoss/augur.svg?branch=master)](https://travis-ci.org/chaoss/augur)

[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/2788/badge)](https://bestpractices.coreinfrastructure.org/projects/2788)

## About Augur

Augur is focused on prototyping open source software metrics.

Functionally, Augur is a prototyped implementation of the Linux Foundation's [CHAOSS Project](http://chaoss.community) on [open source software metrics](https://github.com/chaoss/metrics). Technically, Augur is a [Flask web application](http://augur.osshealth.io), [Python library](https://oss-augur.readthedocs.io/en/dev/library-documentation/python.html) and [REST server](http://augur.osshealth.io/static/api_docs/) that presents metrics on open source software development project health and sustainability.

## Getting Started

**Please follow the 'Getting Started' guide in our [documentation](https://oss-augur.readthedocs.io/en/master/getting-started/getting-started-toc.html).**

Note: we currently only support (most) UNIX systems. If you would like to use Augur but only have access to a non-Unix system, we recommend setting up an Ubuntu 18.04 VM if you can. 
If this is not feasible for you, please reach out to us at [p9j0r6s0m4a0t8v5@augurlabs.slack.com](mailto:p9j0r6s0m4a0t8v5@augurlabs.slack.com) and we will try to help you come up with a solution. In the meantime, if you have Windows and feel so inclined check out issue [#403](https://github.com/chaoss/augur/issues/403) as a starting point until we can finalize a Windows installation.

## Group 11 - Final Project

For our project, we created three new API endpoints: [contributor-affiliation](http://129.114.16.76:5000/api/unstable/repo-groups/20/contributor-affiliation), [committer-data](http://129.114.16.76:5000/api/unstable/repo-groups/20/committer-data), and [testing-coverage](http://129.114.16.76:5000/api/unstable/repo-groups/20/testing-data).  We also created a website to view these new metrics, at http://129.114.16.76:8080/home.html .

### Installation 
1. Clone this repository into a local directory using `git clone https://github.com/computationalmystic/sengfs19-group11.git`
2. Follow the 'Getting Started' guide in the Augur [documentation](https://oss-augur.readthedocs.io/en/master/getting-started/getting-started-toc.html) to set up out Augur version, stopping before `make install`.
3. Ensure your virtual environment has been activated and uses python 3.
4. Run `pip uninstall gunicorn`, then run `pip install gunicorn==19.9.0`.
5. Run `make install`, opting to install the database schema, load the sample data, and not install front-end dependencies.
6. Using the database created following Augur's installation guide, enter into the database using `psql`, and add new data into the database using the commands `insert into augur_data.repo_test_coverage(repo_id, file_subroutines_tested, file_subroutine_count, file_statements_tested, file_statement_count) values (25430, 124, 154, 254, 304)` and `insert into augur_data.repo_test_coverage(repo_id, file_subroutines_tested, file_subroutine_count, file_statements_tested, file_statement_count) values (25432, 354, 354, 463, 602)`
7. Run `make install` again
8. To start the API server, run `augur run --no-enable-housekeeper`

You may now access your API endpoints on your localhost at port 5000, for instance using http://localhost:5000/api/unstable/repo-groups/20/committer-data 

1. In a separate terminal windown, naviage into /sengfs19-group11/website
2. Ensure your virtual environment is activated.
3. run `python3 server.py`

You may now access your website at http://localhost:8080/home.html

### Changed/Added Files
1. created `/website` directory and all contained files 
2. changed `commit.py`, `routes.py`, `test_commit_functions.py`, and `test_commit_routes.py` in `/augur/metrics/commit` directory
3. changed `contributor.py`, `routes.py`, `test_contributor_functions.py`, and `test_contributor_routes.py` in `/augur/metrics/contributor` directory
4. changed `insight.py`, `routes.py`, `test_insight_functions.py`, and `test_insight_routes.py` in `/augur/metrics/insight` directory
5. created `sprint-1`, `sprint-2`, `sprint-3`, and `sprint-4`directories containing all class materials
6. created `Group 11 Design Doc.pdf`

## License, Copyright, and Funding
----------------

Copyright © 2019 University of Nebraska at Omaha, University of Missouri and CHAOSS Project at the Linux Foundation

Augur is free software: you can redistribute it and/or modify it under the terms of the MIT License as published by the Open Source Initiative. See the [LICENSE](LICENSE) file for more details.

This work has been funded through the Alfred P. Sloan Foundation.
