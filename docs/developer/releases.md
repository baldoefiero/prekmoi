# Release Process

This document describes the manual process for preparing and publishing a new **prekmoi** release.

Releases follow [Semantic Versioning](https://semver.org/) and are published through GitHub
Releases.

## Version Management

The project version is declared in two locations:

- `pyproject.toml`: package metadata
- `src/prekmoi/__init__.py`: package `__version__` attribute.

Both declarations must always contain the same version.

## Changelog

The project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

During development, changes are collected under the `Unreleased` section in `CHANGELOG.md`.

When preparing a release:

1. Move the changes from `Unreleased` into a new version section.
2. Add the release date using the `YYYY-MM-DD` format.
3. Create a new empty `Unreleased` section for subsequent development.

## Release Procedure

### 1. Update the version

Choose the next version according to Semantic Versioning.

Update the version in both:

- `pyproject.toml`
- `src/prekmoi/__init__.py`

Ensure that both declarations match.

### 2. Update the changelog

Update `CHANGELOG.md`:

- move the relevant changes from `Unreleased` into the new version section;
- add the release date;
- create a new empty `Unreleased` section.

### 3. Run quality checks

Run the project's quality checks locally:

```
git add . --all
prek run --all-files
```

The command executes the configured hooks, including tests and static analysis.

### 4. Build the distribution

Build the source distribution and wheel:

```
python -m build
```

Verify that both distribution artifacts are generated successfully in `dist/`.

### 5. Commit the release preparation

Commit the version and changelog updates to `main`.

For example:

```
git add . --all
git commit -m "Release vX.Y.Z"
git push origin main
```

Wait for the GitHub Actions workflows to complete successfully.

### 6. Create the Git tag

Create an annotated tag using the `vX.Y.Z` format:

```
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

The tag must point to the release preparation commit on `main`.

### 7. Publish the GitHub Release

On GitHub:

1. Open the repository and go to **Releases**.
2. Select **Draft a new release**.
3. Select the tag created in the previous step.
4. Set the release title to `vX.Y.Z`.
5. Copy the corresponding changes from `CHANGELOG.md` into the release description.
6. Publish the release.

Do not generate release notes automatically: use the project's changelog as the source of truth.

### 8. Verify the release

After publication, verify that:

- The GitHub Release is publicly available.
- The release references the correct tag.
- The tag points to the intended commit.
- The release notes match `CHANGELOG.md`.

## Distribution

Publishing a GitHub Release does not automatically publish the package to PyPI.

PyPI publication is a separate process and is not currently part of the release procedure.
