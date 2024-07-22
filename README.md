# Transparency of Algorithmic Decision making (TAD)

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/minbzk/tad/ci.yml?label=tests)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MinBZK_tad&metric=coverage)](https://sonarcloud.io/summary/new_code?id=MinBZK_tad)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MinBZK_tad&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=MinBZK_tad)
![GitHub Release](https://img.shields.io/github/v/release/minbzk/tad?include_prereleases&sort=semver)
![GitHub License](https://img.shields.io/github/license/minbzk/tad)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=MinBZK_tad&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=MinBZK_tad)

TAD is a modern tool to apply technical and non-technical tests for an AI model.

Note: The main branch may be in an unstable or even broken state during development. Please use releases instead of the main branch.

## How to contribute

See [contributing docs](CONTRIBUTING.md)

## How to build and run TAD

See [build docs](BUILD.md)

## How to run the CLI

The check-state can be executed to see what tasks are waiting to be done.

It requires 2 parameters. The first parameter is a list of instrument urns joined by a comma without
spaces. The second parameter is the location of the system card.

An example command:
```shell
./check-state urn:nl:aivt:ir:td:1.0 urn:nl:aivt:ir:iama:1.0 example/system_test_card.yaml
```
