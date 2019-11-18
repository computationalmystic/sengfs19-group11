from flask import Response

matthew
def create_experimental_routes(server):
	metrics = server._augur.metrics
	
	"""
	API Documentation

	@api {get} /repo/repo_id/testing-coverage Testing Coverage (Repo)
	@apiName testing-coverage-repo
	@apiGroup Risk
	@apiDescription Determine how much code has been tested for a repo 
	 	<a href="https://github.com/chaoss/wg-risk/blob/master/metrics/Test_Coverage.md">CHAOSS Metric Definition</a>
	@apiParam {string} repo_group_id Repository Group ID
	@apiParam {string} [begin_date="1970-1-1 0:0:0"] Beginning date specification. E.g. values: `2018`, `2018-05`, `2019-05-01`
	@apiParam {string} [end_date="current date"] Ending date specification. E.g. values: `2018`, `2018-05`, `2019-05-01`
	@apiSuccessExample {json} Success-Response:
		[
			{

	"""



master
