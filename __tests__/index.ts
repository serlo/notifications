import {
  Matchers,
  MessageProviderPact,
  Pact,
  Verifier
} from '@pact-foundation/pact'
import fetch from 'node-fetch'
import * as path from 'path'
import * as util from 'util'
import * as rimraf from 'rimraf'

const rm = util.promisify(rimraf)

const root = path.join(__dirname, '..')
const pactDir = path.join(root, 'pacts')

const httpPact = new Pact({
  consumer: 'notifications:http',
  provider: 'serlo.org:http',
  port: 9009,
  log: path.join(root, 'pact-http.log'),
  dir: path.join(pactDir, 'http'),
  cors: true
})

jest.setTimeout(30 * 1000)

beforeAll(async () => {
  await waitForServer()
  await rm(pactDir)
  await httpPact.setup()

  async function waitForServer() {
    const retries = 30
    for (let attempt = 0; attempt < 30; attempt++) {
      console.log(
        'Waiting for server, ',
        retries - attempt - 1,
        'remaining attempts…'
      )
      const res = await fetch('http://localhost:8000/health')
      if (res.status === 200 && (await res.json()) === 'ok') return
      await wait()
    }
  }

  function wait(ms = 1000) {
    return new Promise(resolve => {
      setTimeout(resolve, ms)
    })
  }
})

afterEach(async () => {
  await httpPact.verify()
})

afterAll(async () => {
  await httpPact.finalize()
})

test('HTTP Contract', async () => {
  await httpPact.addInteraction({
    state: 'a event with id 234 exists',
    uponReceiving: 'render event 234 in format html',
    withRequest: {
      method: 'POST',
      path: '/events/render/html',
      body: ['234']
    },
    willRespondWith: {
      status: 200,
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: {
        '234': {
          content: Matchers.string()
        }
      }
    }
  })
  await new Verifier({
    provider: 'notifications:http',
    providerBaseUrl: 'http://localhost:8000',
    pactBrokerUrl: 'https://pacts.serlo.org',
    validateSSL: false,
    stateHandlers: {
      'no notifications exist': () => {
        return fetch('http://localhost:8000/pact/set-state/', {
          method: 'POST',
          body: JSON.stringify({
            consumer: 'serlo.org',
            state: 'no notifications exist'
          })
        })
      },
      'a notification for user 123 and event 234 exists': () => {
        return fetch('http://localhost:8000/pact/set-state/', {
          method: 'POST',
          body: JSON.stringify({
            consumer: 'serlo.org',
            state: 'a notification for user 123 and event 234 exists'
          })
        })
      }
    }
  }).verifyProvider()
})

test('Message Contract', async () => {
  await new MessageProviderPact({
    messageProviders: {
      'a `create-event` message': async () => {
        const message = {
          type: 'create-event',
          payload: {
            event: { provider_id: 'serlo.org', id: '123' },
            created_at: '2015-08-06T16:53:10+01:00',
            source: { provider_id: 'serlo.org' }
          }
        }
        await fetch('http://localhost:8000/pact/execute-message/', {
          method: 'POST',
          body: JSON.stringify(message)
        })
        return message
      },
      'a `create-notification` message': async () => {
        const message = {
          type: 'create-notification',
          payload: {
            event: { provider_id: 'serlo.org', id: '123' },
            user: { provider_id: 'serlo.org', id: '234' },
            source: { provider_id: 'serlo.org' }
          }
        }
        await fetch('http://localhost:8000/pact/execute-message/', {
          method: 'POST',
          body: JSON.stringify(message)
        })
        return message
      },
      'a `read-notification` message': async () => {
        const message = {
          type: 'read-notification',
          payload: {
            event: { provider_id: 'serlo.org', id: '234' },
            user: { provider_id: 'serlo.org', id: '123' },
            created_at: '2015-08-06T16:53:10+01:00',
            source: { provider_id: 'serlo.org' }
          }
        }
        await fetch('http://localhost:8000/pact/execute-message/', {
          method: 'POST',
          body: JSON.stringify(message)
        })
        return message
      }
    },
    consumer: 'serlo.org:messages',
    provider: 'notifications:messages',
    stateHandlers: {
      'no notifications exist': () => {
        return fetch('http://localhost:8000/pact/set-state/', {
          method: 'POST',
          body: JSON.stringify({
            consumer: 'serlo.org',
            state: 'no notifications exist'
          })
        })
      },
      'one event with id 123 exists': () => {
        return fetch('http://localhost:8000/pact/set-state/', {
          method: 'POST',
          body: JSON.stringify({
            consumer: 'serlo.org',
            state: 'one event with id 123 exists'
          })
        })
      },
      'a notification for user 123 and event 234 exists': () => {
        return fetch('http://localhost:8000/pact/set-state/', {
          method: 'POST',
          body: JSON.stringify({
            consumer: 'serlo.org',
            state: 'a notification for user 123 and event 234 exists'
          })
        })
      }
    },
    pactBrokerUrl: 'https://pacts.serlo.org'
  }).verify()
})
