# Ray Tracing in One Weekend
_Codon edition_

## Goal

I recently came across an interesting [blog post](https://16bpp.net/blog/post/the-performance-impact-of-cpp-final-keyword/) on Reddit which mentioned a [series of free online books about Ray Tracing](https://raytracing.github.io/). I've previously dabbled in homemade ray tracing multiple times and in various forms (Java, C++, GLSL), so the book was not really for me, but I skimmed through nonetheless.

It was well written and I thought to myself, what if I followed this book not to learn ray tracing but a new language or cool piece of tech?

So I decided to go with [Codon](https://github.com/exaloop/codon), a Python implementation that compiles to native code, and see how performant I can get a ray tracer to be while staying reasonably pythonic.

## Requirements

You'll need a development build of Codon, as the latest release (v0.16.3) is about a year old, and contains some breaking inheritance bugs.

Install Codon normally by following the official instructions, then go to [Codon's CI builds](https://github.com/exaloop/codon/actions/workflows/ci.yml), click the latest build, go on the build corresponding to your OS, expand the "Upload Artifacts" step and download the link at the bottom of the log. Extract all the folders (`bin`, `include`, `lib` and `python`) in `~/.codon/` and you should be good to go.
