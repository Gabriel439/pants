# Haskell plugin

## Summary

Haskell's build tools operate at three layers of granularity:

* The `ghc` compiler builds object code from Haskell source files
* The `cabal` tool builds a Haskell package from a collection of Haskell source
  files and a package definition
* The `stack` tool manages a Haskell project from a collection of Haskell
  packages

This Haskell plugin provides a `pants` interface to the `stack` layer and may
eventually provide an interface to the `cabal` layer as well.  The `ghc`
compiler layer is indirectly managed by both `cabal` and `stack`.

Read the Background section if you are new to Haskell.  The Background section
gives an overview of the Haskell build tooling.

The Implementation section explains how this plugin wraps the Haskell build
tools in more detail.

## Terminology

* Package: A collection of source files
* Project: A collection of packages

## Background

### `ghc`

If you are familiar with C, `ghc` is analogous to a C compiler like `gcc` or
`clang`: source files go in one end and executables or object code come out the
other end.  The only difference is that when `ghc` emits object code it also
emits an additional "interface file" (with a `*.hi` suffix) which exports some
source code for cross-module inlining, specialization, and optimization.

Here's an example of generating object code and an interface file:

```bash
$ cat Test.hs
module Test where
foo = "An example string"

$ ghc -O2 Test.hs
[1 of 1] Compiling Test             ( Test.hs, Test.o )

$ ls
Test.hi Test.hs Test.o
```

... and here's an example of generating an executable:

```bash
$ cat HelloWorld.hs
main = putStrLn "Hello, world!"

$ ghc -O2 HelloWorld.hs
[1 of 1] Compiling Main             ( HelloWorld.hs, HelloWorld.o )
Linking HelloWorld ...

$ ls
HelloWorld    HelloWorld.hi HelloWorld.hs HelloWorld.o

$ ./HelloWorld
Hello, world!
```

By default, GHC executables are *mostly* statically linked, meaning that all
the Haskell code is statically linked, but some libraries that the Haskell
runtime requires are not (specifically `libc`, `libpthread`, and `libgmp`).  You
can optionally fully statically link an executable (i.e. like in Go), or
dynamically link Haskell libraries, but neither of those are the default
behavior.

`ghc` is a low-level tool that is only used for small, ad-hoc projects because
`ghc` does not do any formal dependency management.  For larger projects you
will typically use the `stack` tool (See the Stack section below for more
details).

Haskell code is also not distributed at the granularity of individual source
files or object code.  Instead, Haskell uses a package system like other
languages, which is the subject of the next section.

### Package creation

For all practical purposes packages are the atomic unit of distribution in
Haskell.  A minimal Haskell package is:

* a collection of source files
* a `*.cabal` file containing package meta-data
* a `LICENSE` file

Here is an example package layout:

```
mypackage/
|-- LICENSE
|-- mypackage.cabal
`-- src/
    `-- Foo/
        `-- Bar.hs
```

... where `mypackage.cabal` might look like this:

```
name:                minimal-example-library
version:             1.0.0
description:         Paradigm disruptor
license:             BSD
license-file:        LICENSE
author:              Alice
maintainer:          alice@example.com
build-type:          Simple
cabal-version:       >=1.10
 
library
    hs-source-dirs:    src
    build-depends:     base       >= 4.5 && < 4.8
                     , containers >= 0.5 && < 0.6
    exposed-modules:   Foo.Bar
```

... and `Foo/Bar.hs` might look like this:

```haskell
module Foo.Bar where

import Data.Set (Set, fromList)  -- This module comes from `containers`

