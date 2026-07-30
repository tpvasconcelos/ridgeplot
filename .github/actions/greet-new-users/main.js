// Core logic for the greet-new-users composite action (see action.yml).
//
// Kept in a standalone CommonJS module - rather than inline in action.yml -
// so it can be linted, syntax-checked, and unit-tested directly. It is
// invoked from actions/github-script, which injects its pre-authenticated
// Octokit client (`github`) plus the `core` and `context` helpers.
//
// The greeting messages are read from the ISSUE_MESSAGE / PR_MESSAGE
// environment variables (so that no user-controlled content is ever
// `${{ }}`-interpolated into script source), and a `greeted` output
// ("true"/"false") is always set.

module.exports = async function greet({ core, context, github }) {
  core.setOutput('greeted', 'false')
  try {
    // Only greet on newly created issues/PRs. Guards against consumers
    // triggering this action on e.g. `edited` events, which would
    // otherwise post duplicate greetings.
    if (context.payload.action !== 'opened') {
      return core.info(`Skipping: unsupported event action (${context.payload.action})`)
    }

    const isIssue = context.eventName === 'issues'
    const item = isIssue ? context.payload.issue : context.payload.pull_request
    if (!item) {
      return core.info(`Skipping: unsupported event (${context.eventName})`)
    }

    const message = isIssue ? process.env.ISSUE_MESSAGE : process.env.PR_MESSAGE
    if (!message) {
      return core.info(`Skipping: no ${isIssue ? 'issue' : 'pull request'} message configured`)
    }

    // Never greet bots (pre-commit.ci, dependabot, github-actions, Copilot, ...)
    const author = item.user
    if (author.type === 'Bot') {
      return core.info(`Skipping: ${author.login} is a bot`)
    }

    // Repo-affiliated authors are never "new users". This is only a
    // shortcut: a missing/unreliable value falls through to the real
    // check below, so it can never cause a wrong greeting.
    if (['OWNER', 'MEMBER', 'COLLABORATOR'].includes(item.author_association)) {
      return core.info(`Skipping: ${author.login} is ${item.author_association}`)
    }

    let isFirst = true
    if (isIssue) {
      // Everything this author created (the endpoint returns PRs too,
      // so keep only true issues that predate the current one).
      const created = await github.paginate(github.rest.issues.listForRepo, {
        ...context.repo,
        creator: author.login,
        state: 'all',
        per_page: 100,
      })
      isFirst = !created.some((i) => !i.pull_request && i.number < item.number)
    } else {
      // pulls.list cannot filter by author, so scan all PRs and stop
      // as soon as an older PR by this author shows up.
      await github.paginate(
        github.rest.pulls.list,
        { ...context.repo, state: 'all', per_page: 100 },
        (response, done) => {
          if (response.data.some((p) => p.user?.login === author.login && p.number < item.number)) {
            isFirst = false
            done()
          }
          return []
        },
      )
    }

    if (!isFirst) {
      return core.info(`Skipping: not ${author.login}'s first ${isIssue ? 'issue' : 'pull request'}`)
    }

    core.info(`Greeting ${author.login} on their first ${isIssue ? 'issue' : 'pull request'}`)
    await github.rest.issues.createComment({
      ...context.repo,
      issue_number: item.number,
      body: message,
    })
    core.setOutput('greeted', 'true')
  } catch (error) {
    // The greeting is cosmetic: a red X on a newcomer's first PR is
    // worse than a missing welcome, so warn instead of failing.
    core.warning(`Skipping greeting: ${error.message}`)
  }
}
