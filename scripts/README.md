
## [`ci_test_all.sh`](ci_test_all.sh)

Script to lunch tests on all board connected to the ci or on a subset of them.
It is only executed on applications with a test script. It can be launched on a
subset of these applications.

### Usage

- connect to the ci:

    $ ssh ci@ci-riot-tribe.saclay.inria.fr

- run tests:

    $ /builds/scripts/ci_test_all.sh /builds/tmp/RIOT -a examples/hello-world -b samr21-xpro