baz :: Set Int
baz = fromList [1, 7, 4]
```

This package exports a Haskell module named `Foo.Bar`.  The module name must
match the directory/file layout underneath the source tree.

The `build-depends` section of the `*.cabal` file is where you specify
package dependencies.  For example, when we add `containers` as a build
dependency we can import any module exported by the `containers` package (and
`Data.Set` is one such module).  The package name does not need to match the
name of the modules it exports.

There are three main ways that you can make your package code available to
others in increasing order of diligence:

* The simplest approach is to provide a source distribution of your package
* You can also upload the package to Hackage under a name and version number
* If you are diligent you can optionally add any package on Hackage to Stackage

The more diligent you are the more easily others can depend on your package.

If you choose to only provide source distributions (perhaps hosted on Github)
then users can only depend on your package at the project level (See the
Projects section for more details).  At the package level you can only depend
on something that has been uploaded to Hackage.

Here is an example of such a Github-only source package named `pipes-tar`:

[https://github.com/ocharles/pipes-tar](https://github.com/ocharles/pipes-tar)

Hackage is a more formal package repository.  When you upload a package to
Hackage you specify a package name and version and then any other package can
depend on your package by specifying the same name and version number in their
`*.cabal` file.  Users can also specify version ranges for their dependencies
instead of fixed versions.

You can see an example package named `attoparsec` hosted on Hackage here:

[https://hackage.haskell.org/package/attoparsec](https://hackage.haskell.org/package/attoparsec)

The landing page for the above `attoparsec` package links to every version of
the package ever uploaded and defaults to the most recent version.

Stackage on the other hand is not a package repository; it's actually a
"version set repository".  Stackage keeps track of package versions that build
correctly together using a giant automated "mono-build" (i.e. one giant Haskell
project that attempts to simultaneously build all packages tracked by Stackage).
If a maintainer adds their package to Stackage then they are on the hook to
update their own package to continue building correctly within this mono-build.
Periodically the latest package versions that build together successfully are
frozen and released as version set snapshots known as "resolvers".  Stackage
provides both nightly snapshots named `"nightly-YYYY-MM-DD"` or long-term
support snapshots named `"lts-X.Y"`.

You can see what an example Stackage snapshot looks like here:

[https://www.stackage.org/lts-3.1/cabal.config](https://www.stackage.org/lts-3.1/cabal.config)

The above "resolver" is the long-term support snapshot version 3.1, and the
resolver is just a list of package version constraints.

### Package consumption

Every Haskell package must specify the names of direct dependencies.  To be
precise, if your source code imports some module named `Foo.Bar` then you must
depend on the package that exports `Foo.Bar` within your `*.cabal` file.  You do
not need to specify transitive dependencies that you don't directly import.

For each dependency you can specify either:

* a fixed version,
* a version range, or:
* no constraint at all

Haskell also imposes the restriction that you cannot have two versions of the
same package in a project's dependency graph.  I'm oversimplifying a bit, but
this is mostly true.

For a very long time, the idiomatic solution to dependency resolution was for
packages to specify their dependencies as version ranges.  Then the
`cabal-install` project management tool would use an SMT solver to select a
version for each package in the dependency graph that satisfied all version
constraints.

This version range and SMT-solver approach led to what is popularly known as
"cabal hell", which referred to the irreproducibility of Haskell builds.  A
package that initially built successfully could fail to build a year later.

To correct this problem the company FPComplete (the Haskell version of Scala's
TypeSafe) released a new project management tool named `stack`, which takes a
different approach to dependency resolution:

* Dependency versions are specified at the project level, not the package level
* A project fixes the versions of every package in the dependency graph and
  also fixes the version of compiler used to build the project

The project-level metadata is stored in a `stack.yaml` file.  Here's an example
of a minimal `stack.yaml` file that we can add to the above minimal package to
turn our package into a project:

```
flags: {}  # Ignore this field for now
packages:
- '.'
extra-deps: []
resolver: lts-3.1
```

The meaning of the fields are:

* `resolver`: Lock in versions for dependencies on Stackage
* `extra-deps`: Lock in versions for dependencies on Hackage but not on Stackage
* `packages`: All source dependencies for this project

Our example package had only one dependency (i.e. `containers`) and that
dependency is already constrained by Stackage, so we didn't need to specify any
other information within our `stack.yaml` file.

`stack` was designed to be backwards compatible with the prevous `cabal-install`
build tool and workflow.  This means that there is some duplication of
information: you can constrain a dependency version both at the package level
and the project level.  The best practice for open source is to do both to
ensure that packages build correctly with both the `cabal-install` and `stack`
build tools.  If you know that nobody will ever build your project using
`cabal-install` (such as in a closed source project) then you can safely specify
dependencies only at the project-level using `stack` and omit the version
bounds from the `build-depends` section of your `*.cabal` file.

Stackage encompasses a very wide swath of the most heavily used packages in the
Haskell ecosystem, so usually the `resolver` field suffices to lock in the
versions of all packages in your project's dependency graph.  For example, 96
of the top 100 packages and 752 of the top 1000 packages (by download) are on
Stackage.  You can find the set of packages constrained by a resolver by
visiting:

```
https://www.stackage.org/:resolver/cabal.config
```

For example, you can find the set of package versions constrained by the above
`lts-3.1` resolver here:

[https://www.stackage.org/lts-3.1/cabal.config](https://www.stackage.org/lts-3.1/cabal.config)

Notice that the default `stack.yaml` includes the current directory (i.e. `.`)
as a source dependency of the project.  This reflects the convention that a
`stack.yaml` file is usually located within the source root for your project's
top-level package.

You can also have a "headless" `stack`-managed project with no source
dependencies at all (i.e. the `packages` field is empty), and that's actually a
useful thing to do!  In fact, this Haskell plugin takes advantage of this
feature (See the Implementation section for more details).

Here's an example of a more complicated `stack.yaml` file:

```
flags: {}
packages:
- '../foo/bar'
- https://github.com/k0001/pipes-network/archive/pipes-network-0.6.4.tar.gz
extra-deps: [discrimination-0.1, promises-0.2]
resolver: lts-3.1
```

This project specifies the versions of two dependencies not constrained by the
`lts-3.1` Stackage snapshot (specifically the `discrimination` and `promises`
packages).  Additionally, this project has two source dependencies:

* A local package located at the relative directory `../foo/bar`
* A remote source tarball for the `pipes-network` package

The combination of the `resolver`, `extra-deps`, and `packages` fields ensure
that every `stack`-maintained project produces a reproducible build.

For the remainder of this document I will focus entirely on `stack` for
project management and ignore `cabal-install`.  I believe that `stack is a
significant improvement over `cabal-install` because:

