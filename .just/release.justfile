# release


# check if the new docker-version specified in docker/.gitlab-ci.yml is ok to release
[group: 'release']
[unix]
check-package-version: git-tag-list-versions
    #!/usr/bin/env bash
    # set -euxo pipefail
    set -euo pipefail

    new_version=$(bin/toml get --toml-path pyproject.toml project.version)
    echo -e "\nNew release-version specified in pyproject.toml: $new_version"

    # Validate version-syntax
    if [[ ! $new_version =~ ^[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then
        echo "Invalid format. Please enter the version in x.y or x.y.z format."
        exit 1
    fi

    # Check if the new version already exists as a tag
    if git rev-parse "$new_version" >/dev/null 2>&1; then
        echo "Tag ${new_version} already exists!"
        exit 1
    fi

    # echo "new version would be: ${new_version}"


# release a new package: tag with the version in pyproject.toml + create a GitHub Release.
# Publishing to PyPI happens in .github/workflows/release.yaml, triggered by the GitHub Release
# (event `release: published`) that `gh release create` fires below.
[group: 'release']
[unix]
release: git-check-uncommitted-changes check-package-version
    #!/usr/bin/env bash
    # set -euxo pipefail
    set -euo pipefail

    # check if we are on main-branch
    current_branch=$(git branch --show-current)
    if [ "$current_branch" != "main" ]; then
        echo "You are not on the main branch."
        exit 1
    fi

    new_version=$(bin/toml get --toml-path pyproject.toml project.version)
    printf "\nOK to release ${new_version}? (y/n)\n"
    read answer

    if [ "$answer" != "${answer#[Yy]}" ] ;then
        echo "Tagging new version: ${new_version}"
        git push
        git tag ${new_version}
        git push --tags

        echo "Creating GitHub Release ${new_version}"
        gh release create "${new_version}" --title "${new_version}" --generate-notes
    else
        exit 0
    fi
