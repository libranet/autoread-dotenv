# GitHub CLI commands
# docs: https://cli.github.com/manual/


# list open pull requests
[group: 'gh']
gh-pr-list:
    gh pr list --state open


# list all pull requests (open and closed)
[group: 'gh']
gh-pr-list-all:
    gh pr list --state all --limit 20


# view a specific pull request
[group: 'gh']
gh-pr-view pr:
    gh pr view {{ pr }}


# close a pull request with comment
[group: 'gh']
gh-pr-close pr comment="Closing PR":
    gh pr close {{ pr }} --comment "{{ comment }}"


# merge a pull request
[group: 'gh']
gh-pr-merge pr:
    gh pr merge {{ pr }}


# list recent workflow runs
[group: 'gh']
gh-run-list:
    gh run list --limit 10


# view a specific workflow run
[group: 'gh']
gh-run-view run:
    gh run view {{ run }}


# view failed logs for a workflow run
[group: 'gh']
gh-run-failed run:
    gh run view {{ run }} --log-failed


# watch a workflow run in progress
[group: 'gh']
gh-run-watch run:
    gh run watch {{ run }}


# list dependabot security alerts
[group: 'gh']
gh-alerts:
    gh api repos/:owner/:repo/dependabot/alerts --jq '.[] | select(.state == "open") | {number, severity: .security_advisory.severity, package: .security_vulnerability.package.name, summary: .security_advisory.summary}'


# list all dependabot alerts (open and fixed)
[group: 'gh']
gh-alerts-all:
    gh api repos/:owner/:repo/dependabot/alerts --jq '.[] | {number, state, severity: .security_advisory.severity, package: .security_vulnerability.package.name}'


# dismiss a dependabot alert
[group: 'gh']
gh-alert-dismiss alert reason="not_used":
    gh api --method PATCH repos/:owner/:repo/dependabot/alerts/{{ alert }} -f state=dismissed -f dismissed_reason={{ reason }}


# view repository info
[group: 'gh']
gh-repo-view:
    gh repo view


# open repository in browser
[group: 'gh']
gh-repo-browse:
    gh repo view --web


# open pull requests page in browser
[group: 'gh']
gh-pr-browse:
    gh pr list --web


# open actions page in browser
[group: 'gh']
gh-actions-browse:
    gh run list --web
