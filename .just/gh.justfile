# GitHub CLI (gh) commands
# https://cli.github.com/manual/


# show repository info
[group: 'gh']
gh-repo-view:
    gh repo view


# list pull requests
[group: 'gh']
gh-pr-list limit="10":
    gh pr list --limit {{limit}}


# list all pull requests (including closed)
[group: 'gh']
gh-pr-list-all limit="10":
    gh pr list --state all --limit {{limit}}


# view specific pull request
[group: 'gh']
gh-pr-view pr_number:
    gh pr view {{pr_number}}


# create a new pull request
[group: 'gh']
gh-pr-create:
    gh pr create


# checkout a pull request locally
[group: 'gh']
gh-pr-checkout pr_number:
    gh pr checkout {{pr_number}}


# list issues
[group: 'gh']
gh-issue-list limit="10":
    gh issue list --limit {{limit}}


# view specific issue
[group: 'gh']
gh-issue-view issue_number:
    gh issue view {{issue_number}}


# create a new issue
[group: 'gh']
gh-issue-create:
    gh issue create


# list workflow runs
[group: 'gh']
gh-run-list limit="10":
    gh run list --limit {{limit}}


# list runs for specific workflow
[group: 'gh']
gh-run-list-workflow workflow limit="10":
    gh run list --workflow "{{workflow}}" --limit {{limit}}


# view specific workflow run
[group: 'gh']
gh-run-view run_id:
    gh run view {{run_id}}


# watch a workflow run in real-time
[group: 'gh']
gh-run-watch run_id:
    gh run watch {{run_id}}


# list GitHub Actions caches
[group: 'gh']
gh-cache-list limit="20":
    gh cache list --limit {{limit}}


# delete a specific cache
[group: 'gh']
gh-cache-delete cache_id:
    gh cache delete {{cache_id}}


# delete all caches (requires confirmation)
[group: 'gh']
gh-cache-delete-all:
    gh cache delete --all


# list workflow files
[group: 'gh']
gh-workflow-list:
    gh workflow list


# view workflow file
[group: 'gh']
gh-workflow-view workflow:
    gh workflow view "{{workflow}}"


# enable a workflow
[group: 'gh']
gh-workflow-enable workflow:
    gh workflow enable "{{workflow}}"


# disable a workflow
[group: 'gh']
gh-workflow-disable workflow:
    gh workflow disable "{{workflow}}"


# trigger a workflow manually (workflow_dispatch)
[group: 'gh']
gh-workflow-run workflow:
    gh workflow run "{{workflow}}"


# list releases
[group: 'gh']
gh-release-list limit="10":
    gh release list --limit {{limit}}


# view latest release
[group: 'gh']
gh-release-view-latest:
    gh release view --latest


# create a new release
[group: 'gh']
gh-release-create tag:
    gh release create {{tag}}


# list repository secrets
[group: 'gh']
gh-secret-list:
    gh secret list


# set a repository secret
[group: 'gh']
gh-secret-set name value:
    echo "{{value}}" | gh secret set {{name}}


# delete a repository secret
[group: 'gh']
gh-secret-delete name:
    gh secret delete {{name}}


# view repository status (checks, deployments, etc)
[group: 'gh']
gh-status:
    gh status


# list repository collaborators
[group: 'gh']
gh-api-collaborators:
    gh api repos/{owner}/{repo}/collaborators


# view rate limit status
[group: 'gh']
gh-api-rate-limit:
    gh api rate_limit


# clone repository
[group: 'gh']
gh-repo-clone repo:
    gh repo clone {{repo}}


# fork repository
[group: 'gh']
gh-repo-fork:
    gh repo fork


# sync fork with upstream
[group: 'gh']
gh-repo-sync:
    gh repo sync


# browse repository in browser
[group: 'gh']
gh-browse:
    gh browse


# browse pull requests in browser
[group: 'gh']
gh-browse-pr:
    gh browse --pulls


# browse issues in browser
[group: 'gh']
gh-browse-issues:
    gh browse --issues


# browse actions in browser
[group: 'gh']
gh-browse-actions:
    gh browse --actions


# browse wiki in browser
[group: 'gh']
gh-browse-wiki:
    gh browse --wiki


# list dependabot PRs
[group: 'gh']
gh-pr-list-dependabot limit="10":
    gh pr list --author app/dependabot --limit {{limit}}


# list all dependabot PRs (including closed)
[group: 'gh']
gh-pr-list-dependabot-all limit="20":
    gh pr list --state all --author app/dependabot --limit {{limit}}


# view GitHub Actions usage (billing)
[group: 'gh']
gh-api-actions-usage:
    gh api repos/{owner}/{repo}/actions/billing/usage
