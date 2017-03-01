# netlify_deployer
A script to deploy a whoe directory to Netlify using their incremental deploy API.

Usage:  
`netlify_deployer.py branch_name netlify_site_id directory_to_deploy`

The branch name is being used to determine if the deployment is a preview one `branch_name != 'master'` or should the site be published (when on `master`).

PRs welcome - please see the list of issues for the things to pick up.

