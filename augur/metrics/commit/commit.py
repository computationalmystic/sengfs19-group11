"""
Metrics that provide data about commits & their associated activity
"""

import inspect
import sys
import types
import datetime
import sqlalchemy as s
import pandas as pd
import requests
import json
from augur.util import logger, annotate, add_metrics

@annotate(tag='committers')
def committers(self, repo_group_id, repo_id=None, begin_date=None, end_date=None, period='week'):
    if not begin_date:
        begin_date = '1970-1-1 00:00:01'
    if not end_date:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    committersSQL = None

    if repo_id:
        committersSQL = s.sql.text(
            """
                SELECT
                    date_trunc(:period, commits.cmt_author_date::date) as date,
                    repo_name,
                    rg_name,
                    count(cmt_author_name)
                FROM
                    commits, repo, repo_groups
                WHERE
                    commits.repo_id = :repo_id AND commits.repo_id = repo.repo_id
                    AND repo.repo_group_id = repo_groups.repo_group_id
                    AND commits.cmt_author_date BETWEEN :begin_date and :end_date
                GROUP BY date, repo_name, rg_name
                ORDER BY date DESC
            """
        )
    else:
        committersSQL = s.sql.text(
            """
            SELECT
                date_trunc(:period, commits.cmt_author_date::date) as date,
                rg_name,
                count(cmt_author_name)
            FROM
                commits, repo, repo_groups
            WHERE
                repo.repo_group_id = repo_groups.repo_group_id AND repo.repo_group_id = :repo_group_id
                AND repo.repo_id = commits.repo_id
                AND commits.cmt_author_date BETWEEN :begin_date and :end_date
            GROUP BY date, rg_name
            """
        )

    results = pd.read_sql(committersSQL, self.database, params={'repo_id': repo_id, 'repo_group_id': repo_group_id,'begin_date': begin_date, 'end_date': end_date, 'period':period})

    return results

@annotate(tag='annual-commit-count-ranked-by-new-repo-in-repo-group')
def annual_commit_count_ranked_by_new_repo_in_repo_group(self, repo_group_id, repo_id = None, calendar_year=None):
    """
    For each repository in a collection of repositories being managed, each REPO that first appears in the parameterized
    calendar year (a new repo in that year), show all commits for that year (total for year by repo).
    Result ranked from highest number of commits to lowest by default.

    :param repo_url: the repository's URL
    :param calendar_year: the calendar year a repo is created in to be considered "new"
    :param repo_group: the group of repositories to analyze
    """
    if calendar_year == None:
        calendar_year = 2019

    cdRgNewrepRankedCommitsSQL = None

    if not repo_id:
        cdRgNewrepRankedCommitsSQL = s.sql.text("""
            SELECT repo.repo_id, sum(cast(added as INTEGER) - cast(removed as INTEGER) - cast(whitespace as INTEGER)) as net, patches, repo_name
            FROM dm_repo_annual, repo, repo_groups
            where  repo.repo_group_id = :repo_group_id
            and dm_repo_annual.repo_id = repo.repo_id
            and date_part('year', repo.repo_added) = :calendar_year
            and repo.repo_group_id = repo_groups.repo_group_id
            group by repo.repo_id, patches, rg_name
            ORDER BY net desc
            LIMIT 10
        """)
    else:
        cdRgNewrepRankedCommitsSQL = s.sql.text("""
            SELECT repo.repo_id, sum(cast(added as INTEGER) - cast(removed as INTEGER) - cast(whitespace as INTEGER)) as net, patches, repo_name
            FROM dm_repo_annual, repo, repo_groups
            where  repo.repo_group_id = (select repo.repo_group_id from repo where repo.repo_id = :repo_id)
            and dm_repo_annual.repo_id = repo.repo_id
            and date_part('year', repo.repo_added) = :calendar_year
            and repo.repo_group_id = repo_groups.repo_group_id
            group by repo.repo_id, patches, rg_name
            ORDER BY net desc
            LIMIT 10
        """)
    results = pd.read_sql(cdRgNewrepRankedCommitsSQL, self.database, params={ "repo_group_id": repo_group_id,
    "repo_id": repo_id, "calendar_year": calendar_year})
    return results

