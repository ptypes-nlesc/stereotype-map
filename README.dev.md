# Developer documentation

Please read the [Contributing guidelines](CONTRIBUTING.md) first.

## Linting and formatting

Install a plugin on your editor to use [EditorConfig](https://editorconfig.org).
This will ensure that your editor is configured with important formatting settings.

Install [https://pre-commit.com](https://pre-commit.com) to run the linters and formatters. 

```bash
pipx install pre-commit
```

Then activate it as a pre-commit hook:

```bash
pre-commit install
```

To run the linting and formatting manually, enter the command below:

```bash
pre-commit run -a
```

**Please only commit if all the pre-commit tests pass**.

## First time clone (external collaborators only)

If this is the first time you work with this repository, follow the instructions below:

1. Fork this repository (skip this step if you are an internal collaborator)
2. Clone your repo (this will create a `git remote` called `origin`)
3. Add this repo as a remote:

   ```bash
   git remote add upstream https://github.com/ptypes-nlesc/data-profiling.git
   ```
This will ensure that you have two remotes in your git: `origin` and `upstream`. You will create branches and push to `origin`, and you will fetch and update your local `main` branch from `upstream`.

Internal collaborators don't need to fork the repository or add an `upstream` remote because they have direct access to the main repository. They can clone the repository directly, create branches, and push changes.

## Working on a new issue

1. Fetch from the remote and fast-forward your local main

   ```bash
   git fetch upstream
   git switch main
   git merge --ff-only upstream/main
   ```

2. Branch from `main` to address the issue (see below for naming)

   ```bash
   git switch -c 42-add-answer-universe
   ```

3. Push the new local branch to your personal remote repository

   ```bash
   git push -u origin 42-add-answer-universe
   ```

4. Create a pull request to merge your remote branch into the main.

### Branch naming

- If there is an associated issue, add the issue number.
- If there is no associated issue, **and the changes are small**, add a prefix such as "typo", "hotfix", "small-refactor", according to the type of update.
- If the changes are not small and there is no associated issue, then create the issue first, so we can properly discuss the changes.
- Use dash separated imperative wording related to the issue (e.g., `14-add-tests`, `15-fix-model`, `16-remove-obsolete-files`).

### Commit message

- Use imperative or present tense, for instance: *Add feature* or *Fix bug*.
- Have informative titles.
- If necessary, add a body with details.

### Before creating a pull request

- [Advanced] Try to create "atomic git commits" (recommended reading: [The Utopic Git History](https://blog.esciencecenter.nl/the-utopic-git-history-d44b81c09593)).
- Make sure the tests pass.
- Make sure the pre-commit tests pass.
- Fetch any `main` updates from upstream and rebase your branch, if necessary:

   ```bash
   git fetch upstream
   git rebase upstream/main BRANCH_NAME
   ```

- Then you can open a pull request and work with the reviewer to address any issues.

<!-- ## Tips
### Making a new release

Simple steps:

- Create a branch `release-x.y.z`
- Update `version` in `Project.toml`
- Update the `CHANGELOG.md`:
  - Rename the section "Unreleased" to "[x.y.z] - yyyy-mm-dd" (i.e., version under brackets, dash, and date in ISO format)
  - Add a new section on top of it named "Unreleased"
  - Add a new link in the bottom for version "x.y.z"
  - Change the "[unreleased]" link to use the latest version - end of line, `vx.y.z ... HEAD`.
- Create a commit "Release vx.y.z", push, create a PR, wait for it to pass, merge the PR.
- Go back to main screen and click on the latest commit (link: <https://github.com/ptypes-nlesc/data-profiling/commit/main>) -->
