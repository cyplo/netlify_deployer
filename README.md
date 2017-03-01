# netlify_deployer
A script to deploy a whole directory to Netlify using their incremental deploy API.

Commandline usage:
* Set `NETLIFY_TOKEN` environment variable to your token
* `netlify_deployer.py branch_name netlify_site_id directory_to_deploy`


The branch name is being used to determine if the deployment is a preview one `branch_name != 'master'` or should the site be published - (when on `master`) - [see this issue](https://github.com/cyplo/netlify_deployer/issues/1) for a starting point to make it more explicit.

PRs welcome - please see the list of issues for the things to pick up.