* `stack` guarantees reproducible builds
* `stack` eliminates build failures for all packages on Stackage
* `stack` substantially reduces build failures even for packages off of Stackage
* `stack` treats the compiler as a dependency and isolates the compiler if it
   conflicts with any preinstalled compiler
* `stack` has a much better user experience (in my subjective opinion)
* `stack` requires substantially smaller package caches (See the next section)

... and commercial adoption is heavily biased in favor of `stack` for the above
reasons.

I'm only saying this so that I don't have to explain everything for both
the `stack` and `cabal-install` project managers.

### Package caches

Haskell programmers do not distribute packages as precompiled binaries (with the
exception of operating system package distributions like Debian).  Source
packages are the default.

However, that doesn't mean that you always have to recompile every dependency
every time that you build a new project.  `stack` keeps a global package cache
shared by all projects in the user's home directory (somewhere underneath the
`~/.stack` directory).  This prevents wasteful rebuilds of the same dependency
for multiple projects.

To a first approximation this cache stores a precompiled binary for every
unique combination of package name and version number that you depend on.  If
multiple `stack`-managed projects share the same the same "resolver" then
they will make excellent use of the cache because they will all use the same
version of every package that Stackage tracks.

I'm oversimplifying a bit how the cache works, but that's pretty close to the
truth.

## Implementation

### Targets

The most non-trivial design decision for this plugin is the choice of how to
encode Haskell targets.

For example, when I compile/test/benchmark something am I operating on:

