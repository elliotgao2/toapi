# Contributing to Toapi

An introduction to contributing to the Toapi project.

The Toapi project welcomes, and depends, on contributions from developers and
users in the open source community. Contributions can be made in a number of
ways, a few examples are:

- Code patches via pull requests
- Documentation improvements
- Bug reports and patch reviews

## Code of Conduct

Everyone interacting in the Toapi project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the [PyPA Code of Conduct].

## Reporting an Issue

Please include as much detail as you can. Let us know your platform and Toapi
version. If the problem is visual (for example a theme or design issue) please
add a screenshot and if you get an error please include the full error and
traceback.

## Installing for Development

Run the following command. It is **strongly** recommended that you do
this within a [virtualenv].

```bash
git clone https://github.com/gaojiuli/toapi
cd toapi
pip install --editable .
```

This will install Toapi in development mode which binds the `toapi` command
to the git repository.

## Running the tests

To run the tests, it is recommended that you use [pytest]. This just needs
to be pip installed and then the test suite can be ran for Toapi but running
the command `pytest` in the root of your Toapi repository.

It will attempt to run the tests against all of the Python versions we
support. So don't be concerned if you are missing some and they fail. The rest
will be verified by [Travis] when you submit a pull request.

## Submitting Pull Requests

Once you are happy with your changes or you are ready for some feedback, push
it to your fork and send a pull request. For a change to be accepted it will
most likely need to have tests and documentation if it is a new feature.

[virtualenv]: https://virtualenv.pypa.io/en/latest/userguide.html
[pytest]: https://docs.pytest.org/en/latest/
[travis]: https://travis-ci.org/repositories
[PyPA Code of Conduct]: https://www.pypa.io/en/latest/code-of-conduct/
