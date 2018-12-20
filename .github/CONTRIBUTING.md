# Contributing

We love contributions!  folium is open source, built on open source,
and we'd love to have you hang out in our community.

**Impostor syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not
ready to be an open source contributor; that your skills aren't nearly good
enough to contribute. What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong. If you can write code at
all, you can contribute code to open source. Contributing to open source
projects is a fantastic way to advance one's coding skills. Writing perfect code
isn't the measure of a good developer (that would disqualify all of us!); it's
trying to create something, making mistakes, and learning from those
mistakes. That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can
help out by writing documentation, tests, or even giving feedback about the
project (and yes - that includes giving feedback about the contribution
process). Some of these contributions may be the most valuable to the project as
a whole, because you're coming to the project with fresh eyes, so you can see
the errors and assumptions that seasoned contributors have glossed over.

(This disclaimer was originally written by
[Adrienne Lowe](https://github.com/adriennefriend) for a
[PyCon talk](https://www.youtube.com/watch?v=6Uj746j9Heo), and was adapted by folium
based on its use in the README file for the
[yt project](https://github.com/yt-project/yt/blob/master/README.md))

## Usage questions

The best place to submit questions about how to use folium is via the
[gitter](https://gitter.im/python-visualization/folium) channel.
Usage question in the issue tracker will probably go unanswered.

## Reporting issues

When reporting issues please include as much detail as possible regarding the folium and python version, use of notebooks, etc.
Whenever possible, please also include a [short, self-contained code example](http://sscce.org) that demonstrates the problem.

## Contributing code

First of all, thanks for your interest in contributing!

- If you are new to git/Github, please take check a few tutorials
  on [git](https://git-scm.com/docs/gittutorial) and [GitHub](https://guides.github.com/).
- The basic workflow for contributing is:
  1. [Fork](https://help.github.com/articles/fork-a-repo/) the repository
  2. [Clone](https://help.github.com/articles/cloning-a-repository/) the repository to create a local copy on your computer:
    ```
    git clone git@github.com:${user}/folium.git
    cd folium
    ```
  3. Create a branch for your changes
    ```
    git checkout -b name-of-your-branch
    ```
  4. Make change to your local copy of the folium repository
  5. Make sure the tests pass:
    * in the repository folder do `pip install -e .`  (needed for notebook tests)
    * along with all the dependencies install `phantomjs` via `npm install -g phantomjs` or by downloading it from [here](http://phantomjs.org/download.html) and installing manually
    * run `python -m pytest tests`
    * resolve all errors
  6. Commit those changes
    ```
    git add file1 file2 file3
    git commit -m 'a descriptive commit message'
    ```
  7. Push your updated branch to your fork
    ```
    git push origin name-of-your-branch
    ```
  8. [Open a pull request](https://help.github.com/articles/creating-a-pull-request/) to the python-visualization/folium