* a Haskell source file?
* a Haskell package?
* a Haskell project?

For the following pants goals the Haskell tooling only provides support at the
package or project level:

* `test`
* `bench`
* `doc`

For these goals you can provide a reasonably interpretation at all three levels:

* `compile`
* `binary`
* `run`
* `repl`

So you could imagine that we could either have:

* source-file-level targets,
* package-level targets, or:
* project-level targets.

A "source-file-level" target would map onto `ghc` compiler flags.  A
"package-level" target would map onto a `*.cabal` file.  A "project-level"
target would map onto a `stack.yaml` file.

The first draft of this plugin treates targets as **projects**, meaning that
these targets will map onto `stack.yaml` files.  The main reason for this is
that there are a few important features that the existing Haskell build tooling
only provides at the project level:

* Dependencies on source packages
* Compiler toolchain bootstrapping and isolation
* `ghc-pkg` database isolation (really technical topic, not discussed)

These features could be implemented at the package level or source file level,
but they would have to either (A) be reimplemented within `pants` or more likely
(B) simulated by wrapping them in transient projects.  I chose to use
project-level targets to get something viable off the ground with as little code
as possible and reusing as much existing Haskell tooling and development idioms
as possible.

Each of the Haskell target types maps 1-to-1 on a field of the `stack.yaml`
file:

* `stackage` target maps onto the `resolver` field for Stackage packages
* `hackage` target maps onto the `extra-deps` field for Hackage packages
* the `cabal` target maps onto the `packages` field for source packages

All three of these targets contain:

* a target `name`
* the package `name`
* a Stackage `resolver` (see Resolver section below for more discussion)
* an optional `dependencies` field

For the `stackage` target, that's the only information you need since the
`resolver` already locks in a specific version.

For the `hackage` target, you must also specify a package version.

For the `cabal` target you specify a path to the source distribution which
can be a local directory or a remote tarball.

`stackage` targets are not necessary as dependencies since they are already
implicitly specified by the resolver field.  The only reason to have a
`stackage` target is if you want to directly `bench`/`test`/`repl` a package
tracked by Stackage.

The next logical progression for this plugin would be to add support for
package-level targets so that you could replace `*.cabal` files with `pants`
`BUILD` targets.

### Paths and working directories

This plugin configures the `stack` BUILD tool to use temporary directories
managed by `pants`, with one major exception: the cache directory.  `stack`
currently does not let you configure the cache directory in another location.
If this is an issue I can open up an issue against the `stack` tool to add
support for configuring the location of the package cache.

`stack` also stores a package-local cache for every source package.  This is how
`stack` implements incremental builds for projects spanning multiple source
packages.  As far as I know the location of these directories is also not
configurable and I can similarly open an issue about this if necessary.

### Resolvers

There are two ways you could implement resolvers:

* Every target specifies a `resolver` and tasks verify that all targets in a
  graph share the same `resolver`
* The resolver is specified for the repository as a whole (i.e. in `pants.ini`)

The current implementation does the former, but I'm seriously considering the
latter since it would simplify all the targets and it would maximize the
effectiveness of the package cache.

### Bootstrapping `stack`

The plugin currently does not bootstrap `stack` yet and instead uses whatever
`stack` it finds on the current `PATH` (if any).  There is no good reason for
this, I just haven't implemented this feature yet.

### Goals

The `pants` goals map very cleaningly onto `stack` goals.  `stack` is
basically the Haskell version of `pants` and provides many of the same goals
and features (i.e. caching, source dependencies, and toolchain bootstrapping),
which is why the mapping is very straightforward.

If you're familiar with `pants` then you can easily pick up `stack` by just
performing the following translations:

```
./pants compile  ->  stack build
./pants repl     ->  stack ghci
./pants doc      ->  stack haddock
./pants binary   ->  stack install
./pants run      ->  stack run
./pants test     ->  stack test
./pants bench    ->  stack bench
```

# TODO:

* Make the resolver repo-wide