@annotate(tag='annual-commit-count-ranked-by-repo-in-repo-group')
def annual_commit_count_ranked_by_repo_in_repo_group(self, repo_group_id, repo_id=None, timeframe=None):
    """
    For each repository in a collection of repositories being managed, each REPO's total commits during the current Month,
    Year or Week. Result ranked from highest number of commits to lowest by default.
    :param repo_group_id: The repository's repo_group_id
    :param repo_id: The repository's repo_id, defaults to None
    :param timeframe: all, year, or month for the episodic summary timeframe. 
    """
    if timeframe == None:
        timeframe = 'all'

    cdRgTpRankedCommitsSQL = None

    if repo_id:
        if timeframe == 'all':
            cdRgTpRankedCommitsSQL = s.sql.text("""
                SELECT repo.repo_id, repo_name as name, SUM(added - removed - whitespace) as net, patches
                FROM dm_repo_annual, repo, repo_groups
                WHERE repo.repo_group_id = (select repo.repo_group_id from repo where repo.repo_id = :repo_id)
                AND repo.repo_group_id = repo_groups.repo_group_id
                AND dm_repo_annual.repo_id = repo.repo_id
                group by repo.repo_id, patches
                order by net desc
                LIMIT 10
            """)
        elif timeframe == 'year':
            cdRgTpRankedCommitsSQL = s.sql.text("""
                SELECT repo.repo_id, repo_name as name, SUM(added - removed - whitespace) as net, patches
                FROM dm_repo_annual, repo, repo_groups
                WHERE repo.repo_group_id = (select repo.repo_group_id from repo where repo.repo_id = :repo_id)
                AND repo.repo_group_id = repo_groups.repo_group_id
                AND dm_repo_annual.repo_id = repo.repo_id
                AND date_part('year', repo_added) = date_part('year', CURRENT_DATE)
                group by repo.repo_id, patches
                order by net desc
                LIMIT 10
            """)
        elif timeframe == 'month':
            cdRgTpRankedCommitsSQL = s.sql.text("""
                SELECT repo.repo_id, repo_name as name, SUM(added - removed - whitespace) as net, patches
                FROM dm_repo_monthly, repo, repo_groups
                WHERE repo.repo_group_id = (select repo.repo_group_id from repo where repo.repo_id = :repo_id)
                AND repo.repo_group_id = repo_groups.repo_group_id
                AND dm_repo_monthly.repo_id = repo.repo_id
                AND date_part('year', repo_added) = date_part('year', CURRENT_DATE)
                AND date_part('month', repo_added) = date_part('month', CURRENT_DATE)
                group by repo.repo_id, patches
                order by net desc
                LIMIT 10
            """)
    else:
        if timeframe == 'all':
            cdRgTpRankedCommitsSQL = s.sql.text("""
                SELECT repo.repo_id, repo_name as name, SUM(added - removed - whitespace) as net, patches
                FROM dm_repo_annual, repo, repo_groups
                WHERE repo.repo_group_id = :repo_group_id
                AND repo.repo_group_id = repo_groups.repo_group_id
                AND dm_repo_annual.repo_id = repo.repo_id
                group by repo.repo_id, patches
                order by net desc
                LIMIT 10
            """)
        elif timeframe == "year":
            cdRgTpRankedCommitsSQL = s.sql.text(
                """
                SELECT repo.repo_id, repo_name as name, SUM(added - removed - whitespace) as net, patches
                FROM dm_repo_annual, repo, repo_groups
                WHERE repo.repo_group_id = :repo_group_id
                AND repo.repo_group_id = repo_groups.repo_group_id
                AND dm_repo_annual.repo_id = repo.repo_id
                AND date_part('year', repo_added) = date_part('year', CURRENT_DATE)
                group by repo.repo_id, patches
                order by net desc
                LIMIT 10
                """
            )
        elif timeframe == 'month':
            cdRgTpRankedCommitsSQL = s.sql.text("""
                SELECT repo.repo_id, repo_name as name, SUM(added - removed - whitespace) as net, patches
                FROM dm_repo_annual, repo, repo_groups
                WHERE repo.repo_group_id = :repo_group_id
                AND repo.repo_group_id = repo_groups.repo_group_id
                AND dm_repo_annual.repo_id = repo.repo_id
                AND date_part('year', repo_added) = date_part('year', CURRENT_DATE)
                AND date_part('month', repo_added) = date_part('month', CURRENT_DATE)
                group by repo.repo_id, patches
                order by net desc
                LIMIT 10
            """)


    results = pd.read_sql(cdRgTpRankedCommitsSQL, self.database, params={ "repo_group_id": repo_group_id,
    "repo_id": repo_id})
    return results


