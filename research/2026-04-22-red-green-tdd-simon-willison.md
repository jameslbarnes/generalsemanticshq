# Red/Green TDD — Simon Willison's Agentic Engineering Patterns

**Source:** https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/
**Author:** Simon Willison
**Published:** 23 February 2026, last modified 28 February 2026
**Shared by:** Carter
**Filed:** 2026-04-22

---

"Use red/green TDD" is a pleasingly succinct way to get better results out of a coding agent.

TDD stands for Test Driven Development. It's a programming style where you ensure every piece of code you write is accompanied by automated tests that demonstrate the code works.

The most disciplined form of TDD is test-first development. You write the automated tests first, confirm that they fail, then iterate on the implementation until the tests pass.

This turns out to be a *fantastic* fit for coding agents. A significant risk with coding agents is that they might write code that doesn't work, or build code that is unnecessary and never gets used, or both.

Test-first development helps protect against both of these common mistakes, and also ensures a robust automated test suite that protects against future regressions. As projects grow the chance that a new change might break an existing feature grows with them. A comprehensive test suite is by far the most effective way to keep those features working.

It's important to confirm that the tests fail before implementing the code to make them pass. If you skip that step you risk building a test that passes already, hence failing to exercise and confirm your new implementation.

That's what "red/green" means: the red phase watches the tests fail, then the green phase confirms that they now pass.

Every good model understands "red/green TDD" as a shorthand for the much longer "use test driven development, write the tests first, confirm that the tests fail before you implement the change that gets them to pass".

**Example prompt:**
> Build a Python function to extract headers from a markdown string. Use red/green TDD.

---

## Context: Agentic Engineering Patterns Guide

This article is one chapter in Simon Willison's larger guide on Agentic Engineering Patterns. Related chapters include:

**Principles:**
- What is agentic engineering?
- Writing code is cheap now
- Hoard things you know how to do
- AI should help us produce better code
- Anti-patterns: things to avoid

**Working with coding agents:**
- How coding agents work
- Using Git with coding agents
- Subagents

**Testing and QA:**
- Red/green TDD (this article)
- First run the tests
- Screenshot testing
- Mutation testing

**Project structure:**
- Write CLAUDE.md / AGENTS.md
- Project structure conventions

**Prompting techniques:**
- Thinking out loud
- Explore, then reset and implement

**Case studies:**
- GIF optimization tool using WebAssembly and Gifsicle
- Adding a new content type to my blog-to-newsletter tool

**Appendix:**
- Prompts I use

Full guide: https://simonwillison.net/guides/agentic-engineering-patterns/
