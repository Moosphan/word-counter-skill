# Publishing Guide

This document is for maintainers of the repository, not end users of the skill.

## What The Workflow Does

The repository includes two GitHub Actions workflows:

- `ci.yml`: runs tests and verifies that release artifacts can be packaged
- `release.yml`: builds versioned Codex and Claude Code zip packages and publishes them to GitHub Releases

## Recommended Release Flow

1. Push a version tag such as `v0.1.0`
2. GitHub Actions runs the test suite
3. The runtime is synced into both skill packages
4. Release archives and the manifest are built
5. A GitHub Release is created or updated with the packaged assets

## Manual Release Flow

Run `release.yml` from GitHub Actions and provide the `version` input.

## Published Artifacts

- `codex-word-counter-skill-<version>.zip`
- `claude-code-word-counter-skill-<version>.zip`
- `release-manifest-<version>.json`

## Notes

- The workflows assume Python 3.11 on GitHub-hosted runners.
- If you later publish to a marketplace, keep the same packaging step and add the marketplace-specific upload step afterward.