@annotate(tag='committer-data')
def committer_data(self, repo_group_id, repo_id=None, period='all', begin_date=None, end_date=None):
    """
    Returns a timeseries of all the contributions to a project.

    DataFrame has these columns:
    date
    commits

    :param repo_id: The repository's id
    :param repo_group_id: The repository's group id
  -----  :param period: To set the periodicity to 'all', day', 'week', 'month' or 'year', defaults to 'all'
  -----  :param begin_date: Specifies the begin date, defaults to '1970-1-1 00:00:00'
  -----  :param end_date: Specifies the end date, defaults to datetime.now()
    :return: DataFrame of persons/period
    """

    if not begin_date:
        begin_date = '1970-1-1 00:00:01'
    if not end_date:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if repo_id:
        contributorsSQL = s.sql.text("""
            SELECT 
	            DISTINCT cmt_author_name,
	            cmt_author_affiliation,
                repo_id
            FROM
                augur_data.commits
            WHERE
                repo_id = :repo_id
        """)

        results = pd.read_sql(contributorsSQL, self.database, params={'repo_id': repo_id, 'period': period,
                                                                'begin_date': begin_date, 'end_date': end_date})
    else:
        contributorsSQL = s.sql.text("""
            SELECT 
	            DISTINCT cmt_author_name,
	            cmt_author_affiliation,
                repo_id
            FROM
                augur_data.commits
            WHERE repo_id in (SELECT repo_id
                            FROM augur_data.repo
                            WHERE repo_group_id = :repo_group_id)
        """)

        results = pd.read_sql(contributorsSQL, self.database, params={'repo_group_id': repo_group_id, 'period': period,
                                                                'begin_date': begin_date, 'end_date': end_date})
    
    headers = {
        'X-API-KEY': 'a978daf0d0bae32c8377c1613db4a22b'
    }
    genderURL = "https://v2.namsor.com/NamSorAPIv2/api2/json/genderFull/"
    ethURL = "https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicity/"
    gender = []
    genderProb = []
    eth = []
    ethProb = []

    for _, row in results.iterrows():
        name = row['cmt_author_name']
        dividedName = name.split(" ")

        if len(dividedName) == 2:
            r = requests.get(genderURL + name, headers=headers)
            rjson = r.json()
            gender.append(rjson['likelyGender'])
            genderProb.append(rjson['genderScale'])

            r = requests.get(ethURL + dividedName[0] + "/" + dividedName[1], headers=headers)
            rjson = r.json()
            eth.append(rjson['raceEthnicity'])
            ethProb.append(rjson['probabilityCalibrated'])

        else:
            gender.append('null')
            genderProb.append(0)
            eth.append('null')
            ethProb.append(0)

    results['gender'] = gender
    results['genderProb'] = genderProb
    results['eth'] = eth
    results['ethProb'] = ethProb
        
    return results

def create_commit_metrics(metrics):
    add_metrics(metrics, __name__)
