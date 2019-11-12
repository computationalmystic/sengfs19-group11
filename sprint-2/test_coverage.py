SELECT
	augur_data.repo_test_coverage.repo_id,
	augur_data.repo_test_coverage.file_subroutines_tested,
	augur_data.repo_test_coverage.file_subroutine_count,
	augur_data.repo_test_coverage.file_statements_tested,
	augur_data.repo_test_coverage.file_statement_count
FROM augur_data.repo_test_coverage JOIN augur_data.repo on repo_test_coverage.repo_id = repo.repo_id
GROUP BY augur_data.repo_test_coverage.repo_id

@annotate(tag=<testing-coverage>)
def <testing_coverage>(self, repo_group_id)
"""
<the metric analzyes how much a repository is tested>
:parameter repo_group_id: The repository’s group id
:return: Dataframe of <testing-coverage for a repository>
"""
<testing-coverage-SQL> = ‘ ‘
If not repo_id:
	<testing-coverage-SQL> = s.sql.text("""
		<repo_group form of the SQL query>
	""")
results = pd.read_sql(testing-coverage-SQL>, self.database, params = {‘repo_group_id’: repo_group_id})
# output the testing coverage as percentages, one for subroutines tested and one for statements tested
return results

Else:
	<testing-coverage-SQL> = s.sql.text("""
			<repo form of the SQL query>
SELECT
	augur_data.repo_test_coverage.repo_id,
	augur_data.repo_test_coverage.file_subroutines_tested,
	augur_data.repo_test_coverage.file_subroutine_count,
	augur_data.repo_test_coverage.file_statements_tested,
	augur_data.repo_test_coverage.file_statement_count
FROM augur_data.repo_test_coverage JOIN augur_data.repo on repo_test_coverage.repo_id = repo.repo_id
GROUP BY augur_data.repo_test_coverage.repo_id
	""")
	results = pd.read_sql(<testing-coverage-SQL>, self.database, params={‘repo_id’: repo_id})
	# same as above for outputting percentages
return results

@server.addRepoGroupMetric(metrics.testing-coverage, ‘testing-coverage’)

API Documentation
"""
@api {get} /repo/repo_id/testing-coverage Testing Coverage (Repo)
@apiName testing-coverage-repo
@apiGroup
"""

